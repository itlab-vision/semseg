% Script for preparing segmented image of the Semantic Boundaries Dataset
% http://www.cs.berkeley.edu/~bharath2/codes/SBD/download.html
% to PASCAL VOC format

% function img = SBDImage2VOC(GT)
% GT  - Semantic Boundaries Dataset groundtruth
% img - segmented image in PASCAL VOC format
function img = SBDImage2VOC(GT)

% generate random colors for 20 object classes
num_classes = 20;
color_map = randi([0 255], num_classes, 3);
% show colors for all classes
% for i = 1 : num_classes
%    display(sprintf('class_id = %d; color_id = (%d, %d, %d)', ...
%                    i, color_map(i, 1), color_map(i, 2), color_map(i, 3)));
% end

% get full groundtruth information
sgm = uint8(GT.Segmentation);
img_r = uint8(zeros(size(sgm, 1), size(sgm, 2), 1));
img_g = uint8(zeros(size(sgm, 1), size(sgm, 2), 1));
img_b = uint8(zeros(size(sgm, 1), size(sgm, 2), 1));
for i = 1 : num_classes    
    indeces = (sgm == i);
    img_r(indeces) = color_map(i, 1);
    img_g(indeces) = color_map(i, 2);
    img_b(indeces) = color_map(i, 3);
end
img = cat(3, img_r, img_g, img_b);
