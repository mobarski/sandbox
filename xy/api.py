from bottle import template

# TODO group colors

# TODO mouseenter vs click
# TODO select and hilight

# TODO zoom
# TODO shapes

default = {
	'width':800,
	'height':600,
	'margin':5,
	'size':20,
	'shape':'rect',
	'inner_html':'""'
}


class XY:

	def __init__(self,**kwargs):
		self.options = kwargs
		self.groups = []
		self.x_min = []
		self.x_max = []
		self.y_min = []
		self.y_max = []
	
	def add(self, group, data, **kwargs):
		self.groups += [(group,data,kwargs)]
		# 
		x = [p['x'] for p in data]
		y = [p['y'] for p in data]
		self.x_min += [min(x)]
		self.x_max += [max(x)]
		self.y_min += [min(y)]
		self.y_max += [max(y)]
		
	def render(self,mode='canvas'):
		vars = default.copy()
		vars.update(self.options)
		vars['groups'] = self.groups
		self.preprocess(vars)
		#
		if mode=='canvas':
			pass
		elif mode=='svg':
			return template(svg_template, vars)
		else:
			return self.options, self.groups # DEBUG
	
	def preprocess(self, vars):
		x_min = min(self.x_min)
		y_min = min(self.y_min)
		x_max = max(self.x_max)
		y_max = max(self.y_max)
		size = vars['size']
		shape = vars['shape']
		margin = int(vars['margin']+0.5*size)
		x_factor = 1.0*(vars['width']-2*margin) / (x_max-x_min)
		y_factor = 1.0*(vars['height']-2*margin) / (y_max-y_min)
		for name,points,kwargs in vars['groups']:
			for p in points:
				if shape=='circle':
					p['_x'] = margin + int( x_factor * (p['x']-x_min))
					p['_y'] = margin + int( y_factor * (p['y']-y_min))
				else:
					p['_x'] = margin + int( x_factor * (p['x']-x_min) -0.5*size)
					p['_y'] = margin + int( y_factor * (p['y']-y_min) -0.5*size)
				# aux
				keys = [k for k in p.keys() if not k.startswith('_')]
				p['_aux'] = u' '.join(['{}={}'.format(k,quote(p[k])) for k in keys]
									+ ['{}={}'.format(k,quote(v)) for k,v in kwargs.items()])
		
		
	def render_to_file(self,path,mode='canvas'):
		text = self.render(mode)
		with open(path,'w') as f:
			f.write(text)

def quote(x):
	try:
		return u'"'+x+u'"'
	except:
		return x

# -----------------------------------------------------------------------------

svg_template = """

<style>
	.datapoint {
		width: {{ size }};
		height: {{ size }};
	}
	<!-- TODO -->
	.g1 {
		fill: #FFaaaa;
	}
	.g2 {
		fill: #aaFFaa;
	}
</style>

<script>
	function tooltip(event,elem) {
		t = document.getElementById("tooltip")
		t.innerHTML = {{! inner_html }}
	}
</script>

<!-- ----------------------------------------------------------------------- -->

<svg width={{ width }} height={{ height }}>
	% for grp,points,grp_aux in groups:
		% for p in points:
			% if shape=='circle':
				<circle class="datapoint {{ p.get('_g','') }}" cx={{ p['_x'] }} cy={{ p['_y'] }} r={{ p.get('r',0.5*size) }} {{! p.get('_aux','') }}
					onmouseenter="tooltip(event,this)" />				
			% else:
				<rect class="datapoint {{ p.get('_g','') }}" x={{ p['_x'] }} y={{ p['_y'] }} {{! p.get('_aux','') }}
					onmouseenter="tooltip(event,this)" />
			% end
		% end
	% end
</svg>

<div id="tooltip" class="tooltip">
</div>
"""

# -----------------------------------------------------------------------------

if __name__=="__main__":
	plt = XY(width=900,height=500,inner_html=''' "<br>id:"+elem.getAttribute('id') + "<br>title: "+elem.getAttribute('title') ''')
	plt.add('first',[{'x':1,'y':2,'id':123},{'x':2,'y':3,'id':234},{'x':3,'y':1,'id':321}],xxx='yyy')
	plt.add('second',[{'x':11,'y':22,'id':2123},{'x':22,'y':33,'id':2234},{'x':33,'y':11,'id':2321}],aaa='bbb')
	print(plt.render('svg'))
	plt.render_to_file('api_test.html',mode='svg')
