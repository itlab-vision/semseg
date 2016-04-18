#include <stdio.h>
#include <stdint.h>
#include <iostream>
#include <vector>
#include <fstream>
#include <strstream>

#define _USE_MATH_DEFINES
#include <math.h>

#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>

static std::string input_data, config_file;

static int printUsage()
{
    std::cout << "Usage: segm_tool [OPTIONS]" << std::endl;
    std::cout << "Options:" << std::endl;
    std::cout << "  --input_data     path       - path to input data" << std::endl;
    std::cout << "  --config_file    path       - path to configuration file" << std::endl;
    exit(1);
}
static void parseCmdArg(int argc, const char* argv[])
{
    for (int i = 1; i < argc; i++)
    {
        int argv_len = (int)strlen(argv[i]);
        if (0 == memcmp("--input_data", argv[i], argv_len))
            input_data = argv[++i];
        else if (0 == memcmp("--config_file", argv[i], argv_len))
            config_file = argv[++i];
        else if (0 == strcmp("--help", argv[i]))
        {
            printUsage();
        }
    }
}

struct ObjectInfo
{
    char key;
    int id;
    std::string hint;
    cv::Scalar color;
};

class ObjectsSetting
    : public std::vector<ObjectInfo>
{
public:
    ObjectsSetting()
        : LUT(0)
        , lut_count(0)
    {
    }
    ~ObjectsSetting()
    {
        if (!LUT)
            delete[]LUT;
    }

    bool load(const std::string &config_file)
    {
        cv::FileStorage config(config_file, cv::FileStorage::READ);
        if (!config.isOpened())
            return false;
        this->clear();

        cv::FileNode root = config["objects"];
        for (auto it = root.begin(); it != root.end(); it++)
        {
            ObjectInfo info;
            info.key = ((std::string)(*it)["key"])[0];
            info.id = (int)(*it)["id"];
            info.hint = (*it)["hint"];
            (*it)["color"] >> info.color;
            this->push_back(info);
        }
        return (0 < this->size());
    }

    int parse_key(char ch) const
    {
        for (int o = 0; o < this->size(); o++)
        {
            if (ch == (*this)[o].key)
                return o;
        }
        return -1;
    }

    size_t get_LUT(cv::Vec3b *&lut)
    {
        if (0 != LUT)
        {
            lut = LUT;
            return lut_count;
        }
        lut_count = this->size();
        if (0 == lut_count)
        {
            lut = 0;
            return 0;
        }
        LUT = new cv::Vec3b[lut_count];
        for (size_t i = 0; i < lut_count; i++)
        {
            LUT[i][0] = (uchar)((*this)[i].color[0]);
            LUT[i][1] = (uchar)((*this)[i].color[1]);
            LUT[i][2] = (uchar)((*this)[i].color[2]);
        }
        return lut_count;
    }
private:
    cv::Vec3b *LUT;
    size_t lut_count;
};

static void draw_help(cv::Mat &help_img, const ObjectsSetting &setting)
{
    static const int    fontFace = 0;
    static const double fontScale = 0.3;
    static const int    thickness = 1;
    static const int    gap = 7;

    cv::Size img_size(0, gap);
    std::vector<cv::Point> text_orig(setting.size());
    cv::Point pt(gap, gap);
    for (int o = 0; o < setting.size(); o++)
    {
        cv::String msg = cv::format("%c - %s", setting[o].key, setting[o].hint.c_str());
        int baseline;
        cv::Size textSize = cv::getTextSize(msg, fontFace, fontScale, thickness, &baseline);
        img_size.height += textSize.height + gap;
        img_size.width = MAX(textSize.width + 2 * gap, img_size.width);

        text_orig[o] = pt;
        text_orig[o].y += baseline + thickness;
        pt.y += textSize.height + gap;
    }

    help_img.create(img_size, CV_8UC3); help_img.setTo(255);
    for (int o = 0; o < setting.size(); o++)
    {
        cv::String msg = cv::format("%c - %s", setting[o].key, setting[o].hint.c_str());
        cv::putText(help_img, msg, text_orig[o], fontFace, fontScale, setting[o].color);
    }
}

