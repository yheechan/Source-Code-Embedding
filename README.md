# Source-Code-Embedding

This is a project (in-process) that clusters code snippets for analyzing source code.
* We leverage [CodeBERT](https://github.com/microsoft/CodeBERT), a Pre-Trained Model for Programming and Natural Language ([paper](https://arxiv.org/pdf/2002.08155.pdf)), to embedd given source code snippet.
* We leverage [UMAP](https://umap-learn.readthedocs.io/en/latest/) to reduce dimensions of resulting embeddings
* We leverage [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.htmlh) to form a cluster of given source code snippets
