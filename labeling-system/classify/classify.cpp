#define USE_MKL // workaround for using mkl

#include <caffe/caffe.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <string>
#include <vector>
#include <memory>

using namespace caffe;
using std::string;

class Classifier {
  public:
    Classifier(const string& model_file,
               const string& trained_file,
               const string& annot_file,
               const string& result_folder);

    void Classify();

  private:
    void Classify(const cv::Mat& img, cv::Mat& dst);
    std::vector<float> Predict(const cv::Mat& img);
    void WrapInputLayer(std::vector<cv::Mat>* input_channels);
    void Preprocess(const cv::Mat&, std::vector<cv::Mat>*);

  private:
    shared_ptr<Net<float> > net_;
    cv::Size input_geometry_;
    int num_channels_;
    std::vector<string> filenames_;
    string result_folder_;
};

Classifier::Classifier(const string& model_file,
                       const string& trained_file,
                       const string& annot_file,
                       const string& result_folder) {
#ifdef CPU_ONLY
    Caffe::set_mode(Caffe::CPU);
#else
    Caffe::set_mode(Caffe::GPU);
#endif

    /* Load the network. */
    net_.reset(new Net<float>(model_file, TEST));
    net_->CopyTrainedLayersFrom(trained_file);

    CHECK_EQ(net_->num_inputs(), 1) << "Network should have exactly one input.";
    CHECK_EQ(net_->num_outputs(), 1) << "Network should have exactly one output.";

    Blob<float>* input_layer = net_->input_blobs()[0];
    num_channels_ = input_layer->channels();
    CHECK(num_channels_ == 3 || num_channels_ == 1)
        << "Input layer should have 1 or 3 channels.";
    input_geometry_ = cv::Size(input_layer->width(), input_layer->height());

    /* Load filenames. */
    std::ifstream filenames(annot_file.c_str());
    CHECK(filenames) << "Unable to open annotation file " << annot_file;
    string line;
    while (std::getline(filenames, line))
        filenames_.push_back(string(line));

    Blob<float>* output_layer = net_->output_blobs()[0];

    result_folder_ = result_folder;
}

void Classifier::Classify(const cv::Mat& img, cv::Mat& dst) {
    std::vector<float> output = Predict(img);
    dst = cv::Mat(output, false);
}

std::vector<float> Classifier::Predict(const cv::Mat& img) {
    Blob<float>* input_layer = net_->input_blobs()[0];
    input_layer->Reshape(1, num_channels_,
                       input_geometry_.height, input_geometry_.width);
    /* Forward dimension change to all layers. */
    net_->Reshape();

    std::vector<cv::Mat> input_channels;
    WrapInputLayer(&input_channels);

    Preprocess(img, &input_channels);

    net_->ForwardPrefilled();

    /* Copy the output layer to a std::vector */
    Blob<float>* output_layer = net_->output_blobs()[0];
    const float* begin = output_layer->cpu_data();
    const float* end = begin + output_layer->shape(0) *
                             output_layer->shape(1) *
                             output_layer->shape(2) *
                             output_layer->shape(3);
    std::cout << output_layer->shape_string() << std::endl;
    std::cout << "c " << output_layer->shape(0) << " "
            << output_layer->shape(1) << " "
            << output_layer->shape(2) << " "
            << output_layer->shape(3) << std::endl;
    return std::vector<float>(begin, end);
}

/* Wrap the input layer of the network in separate cv::Mat objects
 * (one per channel). This way we save one memcpy operation and we
 * don't need to rely on cudaMemcpy2D. The last preprocessing
 * operation will write the separate channels directly to the input
 * layer. */
void Classifier::WrapInputLayer(std::vector<cv::Mat>* input_channels) {
    Blob<float>* input_layer = net_->input_blobs()[0];

    int width = input_layer->width();
    int height = input_layer->height();
    float* input_data = input_layer->mutable_cpu_data();
    for (int i = 0; i < input_layer->channels(); ++i) {
        cv::Mat channel(height, width, CV_32FC1, input_data);
        input_channels->push_back(channel);
        input_data += width * height;
    }
}

void Classifier::Preprocess(const cv::Mat& img,
                            std::vector<cv::Mat>* input_channels) {
  cv::Mat sample_float;
  img.convertTo(sample_float, CV_32FC3);

  cv::split(sample_float, *input_channels);

  CHECK(reinterpret_cast<float*>(input_channels->at(0).data)
        == net_->input_blobs()[0]->cpu_data())
    << "Input channels are not wrapping the input layer of the network.";
}


void Classifier::Classify() {
    cv::Vec3b Sky(128,128,128);
	cv::Vec3b Building(128,0,0);
	cv::Vec3b Pole(192,192,128);
	cv::Vec3b Road_marking(255,69,0);
	cv::Vec3b Road(128,64,128);
	cv::Vec3b Pavement(60,40,222);
	cv::Vec3b Tree(128,128,0);
	cv::Vec3b SignSymbol(192,128,128);
	cv::Vec3b Fence(64,64,128);
	cv::Vec3b Car(64,0,128);
	cv::Vec3b Pedestrian(64,64,0);
	cv::Vec3b Bicyclist(0,128,192);
	cv::Vec3b Unlabelled(0,0,0);

    cv::Vec3b classes_[] = { Sky, Building, Pole,
        Road_marking, Road, Pavement, Tree,
        SignSymbol, Fence, Car, Pedestrian,
        Bicyclist, Unlabelled };

    std::vector<cv::Vec3b> classes(classes_, classes_ + 12);

    for (int f = 0; f < filenames_.size(); f++) {
        cv::Mat img = cv::imread(filenames_[f], 0);
        cv::Mat dst;
        Classify(img, dst);

        cv::Mat result(360, 480, CV_8UC3);
        for (int i = 0; i < 360; i++) {
            for (int j = 0; j < 480; j++) {
                std::cout << "(" << i << "," << j << ") ";
                //result.at<cv::Vec3b>(i, j) = classes_[static_cast<int>(dst.at<float>(i, j))];
                std::cout << dst.at<float>(i, j) << " ";
            }
            std::cout << std::endl;
        }
        cv::imwrite(result_folder_ + "/result_" + filenames_[f], result);
    }
}

int main(int argc, char* argv[]) {
    if (argc != 5) {
        std::cerr << "Usage: " << argv[0]
                  << " deploy.prototxt network.caffemodel"
                  << " annotation.txt result_folder" << std::endl;
        return 1;
    }

    ::google::InitGoogleLogging(argv[0]);

    Classifier *classifier = new Classifier(argv[1], argv[2], argv[3], argv[4]);
    classifier->Classify();

    return 0;
}
