import argparse
import pprint

# MY UTIL LIBRARY
import lib.data_util as data_util
import lib.codeBERT_util as codeBERT_util
import lib.cluster_util as cluster_util
import lib.write_util as write_util


def define_argparser():
	# create ArgumentParser object
	p = argparse.ArgumentParser()

	# Add arguments to the parser
	p.add_argument(
		'--data_num',
		type=int,
		default=5000,
		help='Enter the number of data point to use for each project. Default=%(default)s'
	)

	p.add_argument(
		'--n_neighbors',
		type=int,
		default=10,
		help='[UMAP] Number of approximate nearest neighbors used to construct the initial high-dimensional graph. Default=%(default)s'
	)

	p.add_argument(
		'--n_components',
		type=int,
		default=256,
		help='[UMAP] Number of dimension to reduce to. Default=%(default)s'
	)

	p.add_argument(
		'--min_dist',
		type=float,
		default=0.0,
		help='[UMAP] Minimum distance between point in low-dimensional space. Default=%(default)s'
	)

	p.add_argument(
		'--min_cluster_size',
		type=int,
		default=5,
		help='[HDBSCAN] Minimum size a cluster must contain. Default=%(default)s'
	)

	p.add_argument(
		'--min_samples',
		type=int,
		default=5,
		help='[HDBSCAN] The minimum number of points required to form a dense region (core points). Default=%(default)s'
	)

	p.add_argument(
		'--research_title',
		required=True,
		help='The name of the research subject. (ex: test-01)'
	)

	config = p.parse_args()

	return config


def main(config):
	
	# PRINT CONFIG HELP
	def print_config(config):
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(vars(config))
	print_config(config)

	# GET LISTS OF PROJECTS
	data_path = "../data/"
	projects = data_util.get_projects(data_path)


	# GET DATA FOR EACH PROJECTS
	data_list = []
	for project in projects:
		full_path = data_path + project
		data_list.append(data_util.get_data(full_path))
	

	# ***** tokenize and embed data *****
	embeddings, data_list = codeBERT_util.embed_data(projects, data_list, config.data_num)


	# docs_per_topic: each data labeled to a cluster (topic)
	# top_n_words: dataframe of datapoint with top n words sorted (according to c-tf-idf)
	# topic_sizes: topic sizes in order of cluster with most datapoints
	docs_per_topic, top_n_words, topic_sizes = cluster_util.cluster(
		embeddings.numpy(),
		data_list,
		config.n_neighbors,
		config.n_components,
		config.min_dist,
		config.min_cluster_size,
		config.min_samples,
		config.research_title
	)

	write_util.write_results(topic_sizes, top_n_words,
		config.n_neighbors,
		config.n_components,
		config.min_dist,
		config.min_cluster_size,
		config.min_samples,
		config.research_title
	)


if __name__ == '__main__':
	config = define_argparser()
	main(config)
