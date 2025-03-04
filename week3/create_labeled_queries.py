import os
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import csv
import re

# Useful if you want to perform stemming.
import nltk

stemmer = nltk.stem.PorterStemmer()


def normalize_query(query):
    # convert to lower case
    query = query.lower()

    # replace number with space
    query = re.sub(r'[^a-z0-9]', ' ', query)

    # remove one or more space with one space
    query = re.sub(r'\s+', ' ', query)

    # split each word by space -> get stem of word -> join by space
    query = ' '.join([stemmer.stem(part) for part in query.split(' ')])
    return query


# print(normalize_query('Beats By Dr. Dre- Monster Pro Over-the-Ear Headphones -'))

categories_file_name = r'/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

queries_file_name = r'/workspace/datasets/train.csv'
output_file_name = r'/workspace/datasets/fasttext/labeled_queries.txt'

parser = argparse.ArgumentParser(description='Process arguments.')
general = parser.add_argument_group("general")
general.add_argument("--min_queries", default=1, help="The minimum number of queries per category label (default is 1)")
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
output_file_name = args.output

if args.min_queries:
    min_queries = int(args.min_queries)


def roll_up_categories(q_df, parent_cat_dict: dict):
    category_query_count_df = q_df.groupby(['category']).size().reset_index(name='count')
    unqualified_cat_df = category_query_count_df.query('count < @min_queries')
    unqualified_cat_set = set(unqualified_cat_df['category'].values)
    if len(unqualified_cat_df) == 0:
        return q_df

    q_df['category'] = q_df['category'].apply(
        lambda cat: parent_cat_dict[cat] if cat in unqualified_cat_set and cat in parent_cat_dict else cat)
    return roll_up_categories(q_df, parent_cat_dict)


# The root category, named Best Buy with id cat00000, doesn't have a parent.
root_category_id = 'cat00000'

tree = ET.parse(categories_file_name)
root = tree.getroot()

# Parse the category XML file to map each category id to its parent category id in a dataframe.
categories = []
parents = []
for child in root:
    id = child.find('id').text
    cat_path = child.find('path')
    cat_path_ids = [cat.find('id').text for cat in cat_path]
    leaf_id = cat_path_ids[-1]
    if leaf_id != root_category_id:
        categories.append(leaf_id)
        parents.append(cat_path_ids[-2])
parents_df = pd.DataFrame(list(zip(categories, parents)), columns=['category', 'parent'])

# Read the training data into pandas, only keeping queries with non-root categories in our category tree.
queries_df = pd.read_csv(queries_file_name)[['category', 'query']]
queries_df = queries_df[queries_df['category'].isin(categories)]

# IMPLEMENT ME: Convert queries to lowercase, and optionally implement other normalization, like stemming.
queries_df['query'] = queries_df['query'].apply(lambda query: normalize_query(query))

# IMPLEMENT ME: Roll up categories to ancestors to satisfy the minimum number of queries per category.
print("roll up start")
parent_cat_dict = dict(zip(parents_df.category, parents_df.parent))
roll_up_categories(queries_df, parent_cat_dict)

# Create labels in fastText format.
queries_df['label'] = '__label__' + queries_df['category']

# Output labeled query data as a space-separated file, making sure that every category is in the taxonomy.
queries_df = queries_df[queries_df['category'].isin(categories)]
queries_df['output'] = queries_df['label'] + ' ' + queries_df['query']
queries_df[['output']].to_csv(output_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE,
                              index=False)
