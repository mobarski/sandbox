# Author: Olivier Grisel <olivier.grisel@ensta.org>
#         Lars Buitinck
#         Chyi-Kwei Yau <chyikwei.yau@gmail.com>
# License: BSD 3 clause

from __future__ import print_function
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups

n_samples = 2000
n_features = 1000
n_components = 4
n_top_words = 8


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()


# Load the 20 newsgroups dataset and vectorize it. We use a few heuristics
# to filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.

print("Loading dataset...")
t0 = time()
dataset = [
	"In the Kingdom you'll find the best games to play in your browser, as well as our game apps. Play on your computer, mobile or tablet and simply sync your progress. King games are easy to pick up, but hard to put down! So get ready to have fun and enter the Kingdom!"
	,"Peter Rabbit and Pacific Rim Uprising are two of the top trending upcoming movies on IMDb. See what else is coming out this season, get the latest release dates, trivia, and more."
	,"Legion, the acclaimed drama series from creator and executive producer Noah Hawley, will return to FX on Tuesday, April 3 at 10 Pm ET/PT.  Based on the Marvel Comics by Chris Claremont and Bill Sienkiewicz, Legion is the story of David Haller (Dan Stevens), a man who believed himself to be ..."
	,"Disney Pixar's Coco is more of a movie with music than a musical, but during its earlier stages of development, it was going to be a full-blown songified romp through the Land of the Dead. After seeing the early plans for the opening number, all I can say is I'm thrilled it ended up changing. "
	,"onight, Syfy's horror anthology series Channel Zero dips back into the Creepypasta chest of frights for Butcher's Block. The third season of the show is just as unsettling as Candle Cove and No-End House with the added distinction of being the goriest Channel Zero yet. "
	,"Watching a bubble float effortlessly through the @Space_Station may be mesmerizing and beautiful, but that same bubble is also teaching @ISS_Research about how fluids behave differently in microgravity."
	,"Two asteroids, one week. The 1st of this week's close-approaching asteroids happened Feb. 6 at 3:10pm ET at a distance of ~114,000 miles. The 2nd asteroid will safely pass by Earth on Fri. at 2:30pm at a distance of ~39,000 miles"
	,"Somewhat more stable wall-climbing truck. Would love feedback. WASD to drive, Space turns on your control thrusters and Q turns on the rector. E shuts down the reactor, useful for once on flat ground"
	,"Does art imitate life or does life imitate art? Join @AndyWeirAuthor of The Martian, and Planetary Science Director Jim Green as we explore the fascinating intersection of science & science fiction in the season one finale of our Gravity Assist podcast: http://go.nasa.gov/2seReWf "
	,"We've opened up a public Upcoming Beta branch on Steam so our most eager of Trailmakers can check out upcoming patches! Check out the notes and a tease of more news soon here!"
	]
data_samples = dataset[:n_samples]
print("done in %0.3fs." % (time() - t0))

# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=1,
                                   max_features=n_features,
                                   stop_words='english')
t0 = time()
tfidf = tfidf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))

# Use tf (raw term count) features for LDA.
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=1,
                                max_features=n_features,
                                stop_words='english')
t0 = time()
tf = tf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))
print()

if 0:
	# Fit the NMF model
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

if 0:
	# Fit the NMF model
	print("Fitting the NMF model (generalized Kullback-Leibler divergence) with "
	      "tf-idf features, n_samples=%d and n_features=%d..."
	      % (n_samples, n_features))
	t0 = time()
	nmf = NMF(n_components=n_components, random_state=1,
		  beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,
		  l1_ratio=.5).fit(tfidf)
	print("done in %0.3fs." % (time() - t0))

	print("\nTopics in NMF model (generalized Kullback-Leibler divergence):")
	tfidf_feature_names = tfidf_vectorizer.get_feature_names()
	print_top_words(nmf, tfidf_feature_names, n_top_words)

print("Fitting LDA models with tf features, "
      "n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
				learning_method='online',
				learning_offset=50.,
				random_state=0)
t0 = time()
lda.fit(tf)
print("done in %0.3fs." % (time() - t0))

print("\nTopics in LDA model:")
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)
