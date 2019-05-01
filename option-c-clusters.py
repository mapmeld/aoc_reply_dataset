# word2vec and k-means clustering
# based strongly on https://medium.com/ml2vec/using-word2vec-to-analyze-reddit-comments-28945d8cee57
# pip install psycopg2 nltk gensim sklearn pandas numpy

import psycopg2
import nltk.data
from gensim.models import word2vec
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree
import pandas as pd
import numpy as np
import re
import multiprocessing

# postgresql
conn = psycopg2.connect("dbname='tweetreplies'")
cur = conn.cursor()

# nltk download
nltk.download('punkt')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def clean_text(all_comments, out_name):

    out_file = open(out_name, 'w')
    total_rows = len(all_comments)

    for pos in range(1, total_rows):

        #Get the comment
        val = all_comments[pos][0]

        #Normalize tabs and remove newlines
        no_tabs = str(val).replace('\t', ' ').replace('\n', '')

        #Remove all characters except A-Z and a dot.
        alphas_only = re.sub("[^a-zA-Z\.]", " ", no_tabs)

        #Normalize spaces to 1
        multi_spaces = re.sub(" +", " ", alphas_only)

        #Strip trailing and leading spaces
        no_spaces = multi_spaces.strip()

        #Normalize all charachters to lowercase
        clean_text = no_spaces.lower()

        #Get sentences from the tokenizer, remove the dot in each.
        sentences = tokenizer.tokenize(clean_text)
        sentences = [re.sub("[\.]", "", sentence) for sentence in sentences]

        #If the text has more than one space (removing single word comments) and one character, write it to the file.
        if len(clean_text) > 0 and clean_text.count(' ') > 0:
            for sentence in sentences:
                out_file.write("%s\n" % sentence)
                #print(sentence)

        #Simple logging. At every 50000th step,
        #print the total number of rows processed and time taken so far, and flush the file.
        if pos % 50000 == 0:
            print('Completed ' + str(round(100 * (pos / total_rows), 2)) + '% - ' + str(pos) + ' rows\r')
            #out_file.flush()
            #break

    out_file.close()

cur.execute('SELECT body FROM replies')
sql_data = cur.fetchall()
clean_comments = clean_text(sql_data, './out_full')

######

# Set values for various parameters
num_features = 100    # Dimensionality of the hidden layer representation
min_word_count = 40   # Minimum word count to keep a word in the vocabulary
num_workers = multiprocessing.cpu_count()       # Number of threads to run in parallel set to total number of cpus.
context = 5          # Context window size (on each side)
downsampling = 1e-3   # Downsample setting for frequent words
# Initialize and train the model.
#The LineSentence object allows us to pass in a file name directly as input to Word2Vec,
#instead of having to read it into memory first.
print("Training model...")
model = word2vec.Word2Vec(word2vec.LineSentence('./out_full'), workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)
# We don't plan on training the model any further, so calling
# init_sims will make the model more memory efficient by normalizing the vectors in-place.
model.init_sims(replace=True)
# Save the model
model_name = "model_full_twitter"
model.save(model_name)


Z = model.wv.vectors
print(Z[0].shape)

def clustering_on_wordvecs(word_vectors, num_clusters):
    # Initalize a k-means object and use it to extract centroids
    kmeans_clustering = KMeans(n_clusters = num_clusters, init='k-means++')
    idx = kmeans_clustering.fit_predict(word_vectors)

    return kmeans_clustering.cluster_centers_, idx

centers, clusters = clustering_on_wordvecs(Z, 50)
centroid_map = dict(zip(model.wv.index2word, clusters))

def get_top_words(index2word, k, centers, wordvecs):
    tree = KDTree(wordvecs)
#Closest points for each Cluster center is used to query the closest 20 points to it.
    closest_points = [tree.query(np.reshape(x, (1, -1)), k=k) for x in centers]
    closest_words_idxs = [x[1] for x in closest_points]
#Word Index is queried for each position in the above array, and added to a Dictionary.
    closest_words = {}
    for i in range(0, len(closest_words_idxs)):
        closest_words['Cluster #' + str(i)] = [index2word[j] for j in closest_words_idxs[i][0]]
#A DataFrame is generated from the dictionary.
    print(closest_words)
    df = pd.DataFrame(closest_words)
    df.index = df.index + 1
    return df

top_words = get_top_words(model.wv.index2word, 50, centers, Z)
#print(top_words)
