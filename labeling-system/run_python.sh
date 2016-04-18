#!/bin/sh
prj_path=$1
if [[ $prj_path = "" ]]
    then echo "Error: use run.sh project_path"
fi

srun -t "00:03:00"  -N 1 -p gpu -o "$prj_path/out_python.txt"\
    python $prj_path/test_segmentation_camvid.py\
    --model $prj_path/models/segnet_inference_modified.prototxt\
    --weights $prj_path/models/segnet_weights_driving_webdemo.caffemodel\
    --path_to_images $prj_path/CamVid/test\
    --iter 200\
    --result_dir $prj_path/out_img &
