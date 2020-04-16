import inverness
from inverness.sorbet import sorbet
from tqdm import tqdm

path = 'model_all_v7/'
model = inverness.Model(path)
model.load(['fun','meta'])
fixed = sorbet(path+'meta_fixed').new()
meta = tqdm(model.meta, desc='meta', total=len(model.meta))
for m in meta:
	m['path'] = m['path'].replace('\\','/').replace('data/','/kaggle/input/CORD-19-research-challenge/')
	fixed.append(m)
fixed.save()

print(model.meta[4242])
print(fixed[4242])
