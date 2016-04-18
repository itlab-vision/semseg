#!/bin/sh
prj_path=$1
if [[ $prj_path = "" ]]
    then echo "Error: use run.sh project_path"
fi

srun -t "00:03:00"  -N 1 -p gpu -o "$prj_path/out.txt"\
    /home/kruchinin_d/lib/caffe-segnet/caffe-segnet-segnet-cleaned/build/tools/caffe\
    test -gpu 0\
    -model $prj_path/models/segnet_mdw_modified.prototxt\
    -weights $prj_path/models/segnet_weights_driving_webdemo.caffemodel &
