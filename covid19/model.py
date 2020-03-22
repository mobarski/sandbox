from model_phraser import HoracyPhraser
from model_dictionary import HoracyDictionary

class HoracyModel(
		HoracyPhraser,
		HoracyDictionary):
	pass

if __name__=="__main__":
	model = HoracyModel()
	model.load_phraser()
	model.init_dictionary(50)
	model.save_dictionary()
