from sklearn.feature_extraction.text import CountVectorizer

DOCUMENTS = [
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

STOPWORDS = ['na','to','sa']

vectorizer = CountVectorizer(stop_words=STOPWORDS)
X = vectorizer.fit_transform(DOCUMENTS)
F = vectorizer.get_feature_names()

if __name__=="__main__":
	print(X.toarray())
	print(F)
