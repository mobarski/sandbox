from setuptools import setup, find_packages

setup(
	name="horacy",
	version="0.0.1",
	packages=find_packages(),
	
	install_requires=["gensim","nmslib","tqdm"],
	
	author="Maciej Obarski",
	author_email="mobarski@gmail.com",
	description="Natural Language Processing (NLP) framework "\
		"built on top of gensim and nmslib.",
	keywords="NLP",
	classifiers=[
		"License :: OSI Approved :: Python Software Foundation License"
	]
)
