from __future__ import print_function
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation


n_samples = 9
n_features = 100
n_components = 3
n_top_words = 6


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()


print("Loading dataset...")
t0 = time()
## dataset = fetch_20newsgroups(shuffle=True, random_state=1,
                             ## remove=('headers', 'footers', 'quotes'))
## data_samples = dataset.data[:n_samples]
data_samples = [
"reksio szczeka na koty",
"pies glosno szczeka",
"koty cicho mrucza",
"reksio to madry pies",
"kerbale buduja rakiety",
"rakiety wynosza satelity",
"satelity sa na orbicie",
"rakiety glosno startuja",
"szybowce leca cicho",
"szybowce startuja z wyciagarki",
"samoloty szturmowe leca nisko",
"krowy jedza trawe",
"kury jedza ziarno",
"krowy pija wode"
]
print("done in %0.3fs." % (time() - t0))

# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=1,
                                   max_features=n_features,
                                   stop_words=['na','sa','z','to'])
t0 = time()
tfidf = tfidf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))
#print(tfidf)

# Use tf (raw term count) features for LDA.
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=1,
                                max_features=n_features,
                                stop_words=['na','sa','z'])
t0 = time()
tf = tf_vectorizer.fit_transform(data_samples)
tf_feature_names = tf_vectorizer.get_feature_names()
print("done in %0.3fs." % (time() - t0))
print(tf_feature_names)

# Fit the NMF model
if 1:
	print("Fitting the NMF model (Frobenius norm) with tf-idf features, "
	      "n_samples=%d and n_features=%d..."
	      % (n_samples, n_features))
	t0 = time()
	nmf = NMF(n_components=n_components, random_state=1,
		  alpha=.1, l1_ratio=.5).fit(tfidf)
	print("done in %0.3fs." % (time() - t0))

	print("\nTopics in NMF model (Frobenius norm):")
	tfidf_feature_names = tfidf_vectorizer.get_feature_names()
	print_top_words(nmf, tfidf_feature_names, n_top_words)

# Fit the LDA model
if 1:
	print("Fitting LDA models with tf features, "
	      "n_samples=%d and n_features=%d..."
	      % (n_samples, n_features))
	lda = LatentDirichletAllocation(n_components=n_components, max_iter=50,
					learning_method='online',
					learning_offset=50.,
					random_state=0)
	t0 = time()
	lda.fit(tf)
	print("done in %0.3fs." % (time() - t0))

	print("\nTopics in LDA model:")
	tf_feature_names = tf_vectorizer.get_feature_names()
	print_top_words(lda, tf_feature_names, n_top_words)
