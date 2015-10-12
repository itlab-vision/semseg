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

% 5 x 5 pixels for contour
shifts = [-2 -1 0 1 2];

for i = 1 : length(shifts)
	% consider as a 2 dim matrix. Each shift is computed as i-th element of 
	% multiplication: {shifts} x {shifts}
	shift = [shifts(1 + floor(i / 5)), shifts(1 + mod(i, 5))];
	% shift and duplicate contour
	bnd_logical_shift = circshift(bnd_logical, shift);
	img_r(bnd_logical_shift) = color_contour(1);
	img_g(bnd_logical_shift) = color_contour(2);
	img_b(bnd_logical_shift) = color_contour(3);
end