import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans

w = open('cleaned_tweets_sanilk2.txt', 'w')
tweets_dict = {}
# an array of stop words, these will be removed from the tweets.
stopwords = ['a', 'an', 'another', 'any', 'certain', 'each', 'every', 'her', 'his', 'i', 'its', 'its', 'my', '"no',
             'our', 'some', 'that', 'the', 'their', 'this', 'and', 'but', 'or', 'yet', 'for', 'nor', 'so', 'as',
             'aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'around', 'at', 'before', 'behind',
             'below', 'beneath', 'beside', 'between', 'beyond', 'but', 'by', 'down', 'during', 'except', 'following',
             'for', 'from', 'in', 'inside', 'into', 'like', 'minus', 'near', 'next', 'of', 'off', 'on',
             'onto', 'opposite', 'out', 'outside', 'over', 'past', 'plus', 'round', 'since', 'than', 'through', 'to',
             'toward', 'under', 'underneath', 'unlike', 'until', 'up', 'upon', 'with', 'without']

# every tweet is preprocessed to remove stop words and other punctuations. Also I am removing URL's, @ mentions,
# #hastags, html elements, extra
# spaces, etc. The final processed tweets are written into cleaned_tweets_sanilk2.txt


def preprocess(cur_tweet):
    cur_tweet = cur_tweet.lower().strip()
    cur_tweet = re.sub(r'@[^\s]+', '', cur_tweet).strip()
    cur_tweet = re.sub(r'\#+[\w_]+[\w\'_\-]*[\w_]+', '', cur_tweet).strip()
    cur_tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', '', cur_tweet).strip()
    cur_tweet = re.sub(r'<[^>]+>', '', cur_tweet).strip()
    cur_tweet = re.sub(r'[\s]+', ' ', cur_tweet).strip()
    processed_tweet = []
    words = re.findall(r'[\w]+', cur_tweet)
    for word in words:
        if word not in stopwords:
            processed_tweet.append(word)

    final_tweet = " ".join(word for word in processed_tweet).strip()
    if not final_tweet.strip():
        return
    w.write(final_tweet + "\n")


with open('search_output_sanilk2.txt') as f:
    for tweet in f:
        if not tweet.strip():
            continue
        preprocess(tweet)


w.close()

tweets = []
u = open('unique_tweets_sanilk2.txt','w')
with open('cleaned_tweets_sanilk2.txt') as f:
    for line in f:
        if line not in tweets:
            tweets.append(line)
            u.write(line)

u.close()

tweets = []
i = 0
with open('unique_tweets_sanilk2.txt') as f:
    for line in f:
        tweets.append(line.strip())
        tweets_dict[i] = line.strip()
        i += 1

########### Query ##################
query_to_search = ['megyn kelly hillary trump']
####################################


print("\n\n######## TF-IDF Vectorizer ##########\n\n")

# tf_idf_vectorizer for docs
vectorizer_idf_docs = TfidfVectorizer(min_df=0.2, max_df=0.8, lowercase=True, norm='l2', smooth_idf=True,
                                      sublinear_tf=False, analyzer='word', stop_words=['english', 'rt'], use_idf=True)
tf_idf_vectorizer = vectorizer_idf_docs.fit_transform(tweets)
vectors_idf_docs = tf_idf_vectorizer.toarray()

# tf_idf_vectorizer for query
tf_idf_query = vectorizer_idf_docs.transform(query_to_search)
vectors_idf_query = tf_idf_query.toarray()

query_doc_dict_tf_idf = {}

i = 0
for doc_vectors in vectors_idf_docs:
    doc_vectors = doc_vectors.reshape(1, -1)
    tf_idf_similarity = cosine_similarity(doc_vectors, vectors_idf_query)
    query_doc_dict_tf_idf[i] = tf_idf_similarity[0][0]
    i += 1

query_doc_dict_tf_idf = sorted(query_doc_dict_tf_idf, key=query_doc_dict_tf_idf.get, reverse=True)
for i in range(0, 10):
    print(query_doc_dict_tf_idf[i], tweets_dict[i])

print("\n\n######## Count Vectorizer ##########\n\n")

