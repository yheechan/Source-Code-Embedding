from tqdm import tqdm

from transformers import AutoTokenizer, AutoModel
import torch

# FUNCTION TO EMBED GIVEN DATA
def embed_data (projects, data_list, data_num):
	# BRING CODEBERT MODEL
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
	model = AutoModel.from_pretrained("microsoft/codebert-base").to(device) # RobertaModel

	# EMBED GIVEN DATA
	initial_tensor = torch.empty(0, 768)
	inital_list = []

	for i in range(len(projects)):
		print("*****["+projects[i]+"]*****")
	
		for j in tqdm(range(data_num)):
			code_tokens = tokenizer.tokenize(data_list[i][j])
			tokens = [tokenizer.cls_token]+code_tokens+[tokenizer.eos_token]
			tokens_ids = tokenizer.convert_tokens_to_ids(tokens)
			
			if (len(tokens_ids) > 511):	continue

			# Perform gradient checkpointing during the forward pass
			with torch.no_grad():
				context_embeddings = model(torch.tensor(tokens_ids).to(device)[None,:])[0][:,0,:]

			# context_embeddings = model(torch.tensor(tokens_ids).to(device)[None,:])[0][:,0,:]
			initial_tensor = torch.cat((initial_tensor, context_embeddings.cpu()), dim=0)
			inital_list.append(data_list[i][j])

			# release tensor
			del context_embeddings
			torch.cuda.empty_cache()
	
	return initial_tensor, inital_list
