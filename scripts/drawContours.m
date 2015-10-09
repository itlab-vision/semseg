% function [img_r, img_g, img_b] = drawContours(img_r, img_g, img_b, ...
%                                               bnd_logical, color_contour)
% img_r         - R-channel of segmented image
% img_g         - G-channel of segmented image
% img_b         - B-channel of segmented image
% bnd_logical   - logical matrix of segments boundaries
% color_contour - color of all contours
function [img_r, img_g, img_b] = drawContours(img_r, img_g, img_b, ...
                                              bnd_logical, color_contour)
% draw contour
img_r(bnd_logical) = color_contour(1);
img_g(bnd_logical) = color_contour(2);
img_b(bnd_logical) = color_contour(3);

% shift and duplicate contour
bnd_logical_shift = circshift(bnd_logical, [-1 -1]);
img_r(bnd_logical_shift) = color_contour(1);
img_g(bnd_logical_shift) = color_contour(2);
img_b(bnd_logical_shift) = color_contour(3);

bnd_logical_shift = circshift(bnd_logical, [ 0 -1]);
img_r(bnd_logical_shift) = color_contour(1);
img_g(bnd_logical_shift) = color_contour(2);
img_b(bnd_logical_shift) = color_contour(3);

bnd_logical_shift = circshift(bnd_logical, [ 1 -1]);
img_r(bnd_logical_shift) = color_contour(1);
img_g(bnd_logical_shift) = color_contour(2);
img_b(bnd_logical_shift) = color_contour(3);

bnd_logical_shift = circshift(bnd_logical, [-1  0]);
img_r(bnd_logical_shift) = color_contour(1);
img_g(bnd_logical_shift) = color_contour(2);
img_b(bnd_logical_shift) = color_contour(3);

bnd_logical_shift = circshift(bnd_logical, [ 1  0]);
img_r(bnd_logical_shift) = color_contour(1);
img_g(bnd_logical_shift) = color_contour(2);
img_b(bnd_logical_shift) = color_contour(3);

bnd_logical_shift = circshift(bnd_logical, [-1  1]);
img_r(bnd_logical_shift) = color_contour(1);
img_g(bnd_logical_shift) = color_contour(2);
img_b(bnd_logical_shift) = color_contour(3);

bnd_logical_shift = circshift(bnd_logical, [ 0  1]);
img_r(bnd_logical_shift) = color_contour(1);
img_g(bnd_logical_shift) = color_contour(2);
img_b(bnd_logical_shift) = color_contour(3);

bnd_logical_shift = circshift(bnd_logical, [ 1  1]);
img_r(bnd_logical_shift) = color_contour(1);
img_g(bnd_logical_shift) = color_contour(2);
img_b(bnd_logical_shift) = color_contour(3);