# count vectorizer for docs
vectorizer_count_docs = CountVectorizer(min_df=0.2, max_df=0.8, lowercase=True, analyzer='word',
                                        stop_words=['english', 'rt'])
count_vectorizer = vectorizer_count_docs.fit_transform(tweets)
vectors_count_docs = count_vectorizer.toarray()

# count vecroizer for query
count_query = vectorizer_count_docs.transform(query_to_search)
vectors_count_query = count_query.toarray()

query_doc_dict_count = {}

i = 0
for doc_vectors in vectors_count_docs:
    doc_vectors = doc_vectors.reshape(1, -1)
    count_similarity = cosine_similarity(doc_vectors, vectors_count_query)
    query_doc_dict_count[i] = count_similarity[0][0]
    i += 1

query_doc_dict_count = sorted(query_doc_dict_count, key=query_doc_dict_count.get, reverse=True)
for i in range(0, 10):
    print(query_doc_dict_count[i], tweets_dict[i])

print("\n\n######## Hashing Vectorizer ##########\n\n")

# hashing vectorizer for docs
vectorizer_hashing_docs = HashingVectorizer(norm='l2', lowercase=True, analyzer='word', stop_words=['english', 'rt'],
                                            non_negative=True)
hashing_vectorizer = vectorizer_hashing_docs.transform(tweets)
vectors_hash_docs = hashing_vectorizer.toarray()

# hashing vecroizer for query
hash_query = vectorizer_hashing_docs.transform(query_to_search)
vectors_hash_query = hash_query.toarray()

query_doc_dict_hash = {}

i = 0
for doc_vectors in vectors_hash_docs:
    doc_vectors = doc_vectors.reshape(1, -1)
    hash_similarity = cosine_similarity(doc_vectors, vectors_hash_query)
    query_doc_dict_hash[i] = hash_similarity[0][0]
    i += 1

query_doc_dict_hash = sorted(query_doc_dict_hash, key=query_doc_dict_hash.get, reverse=True)
for i in range(0, 10):
    print(query_doc_dict_hash[i], tweets_dict[i])

print("\n\n########## TF-IDF Vectorizer Clustering (Does Word ckustering rather than Tweets)################\n\n")
vectorizer_idf_docs = TfidfVectorizer(lowercase=True, norm='l2', smooth_idf=True,
                                      sublinear_tf=False, analyzer='word', stop_words=['english', 'rt'],
                                      max_features=6, use_idf=True)
X = vectorizer_idf_docs.fit_transform(tweets)
print("Clustering Shape: ", X.shape)

svd = TruncatedSVD(5)
normalizer = Normalizer(copy=False)
lsa = make_pipeline(svd, normalizer)

X = lsa.fit_transform(X.toarray())
km = KMeans(n_clusters=5, init='k-means++', max_iter=100, n_init=1)
km.fit(X)

centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer_idf_docs.get_feature_names()
for i in range(5):
    print("Cluster %d:" % i, end='')
    for ind in centroids[i, :10]:
        print(' %s' % terms[ind], end='')
    print("\n")


print("\n\n########## TF-IDF Vectorizer Clustering (Tweets clustering)################\n\n")
vectorizer_idf_docs = TfidfVectorizer(min_df=0.2, max_df=0.8, lowercase=True, norm='l2', smooth_idf=True,
                                      sublinear_tf=False, analyzer='word', stop_words=['english', 'rt'], use_idf=True)
tf_idf_vectorizer = vectorizer_idf_docs.fit_transform(tweets)
vectors_idf_docs = tf_idf_vectorizer.toarray()

cluster_tf_idf = {}

doc_vectors = [vector for vector in vectors_idf_docs]
tweet_doc = {}

