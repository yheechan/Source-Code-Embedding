import subprocess
from tqdm import tqdm

from transformers import AutoTokenizer, AutoModel
import torch

def get_projects (path):
	command = f"ls {path}"
	result = subprocess.run(command, shell=True, capture_output=True, text=True)

	if result.returncode == 0:
		file_list = result.stdout.splitlines()
		return file_list
	else:
		print("Error: ", result.stderr)

def get_data (path):
	command = f"cat {path}"
	result = subprocess.run(command, shell=True, capture_output=True, text=True)

	if result.returncode == 0:
		lines = result.stdout.splitlines()
		return lines
	else:
		print("Error: ", result.stderr)

def embed_data (projects, data_list, tokenizer, model, device):
  initial_tensor = torch.empty(0, 768)

  for i in range(len(projects)):
    print("*****["+projects[i]+"]*****")
    for j in tqdm(range(1000)):
      code_tokens = tokenizer.tokenize(data_list[i][j])
      tokens = [tokenizer.cls_token]+code_tokens+[tokenizer.eos_token]
      tokens_ids = tokenizer.convert_tokens_to_ids(tokens)

      if (len(tokens_ids) > 512):
        continue
      
      # Perform gradient checkpointing during the forward pass
      with torch.no_grad():
        context_embeddings = model(torch.tensor(tokens_ids).to(device)[None,:])[0][:,0,:]

      # context_embeddings = model(torch.tensor(tokens_ids).to(device)[None,:])[0][:,0,:]
      initial_tensor = torch.cat((initial_tensor, context_embeddings.cpu()), dim=0)

      # release tensor
      del context_embeddings
      torch.cuda.empty_cache()
    
  return initial_tensor

# ***** get lists of projects *****
data_path = "../data/"
projects = get_projects(data_path)

# ***** get data for each projects *****
data_list = []
for project in projects:
	full_path = data_path + project
	data_list.append( get_data(full_path) )

# ***** bring CodeBert Model *****
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base").to(device) # RobertaModel

# ***** tokenize and embed data *****
embeddings = embed_data(projects, data_list, tokenizer, model, device)