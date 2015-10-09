% Script for preparing segmented image of the Semantic Boundaries Dataset
% http://www.cs.berkeley.edu/~bharath2/codes/SBD/download.html
% to PASCAL VOC format

% function img = SBDImage2VOC(GTcls, GTinst)
% GTcls       - Semantic Boundaries Dataset classes groundtruth
% GTinst      - Semantic Boundaries Dataset boundaries groundtruth
% img         - segmented image in PASCAL VOC format
% num_classes - number of semantic classes
% color_map   - generated color map for semantic classes
function img = SBDImage2VOC(GTcls, GTinst, num_classes, color_map)

% prepare segmented image
sgm = uint8(GTcls.Segmentation);
img_r = uint8(zeros(size(sgm, 1), size(sgm, 2), 1));
img_g = uint8(zeros(size(sgm, 1), size(sgm, 2), 1));
img_b = uint8(zeros(size(sgm, 1), size(sgm, 2), 1));
for i = 1 : num_classes    
    indeces = (sgm == i);
    img_r(indeces) = color_map(i, 1);
    img_g(indeces) = color_map(i, 2);
    img_b(indeces) = color_map(i, 3);
end

% draw contours on the segmented image
color_contour = [255 255 255];
bnds = GTinst.Boundaries;
for i = 1 : length(bnds)
    bnd_logical = bnds{i, 1};
    [img_r, img_g, img_b] = ...
        drawContours(img_r, img_g, img_b, bnd_logical, color_contour);
end
img = cat(3, img_r, img_g, img_b);