from horacy import HoracyModel
model = HoracyModel('model_1000/').load()

# TODO sprawdzanie zakresu -1,+2

q = "mechanical ventilation"
top = model.find_dense(q,20)
for i,d,m in top:
	doc = model.get_doc(i)
	text = model.doc_to_text(doc).replace('\n',' ').replace('\r',' ')
	doc2 = model.get_doc(i+1)
	text2 = model.doc_to_text(doc2).replace('\n',' ').replace('\r',' ')		
	print(f"{d:.03f}  {text} {text2}")
