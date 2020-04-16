import inverness
import nmslib
from tqdm import tqdm
from time import time

label=4000
model = inverness.Model(f'model_{label}_v7/').load(['fun','meta','phraser','dictionary','tfidf','lsi','dense_ann'])
ann = nmslib.init(method='hnsw', space='cosinesimil')

if 1:
	ann.loadIndex('xxx_synonymes.bin',load_data=True)
else:
	t0 = time()
	items = model.dictionary.items()
	items = tqdm(items,desc='tokens',total=len(model.dictionary))
	for id,token in items:
		point = model.text_to_dense(token)
		ann.addDataPoint(id,point)
	ann.createIndex(print_progress=True)
	ann.saveIndex('xxx_synonymes.bin',save_data=True)
	print('done in ',time()-t0)

point = model.text_to_dense('APACHE SOFA SAPS')
point = model.text_to_dense('remotely')
i_d_list = ann.knnQuery(point,40)
for id,dist in list(zip(*i_d_list))[:40]:
	token = model.dictionary.get(id)
	df = model.dictionary.dfs[id]
	print(F"{id:8}  {token:20} {df:5}  {dist:.03f}")

# non-survivors *elder* *older* young* menopause VIDD year 
# extubation reintubation ventilated non.?invasive* invasive*
# usunac RIFLE
# ocena DFS criteria


# NEXT
"""Age-adjusted mortality data for Acute Respiratory Distress Syndrome (ARDS) with/without other organ failure – particularly for viral etiologies"""

"""Efforts to determine adjunctive and supportive interventions that can improve the clinical outcomes of infected patients (e.g. steroids, high flow oxygen)"""

"""Best telemedicine practices, barriers and faciitators, and specific actions to remove/expand them within and across state boundaries."""


"""Extracorporeal membrane oxygenation (ECMO) outcomes data of COVID-19 patients"""
"""Knowledge of the frequency, manifestations, and course of extrapulmonary manifestations of COVID-19, including, but not limited to, possible cardiomyopathy and cardiac arrest"""


"""Guidance on the simple things people can do at home to take care of sick people and manage disease"""
"""Use of AI in real-time health care delivery to evaluate interventions, risk factors, and outcomes in a way that could not be done manually"""
