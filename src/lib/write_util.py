import os

def create_directory(directory_path):
	if not os.path.exists(directory_path):
		os.makedirs(directory_path)
		print(f"Directory created: {directory_path}")
	else:
		print(f"Directory already exists: {directory_path}")

def write_results(topic_sizes, top_n_words,
					n_neighbors,
					n_components,
					min_dist,
					min_cluster_size,
					min_samples,
					research_title):

	dir = '../results/'
	create_directory(dir)

	fn = research_title

	with open(dir + fn, 'w') as f:
		f.write('n_neighbors: ' + str(n_neighbors) + '\n')
		f.write('n_components: ' + str(n_components) + '\n')
		f.write('min_dist: ' + str(min_dist) + '\n\n')
		f.write('min_cluster_sizes: ' + str(min_cluster_size) + '\n')
		f.write('min_samples: ' + str(min_samples) + '\n\n')

		total = str(topic_sizes['Size'].sum())
		nonCluster = str(topic_sizes['Size'][0])
		cluster_n = str(len(topic_sizes))

		f.write('total number of cluster: ' + cluster_n + '\n')
		f.write('not in cluster: ' + nonCluster + '/' + total + '\n\n')
		f.write('top 5 cluster')

		cnt = 0
		for i, row in topic_sizes.iterrows():
			f.write('\n')
			topic_num = row['Topic']
			topic_size = row['Size']

			if topic_num == -1: continue

			f.write('cluster #' + str(topic_num) + '\n')
			f.write('cluster size: ' + str(topic_size) + '\n')

			for word in top_n_words[topic_num][:10]:
				f.write(str(word) + '\n')
			f.write('\n')

			if cnt == 10: break
			cnt += 1

			f.write('\n')
