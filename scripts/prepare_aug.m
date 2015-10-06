#Script for segmentation data extraction

dataset_dir = "C:/Programming/CProjects/nnsu/datasets/benchmark_RELEASE/dataset";
dataset_info_dir = "/inst";
dataset_list_name = [dataset_dir, "/val.txt"];

  output_path = "/SegmentationValAug_inst";
dataset_info_name = [dataset_dir, "/val_aug_inst.txt"];




dataset_list_fid = fopen(dataset_list_name, "r");

if (dataset_list_fid == -1)
  printf("Error: Failed to load a file '%s'. Aborting.\n", dataset_list_name);
  exit;
endif

dataset_list = textscan(dataset_list_fid, "%s");

fclose(dataset_list_fid);

dataset_list_length = length(dataset_list{1});
printf("Entries count: %d\n", dataset_list_length);

dataset_info = fopen(dataset_info_name, "w+");
if (dataset_info_name == -1)
  printf("Error: Failed to create a file '%s'. Aborting.\n", dataset_info_name);
  exit;
endif

output_dir = [dataset_dir, output_path];

for i = 1: dataset_list_length
  sample_name = dataset_list{1}{i};
  img_info_name = [dataset_dir, dataset_info_dir, "/", sample_name, ".mat"];
  try 
    load(img_info_name);
  catch
    printf("Error: File '%s' not found. Skipping.\n", img_info_name);
    continue;
  end_try_catch
  
  img = GTinst.Segmentation;
    
  try
    out_img_name = [output_dir, "/", sample_name, ".png"];
    imwrite(img, out_img_name);
    #printf("Image created successfully: '%s'.\n", out_img_name);
  catch
    printf("Error: Failed to write image '%s'\n", out_img_name);
  end_try_catch
  
  out_name = [output_path, "/", sample_name];   
  fprintf(dataset_info, "%s %s\n", sample_name, out_name);
endfor

fclose(dataset_info);

printf("Operation completed successfully!\n");