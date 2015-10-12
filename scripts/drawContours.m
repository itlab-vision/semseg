% function [img_r, img_g, img_b] = drawContours(img_r, img_g, img_b, ...
%                                               bnd_logical, color_contour)
% img_r         - R-channel of segmented image
% img_g         - G-channel of segmented image
% img_b         - B-channel of segmented image
% bnd_logical   - logical matrix of segments boundaries
% color_contour - color of all contours
function [img_r, img_g, img_b] = drawContours(img_r, img_g, img_b, ...
                                              bnd_logical, color_contour)


% 5 x 5 pixels for contour
shifts = [-2 -1 0 1 2];

for i = 1 : length(shifts)
    for j = 1 : length(shifts)
        shift = [shifts(i), shifts(j)];
        % shift and duplicate contour
        bnd_logical_shift = circshift(bnd_logical, shift);
        img_r(bnd_logical_shift) = color_contour(1);
        img_g(bnd_logical_shift) = color_contour(2);
        img_b(bnd_logical_shift) = color_contour(3);
    end
end
