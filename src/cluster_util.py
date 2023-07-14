import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


# PROCESS CLASS-TF-IDF
def c_tf_idf(documents, m, ngram_range=(1, 1)):
	# count is CountVectorizer object
	count = CountVectorizer(ngram_range=ngram_range, stop_words=None).fit(documents)

	t = count.transform(documents).toarray()
	w = t.sum(axis=1)
	tf = np.divide(t.T, w)
	sum_t = t.sum(axis=0)
	idf = np.log(np.divide(m, sum_t)).reshape(-1, 1)
	tf_idf = np.multiply(tf, idf)

	return tf_idf, count


# EXTRACT TOP N WORDS PER TOPIC
# count is CountVectorizer object
def extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=20):
	words = count.get_feature_names_out()
	labels = list(docs_per_topic.Topic)
	tf_idf_transposed = tf_idf.T
	indices = tf_idf_transposed.argsort()[:, -n:]
	top_n_words = {label: [(words[j], tf_idf_transposed[i][j]) for j in indices[i]][::-1] for i, label in enumerate(labels)}

	return top_n_words


# RETURN TOPIC SIZES IN SORTED ORDER
def extract_topic_sizes(df):
	topic_sizes = (df.groupby(['Topic']).Doc.count().reset_index().rename({"Topic": "Topic", "Doc": "Size"}, axis='columns').sort_values("Size", ascending=False))
	
	return topic_sizes



# =====================================================================
# =====================================================================
# =====================================================================
import warnings
warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")

import umap

import hdbscan
from hdbscan.flat import (HDBSCAN_flat, approximate_predict_flat, membership_vector_flat, all_points_membership_vectors_flat)

import matplotlib.pyplot as plt
import pandas as pd


# embeddings: data embedded to vector values with codeBERT model
# data_list: original data points
def cluster(embeddings, data_list, n_neighbors, n_components, min_dist, min_cluster_size, min_samples, title):

	# REDUCE EMBEDDING DIMENSIONS using UMAP
	umap_embeddings = umap.UMAP(n_neighbors=n_neighbors, n_components=n_components, min_dist=min_dist, metric='cosine').fit_transform(embeddings)
	print('\nDONE REDUCING DIMENSIONS USING UMAP.')


	# CLUSTER EMBEDDINGS using HDBSCAN
	cluster = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, cluster_selection_epsilon=0.0, metric='euclidean', cluster_selection_method='eom').fit(umap_embeddings)
	
	# cluster = HDBSCAN_flat(umap_embeddings, cluster_selection_method='eom', n_clusters=20, min_cluster_size=min_cluster_size)

	print('\nDONE FORMING CLUSTER USING HDBSCAN.')
	

	# REDUCE DATA TO 2-dimension FOR PLOT
	umap_data = umap.UMAP(n_neighbors=n_neighbors, n_components=2, min_dist=min_dist, metric='cosine').fit_transform(embeddings)
	result = pd.DataFrame(umap_data, columns=['x', 'y'])

	# LABEL USING CLUSTERS FORMED FROM HDBSCAN
	result['labels'] = cluster.labels_


	# VISUALIZE CLUSTERS
	fig, ax = plt.subplots(figsize=(20, 10))
	outliers = result.loc[result.labels == -1, :]
	clustered = result.loc[result.labels != -1, :]
	plt.scatter(outliers.x, outliers.y, color='#BDBDBD', s=0.05)
	plt.scatter(clustered.x, clustered.y, c=clustered.labels, s=0.05, cmap='hsv_r')
	plt.colorbar()
	plt.show()

	print('\nDONE WITH 2D PLOT PLOT USING MATPLOTLIB')


	# process class based tf-idf
	docs_df = pd.DataFrame(data_list, columns=["Doc"])
	docs_df['Topic'] = cluster.labels_
	docs_df['Doc_ID'] = range(len(docs_df))
	docs_per_topic = docs_df.groupby(['Topic'], as_index=False).agg({'Doc': ' '.join})


	tf_idf, count = c_tf_idf(docs_per_topic.Doc.values, m=len(data_list))


	top_n_words = extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=20)
	topic_sizes = extract_topic_sizes(docs_df)

	print(topic_sizes.head(10))
	print(len(topic_sizes))

	cnt = 0
	for i, row in topic_sizes.iterrows():
		topic_num = row['Topic']
		topic_size = row['Size']

		# topic_num with -1 are the outlier cluster
		if topic_num == -1: continue

		print(topic_size, top_n_words[topic_num][:10])

		# show top 10 cluster with mose data points
		if cnt == 10: break
		cnt += 1
	
	return docs_per_topic, top_n_words, topic_sizes
