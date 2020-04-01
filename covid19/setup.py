from setuptools import setup, find_packages

setup(
	name="horace",
	version="0.0.1",
	scripts=[
		'model.py',
		'model_ann.py',
		'model_dictionary.py',
		'model_lsi.py',
		'model_meta.py',
		'model_phraser.py',
		'model_sentencer.py',
		'model_tfidf.py',
		'sorbet.py',
		'util_coverage.py',
		'util_time.py',
	],
	install_requires=["gensim","nmslib","numpy"],
	
	author="Maciej Obarski",
	author_email="mobarski@gmail.com",
	description="",
	keywords="",
	classifiers=[
		"License :: OSI Approved :: Python Software Foundation License"
	]
	#packages=find_packages()
)