for i in range(0, 5):
    print("Top tweets similar to tweet : ", tweets_dict[i])
    vectorizer_idf_doc = doc_vectors[i]
    vectorizer_idf_doc = vectorizer_idf_doc.reshape(1, -1)
    tf_idf_similarity = cosine_similarity(vectorizer_idf_doc, vectors_idf_docs)
    cluster_similarity = tf_idf_similarity[0]

    for index in range(len(tweets_dict)):
        value = cluster_similarity[index]
        if value != 1:
            if value not in tweet_doc:
                tweet_doc[value] = tweets_dict[index]

    cluster_similarity = sorted(cluster_similarity, reverse=True)
    i = 0
    value_dict = []

    for value in cluster_similarity:
        if i >= 5:
            break

        if value != 1:
            if value not in value_dict:
                if str(tweet_doc[value]).strip():
                    value_dict.append(value)
                    i += 1
                    print(tweet_doc[value])

    print("\n\n")


print("\n\n################## Bonus Points - Trigrams ################\n\n")
print("\n\n######## TF-IDF Vectorizer - Trigrams ##########\n\n")

# tf_idf_vectorizer for docs
vectorizer_idf_docs = TfidfVectorizer(min_df=0.2, max_df=0.8, lowercase=True, norm='l2', ngram_range=(1, 3),
                                      smooth_idf=True, sublinear_tf=False, analyzer='word', stop_words=['english', 'rt'],
                                      use_idf=True)
tf_idf_vectorizer = vectorizer_idf_docs.fit_transform(tweets)
vectors_idf_docs = tf_idf_vectorizer.toarray()

# tf_idf_vectorizer for query
tf_idf_query = vectorizer_idf_docs.transform(query_to_search)
vectors_idf_query = tf_idf_query.toarray()

query_doc_dict_tf_idf = {}

i = 0
for doc_vectors in vectors_idf_docs:
    doc_vectors = doc_vectors.reshape(1, -1)
    tf_idf_similarity = cosine_similarity(doc_vectors, vectors_idf_query)
    query_doc_dict_tf_idf[i] = tf_idf_similarity[0][0]
    i += 1

query_doc_dict_tf_idf = sorted(query_doc_dict_tf_idf, key=query_doc_dict_tf_idf.get, reverse=True)
for i in range(0, 10):
    print(query_doc_dict_tf_idf[i], tweets_dict[i])

print("\n\n######## Count Vectorizer - Trigrams ##########\n\n")

# count vectorizer for docs
vectorizer_count_docs = CountVectorizer(min_df=0.2, max_df=0.8, lowercase=True, analyzer='word', ngram_range=(1, 3),
                                        stop_words=['english', 'rt'])
count_vectorizer = vectorizer_count_docs.fit_transform(tweets)
vectors_count_docs = count_vectorizer.toarray()

# count vecroizer for query
count_query = vectorizer_count_docs.transform(query_to_search)
vectors_count_query = count_query.toarray()

query_doc_dict_count = {}

i = 0
for doc_vectors in vectors_count_docs:
    doc_vectors = doc_vectors.reshape(1, -1)
    count_similarity = cosine_similarity(doc_vectors, vectors_count_query)
    query_doc_dict_count[i] = count_similarity[0][0]
    i += 1

query_doc_dict_count = sorted(query_doc_dict_count, key=query_doc_dict_count.get, reverse=True)
for i in range(0, 10):
    print(query_doc_dict_count[i], tweets_dict[i])

print("\n\n######## Hashing Vectorizer - Trigrams ##########\n\n")

# hashing vectorizer for docs
vectorizer_hashing_docs = HashingVectorizer(norm='l2', lowercase=True, analyzer='word', ngram_range=(1, 3),
                                            stop_words=['english', 'rt'], non_negative=True)
hashing_vectorizer = vectorizer_hashing_docs.transform(tweets)
vectors_hash_docs = hashing_vectorizer.toarray()

# hashing vecroizer for query
hash_query = vectorizer_hashing_docs.transform(query_to_search)
vectors_hash_query = hash_query.toarray()

query_doc_dict_hash = {}

i = 0
for doc_vectors in vectors_hash_docs:
    doc_vectors = doc_vectors.reshape(1, -1)
    hash_similarity = cosine_similarity(doc_vectors, vectors_hash_query)
    query_doc_dict_hash[i] = hash_similarity[0][0]
    i += 1

query_doc_dict_hash = sorted(query_doc_dict_hash, key=query_doc_dict_hash.get, reverse=True)
for i in range(0, 10):
    print(query_doc_dict_hash[i], tweets_dict[i])


