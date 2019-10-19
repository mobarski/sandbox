with open('itsy0.js','w') as fo:
	for fn in ['computer','core','storage','banks','palette','screen','boot','mouse','touch','keyboard']:
		with open(fn+'.js','r') as f:
			fo.write(f.read())

# TODO: https://obfuscator.io/
