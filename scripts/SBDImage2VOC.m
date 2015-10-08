% Script for preparing segmented image of the Semantic Boundaries Dataset
% http://www.cs.berkeley.edu/~bharath2/codes/SBD/download.html
% to PASCAL VOC format

% function img = SBDImage2VOC(GT)
% GT  - Semantic Boundaries Dataset groundtruth
% img - segmented image in PASCAL VOC format
function img = SBDImage2VOC(GT)

% generate random colors for 20 object classes
color_map = rand(20, 3);

% get full groundtruth information
sgm = GT.Segmentation;
cls = GT.Categories;
bnd = GT.Boundaries;

% prepare 3-channel image
contours_r = zeros(size(sgm, 1), size(sgm, 2), 1);
contours_g = zeros(size(sgm, 1), size(sgm, 2), 1);
contours_b = zeros(size(sgm, 1), size(sgm, 2), 1);
for i = 1 : length(bnd)
   bnd_logical = bnd{i, 1};
   color = color_map(cls(i), :); 
   display(sprintf('class = %d; color = (%.4f %.4f %.4f)', ...
                   cls(i), color(1), color(2), color(3)));
   contours_r(bnd_logical) = color(1);
   contours_g(bnd_logical) = color(2);
   contours_b(bnd_logical) = color(3);   
end
img = cat(3, contours_r, contours_g, contours_b);