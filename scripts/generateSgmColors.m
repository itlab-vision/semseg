% function color_map = generateSgmColors(num_classes)
% num_classes - number of classes to fill segments
% color_map   - color list ( size = [num_classes x 3])
function color_map = generateSgmColors(num_classes)

% call function 'labelcolormap' from PASCAL VOC Devkit
color_map = labelcolormap(num_classes);
% show colors for all classes
for i = 1 : num_classes
    display(sprintf('class_id = %d; color_id = (%d, %d, %d)', ...
                    i, color_map(i, 1), color_map(i, 2), color_map(i, 3)));
end