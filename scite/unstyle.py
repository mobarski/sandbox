import os
import re

for fn in os.listdir('.'):
	if not fn.endswith('.properties'): continue
	raw = open(fn,'r').read()
	n = len(re.findall('(?m)^style[.]',raw))
	print(fn,n)
	clean = re.sub('(?m)^style[.]','#~unstyle~#style.',raw)
	open(fn,'w').write(clean)
