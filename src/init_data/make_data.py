import os
import argparse
import subprocess
import random
from tqdm import tqdm
import time
import json

# function for counting number of lines of a file given its path
def count_lines(file_path):
	command = f"wc -l {file_path}"
	output = subprocess.check_output(command, shell=True).decode().strip()
	line_count = int(output.split()[0])
	return line_count

def create_directory(directory_path):
	if not os.path.exists(directory_path):
		os.makedirs(directory_path)
		print(f"Directory created: {directory_path}")

# make data from git project
def make_from_git(data_num, data_dir):
  # Define the directory to search in
  directory = "../../git_projects/"

  # Define the find command to search for .c and .cpp files
  find_command = f"find {directory} -type f \( -name '*.c' -o -name '*.cpp' \)"

  # Execute the find command using subprocess and get the output
  find_process = subprocess.Popen(find_command, shell=True, stdout=subprocess.PIPE)
  find_output, _ = find_process.communicate()

  # Decode the output and split it into individual file paths
  file_paths = find_output.decode().splitlines()

  info_dict = {}

  # Read the content of each file
  for file_path in file_paths:
    project_nm = file_path.split('/')[3]
    max_lines = count_lines(file_path)

    if project_nm not in info_dict:
      info_dict[project_nm] = []
    
    info_dict[project_nm].append((file_path, max_lines))

  projects = list(info_dict.keys())

  # for each project
  # make 1000 data
  # from random c or cpp source code of that project
  # containing random 4~8 lines

  data_path = "../../data/"
  create_directory(data_path)
  data_path += data_dir+'/'
  create_directory(data_path)

  for project in projects:
    num_of_files = len(info_dict[project])
    full_data_path = data_path + project
    

    print("*****["+project+"]*****")
    for i in tqdm(range(data_num)):
      
      while 1:
        file_idx = random.randint(0, num_of_files-1)
        file_path, file_max_line = info_dict[project][file_idx]
        number_of_lines = random.randint(4, 8)

        if 1 > file_max_line-number_of_lines:
          continue

        start_line_num = random.randint(1, file_max_line-number_of_lines)
        end_line_num = start_line_num+number_of_lines
        break

      # head_command = f"head -n {end_line_num} {file_path} | tail -n +{start_line_num}"
      sed_command = f"sed -n '{start_line_num},{end_line_num}p' {file_path} | tr '\n' ' '"
      output_str = subprocess.check_output(sed_command, shell=True).decode().strip()

      output = output_str.replace("\n", "").replace("\t", "").replace("\0", "").replace("\r", "").replace("\f", "")

      if not os.path.exists(full_data_path):
        with open(full_data_path, 'w') as file:
          file.write(output)
      else:
        with open(full_data_path, 'a') as file:
          file.write("\n"+output)

# make data from json target file
def make_from_json(data_dir, json_fn):
	data_path = "../../data/"
	create_directory(data_path)
	data_path += data_dir+'/'
	create_directory(data_path)

	fn = json_fn.split(".")[0]
	full_data_path = data_path + fn

	with open('../../json/'+json_fn, "r") as fp:
		data = json.load(fp)
	
	for i in range(len(data)):
		output = data[i]["before-code"].replace("\n", "").replace("\t", "").replace("\0", "").replace("\r", "").replace("\f", "")

		if not os.path.exists(full_data_path):
			with open(full_data_path, 'w') as fp2:
				fp2.write(output)
		else:
			with open(full_data_path, 'a') as fp2:
				fp2.write("\n"+output)

if __name__ == '__main__':
  # create ArgumentParser object
  parser = argparse.ArgumentParser()

  # Add an argument to the parser
  parser.add_argument("--num",
  						type=int,
						default=1000,
						help="Enter the number of data for each project.")
  
  parser.add_argument("--data_directory",
  						required=True,
						help='The name of the directory to contain all the data file')
  
  parser.add_argument("--from_json",
						default=False,
						help='Boolean flag whether to make data from json directory or open-source directory (ex: True)')

  parser.add_argument("--target_file",
  						help='The name of the target json file to make data')

  # Parser the command-line argument
  args = parser.parse_args()

  data_num = int(args.num)
  data_dir = str(args.data_directory)
  from_json = bool(args.from_json)

  if from_json == False:
  	make_from_git(data_num, data_dir)
  else:
  	json_fn = str(args.target_file)
  	make_from_json(data_dir, json_fn)
