% Script for conversion of the Semantic Boundaries Dataset
% http://www.cs.berkeley.edu/~bharath2/codes/SBD/download.html
% to PASCAL VOC format

% This script should be used for training DeepLab models
% on augmented PASCAL VOC 2012 dataset

% function [] = SBDataset2VOC(dataset_dir, output_dir, prefix)
% dataset_dir - directory containing the Semantic Boundaries Dataset
% output_dir  - directory to put converted data
% prefix      - which part of dataset to convert ('train' or 'val')
function [] = SBDataset2VOC(dataset_dir, output_dir, prefix)

output_aug_folder_name = ['SegmentationClass_', prefix, '_aug_cls'];
images_folder_name = 'img';
output_path = fullfile(output_dir, output_aug_folder_name);
if (exist(output_path, 'dir') ~= 7)
    mkdir(output_path);
end
dataset_info_name = fullfile(output_dir, [prefix, '_aug_cls.txt']);

% read dataset list
display('---------------------------------------------------------');
dataset_list_name = fullfile(dataset_dir, [prefix, '.txt']);
display(sprintf('Reading dataset list %s...\n', dataset_list_name));
dataset_list_fid = fopen(dataset_list_name, 'r');
if (dataset_list_fid == -1)
  display(sprintf('Error: Failed to load a file %s. Aborting.\n', ...
                  dataset_list_name));
  exit;
end
dataset_list = textscan(dataset_list_fid, '%s');
fclose(dataset_list_fid);
dataset_list_length = length(dataset_list{1});
display(sprintf('Entries count: %d.\n', dataset_list_length));
display(sprintf('Reading dataset list %s.\n', dataset_list_name));
display('---------------------------------------------------------');

% open (and create if it doesn't exist) file for augmented information
dataset_info = fopen(dataset_info_name, 'w+');
if (dataset_info_name == -1)
  display(sprintf('Error: Failed to create a file %s. Aborting.\n', ...
                  dataset_info_name));
  exit;
end

% list all samples and parse .mat-files
display('Converting .mat to .png representation...');
for i = 1 : dataset_list_length
  sample_name = dataset_list{1}{i};
  display(sprintf('-----Process sample %s.-----', sample_name));
  
  img_info_name = fullfile(dataset_dir, 'cls', [sample_name, '.mat']);  
  display(sprintf('Information file: %s.', img_info_name));
  try 
    load(img_info_name);    
  catch exception
    display(sprintf('%s.', getReport(exception)));
    continue;
  end
  
  GT = GTcls;
  
  out_img_name = fullfile(output_path, [sample_name, '.png']);
  display(sprintf('Image file: %s.', out_img_name));
  try
    img = SBDImage2VOC(GT);
    imwrite(img, out_img_name);
  catch exception
    display(sprintf('%s.', getReport(exception)));    
  end
  
  out_name = [output_aug_folder_name, '/', sample_name];
  fprintf(dataset_info, '%s %s', ...
      ['/', images_folder_name, '/', sample_name, '.jpg'], ['/', out_name]);
end
display('Converting .mat to .png representation.');
fclose(dataset_info);
display('---------------------------------------------------------');
