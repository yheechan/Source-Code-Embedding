import subprocess

# FUNCTION TO GET GIT OPEN-SOURCE PROJECTS NAMES FROM PATH
def get_projects (path):
	command = f"ls {path}"
	result = subprocess.run(command, shell=True, capture_output=True, text=True)

	if result.returncode == 0:
		file_list = result.stdout.splitlines()
		return file_list
	else:
		print("Error: ", result.stderr)


# FUNCTION TO GET DATA POINTS FROM PATH
def get_data (path):
	command = f"cat {path}"
	result = subprocess.run(command, shell=True, capture_output=True, text=True)

	if result.returncode == 0:
		lines = result.stdout.splitlines()
		return lines
	else:
		print("Error: ", result.stderr)
