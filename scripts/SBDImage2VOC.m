% Script for preparing segmented image of the Semantic Boundaries Dataset
% http://www.cs.berkeley.edu/~bharath2/codes/SBD/download.html
% to PASCAL VOC format

% function img = SBDImage2VOC(GT)
% GT  - Semantic Boundaries Dataset groundtruth
% img - segmented image in PASCAL VOC format
function img = SBDImage2VOC(GT)

% generate random colors for 20 obkect classes
color_map = rand(20, 3);

% get full groundtruth information
sgm = GT.Segmentation;
cls = GT.Categories;
bnd = GT.Boundaries;

% prepare 3-channel image
img = cat(3, sgm, sgm, sgm);
for i = 1 : length(bnd)
   bnd_logical = bnd{i, 1};
   color = color_map(cls(i));
   img(bnd_logical) = color;
end
