# Source-Code-Embedding

## General Info
This is a project (in-process) forms clusters for given code snippet data for source code analyzing using LLM model, [CodeBERT](https://github.com/microsoft/CodeBERT).

* We leverage [CodeBERT](https://github.com/microsoft/CodeBERT), a Pre-Trained Model for Programming and Natural Language ([paper](https://arxiv.org/pdf/2002.08155.pdf)), to embed given source code snippet.
* We leverage [UMAP](https://umap-learn.readthedocs.io/en/latest/) to reduce dimensions of resulting embeddings
* We leverage [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.htmlh) to form a cluster of given source code snippets

## Dependency
* Python library dependencies can be found at [requirements.txt](https://github.com/yheechan/Source-Code-Embedding/blob/master/docs/dependency.txt).
```
$ pip install -r requirements.txt
```

## Run Program
1. run ```$ ./clone_cmd.sh``` to clone all 10 open-source github projects. (found in ```./src/init_data/```)
2. run ```$ python3 make_data.py``` to make data from all open-source projects of only c and c++ code files.(found in ```./src/init_data/```)
```
usage: make_data.py [-h] [--num NUM]

optional arguments:
  -h, --help  show this help message and exit
  --num NUM   Enter the number of data for each project.
```
3. run ```$ python3 main.py``` to execute the main program of the project to embed and cluster given code snippet data. (found in ```./src/```)
```
EXAMPLE COMMAND:
$ python3 main.py --data_num 5000 --n_neighbors 10 --n_components 256 --min_dist 0.0 --min_cluster_size 5 --min_samples 5 --research_title test-01
```
```
usage: main.py [-h] [--data_num DATA_NUM] [--n_neighbors N_NEIGHBORS] [--n_components N_COMPONENTS]
               [--min_dist MIN_DIST] [--min_cluster_size MIN_CLUSTER_SIZE] [--min_samples MIN_SAMPLES]
               --research_title RESEARCH_TITLE

optional arguments:
  -h, --help            show this help message and exit
  --data_num DATA_NUM   Enter the number of data point to use for each project. Default=5000
  --n_neighbors N_NEIGHBORS
                        [UMAP] Number of approximate nearest neighbors used to construct the initial high-
                        dimensional graph. Default=10
  --n_components N_COMPONENTS
                        [UMAP] Number of dimension to reduce to. Default=256
  --min_dist MIN_DIST   [UMAP] Minimum distance between point in low-dimensional space. Default=0.0
  --min_cluster_size MIN_CLUSTER_SIZE
                        [HDBSCAN] Minimum size a cluster must contain. Default=5
  --min_samples MIN_SAMPLES
                        [HDBSCAN] The minimum number of points required to form a dense region (core
                        points). Default=5
  --research_title RESEARCH_TITLE
                        The name of the research subject. (ex: test-01)
```

## Results
Results can be seen in ```./results/``` directory.
