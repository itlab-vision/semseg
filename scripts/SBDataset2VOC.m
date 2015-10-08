% Script for conversion of the Semantic Boundaries Dataset
% http://www.cs.berkeley.edu/~bharath2/codes/SBD/download.html
% to PASCAL VOC format

% This script should be used for training DeepLab models
% on augmented PASCAL VOC 2012 dataset

% function [] = SBDataset2VOC(dataset_dir, output_dir, prefix, prefix1)
% dataset_dir - directory containing the Semantic Boundaries Dataset
% output_dir  - directory to put converted data
% prefix      - which part of dataset to convert ('train' or 'val')
% prefix1     - directory prefix ('cls', 'inst')
function [] = SBDataset2VOC(dataset_dir, output_dir, prefix, prefix1)

output_aug_folder_name = ['SegmentationClass_', prefix, '_aug_', prefix1];
images_folder_name = 'img';
output_path = fullfile(output_dir, output_aug_folder_name);
if (exist(output_path, 'dir') ~= 7)
    mkdir(output_path);
end
dataset_info_name = fullfile(output_dir, [prefix, '_aug_', prefix1,'.txt']);

% read dataset list
display('---------------------------------------------------------');
dataset_list_name = fullfile(dataset_dir, [prefix, '.txt']);
display(sprintf('Reading dataset list %s...\n', dataset_list_name));
dataset_list_fid = fopen(dataset_list_name, 'r');
if (dataset_list_fid == -1)
  display(sprintf('Error: Failed to load a file %s. Aborting.\n', dataset_list_name));
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
  display(sprintf('Error: Failed to create a file %s. Aborting.\n', dataset_info_name));
  exit;
end

% list all samples and parse .mat-files
display('Converting .mat to .png representation...');
for i = 1: dataset_list_length  
  sample_name = dataset_list{1}{i};
  display(sprintf('Process sample %s.\n', sample_name));
  
  img_info_name = fullfile(dataset_dir, prefix1, [sample_name, '.mat']);  
  display(sprintf('Information file: %s.\n', img_info_name));
  try 
    load(img_info_name);    
  catch exception
    display(sprintf('%s.\n', getReport(exception)));
    continue;
  end
  
  if (strcmp(prefix1, 'cls'))
    GT = GTcls;
  else
    GT = GTinst;
  end
    
  out_img_name = fullfile(output_path, [sample_name, '.png']);
  display(sprintf('Image file: %s.\n', out_img_name));
  try
    img = SBDImage2VOC(GT);
    imwrite(img, out_img_name);
  catch exception
    display(sprintf('%s.\n', getReport(exception)));    
  end
  
  out_name = [output_aug_folder_name, '/', sample_name];
  fprintf(dataset_info, '%s %s\n', ['/', images_folder_name, '/', sample_name, '.jpg'], ['/', out_name]);
end
display('Converting .mat to .png representation.');
fclose(dataset_info);
display('---------------------------------------------------------');