static int object_idx = -1;
static cv::Mat markers;
static cv::Point prevPt(-1, -1);
static ObjectsSetting setting;
static int marker_thickness = 2;
static void onMouse(int event, int x, int y, int flags, void* data)
{
    if (-1 == object_idx)
        return;

    cv::Mat *show_img = (cv::Mat *)data;
    if (event == cv::EVENT_LBUTTONUP || !(flags & cv::EVENT_FLAG_LBUTTON))
        prevPt = cv::Point(-1, -1);
    else if (event == cv::EVENT_LBUTTONDOWN)
        prevPt = cv::Point(x, y);
    else if (event == cv::EVENT_MOUSEMOVE && (flags & cv::EVENT_FLAG_LBUTTON))
    {
        cv::Point pt(x, y);
        if (prevPt.x < 0)
            prevPt = pt;
        cv::line(markers, prevPt, pt, cv::Scalar::all(setting[object_idx].id), marker_thickness);
        cv::line(*show_img, prevPt, pt, setting[object_idx].color, marker_thickness);
        prevPt = pt;

        cv::imshow("image", *show_img);
    }
}

int main(int argc, const char** argv)
{
    parseCmdArg(argc, argv);
    if (input_data.empty() || config_file.empty())
    {
        printUsage();
        return 1;
    }

    if (!setting.load(config_file))
        return 1;
    std::vector<cv::String> input_files;
    cv::glob(input_data, input_files);
    if (input_files.empty())
        return 1;

    cv::Mat help_img;
    draw_help(help_img, setting);

    bool show_help = false;
    double transparent = 0.;
    for (int i = 0; i < input_files.size(); i++)
    {
        cv::Mat img = cv::imread(input_files[i], cv::IMREAD_COLOR);
        
        cv::Mat show_img; img.copyTo(show_img);
        markers.create(img.size(), CV_32SC1); markers.setTo(-1);
        int c = 0;
        for (;;)
        {
            img.copyTo(show_img);

            cv::Vec3b *lut; setting.get_LUT(lut);
            if (lut)
            {
                cv::Mat temp;
                if (0. < transparent)
                    temp.create(show_img.size(), CV_8UC3);
                else
                    temp = show_img;

                for (int row = 0; row < show_img.rows; row++)
                {
                    cv::Vec3b *ptr_img = temp.ptr<cv::Vec3b>(row);
                    int *ptr_markers = markers.ptr<int>(row);
                    for (int col = 0; col < show_img.cols; col++)
                    {
                        if (-1 == ptr_markers[col])
                            continue;
                        ptr_img[col] = lut[ptr_markers[col]];
                    }
                }
                if (0. < transparent)
                    cv::addWeighted(show_img, 1. - transparent, temp, transparent, 0., show_img);
            }

            if (show_help)
            {
                cv::Mat temp = show_img(cv::Rect(0, 0, help_img.cols, help_img.rows));
                cv::addWeighted(temp, 0.4, help_img, 0.6, 0., temp);
            }

            cv::imshow("image", show_img);
            cv::setWindowTitle("image", input_files[i]);
            cv::setMouseCallback("image", onMouse, (&show_img));
            int c = cv::waitKey(0);
            if (27 == c)
                break;
            if (' ' == c)
                break;

            img.copyTo(show_img);
            int obj_idx_new = setting.parse_key(c);
            if (-1 != obj_idx_new)
                object_idx = obj_idx_new;
            switch (c)
            {
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                marker_thickness = (int)(c - '0');
                break;
            case 'h':
                show_help = !show_help;
                break;
            case 'w':
                cv::watershed(img, markers);
                break;
            case 't':
                transparent += 0.2;
                if (1.0 < transparent)
                    transparent = 0.0;
                break;
            }
        }
        if (27 == c)
            break;
    }

    return 0;
}
