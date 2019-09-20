from bottle import template
from random import randint

# TODO better colors

# TODO canvas mode
# TODO filter and highlight
# TODO select single
# TODO url

# TODO zoom
# TODO shapes

default = {
	'width':800,
	'height':600,
	'margin':5,
	'size':5,
	'shape':'rect',
	'inner_html':'""',
	"g_color":{}
}


class XY:

	def __init__(self,**kwargs):
		self.options = kwargs
		self.groups = []
		self.x_min = []
		self.x_max = []
		self.y_min = []
		self.y_max = []

	
	def add(self, name, points, **other):
		self.groups += [(name, points, other)]
		# 
		x = [p['x'] for p in points]
		y = [p['y'] for p in points]
		self.x_min += [min(x)]
		self.x_max += [max(x)]
		self.y_min += [min(y)]
		self.y_max += [max(y)]


	def render_to_file(self,path,mode='canvas'):
		text = self.render(mode)
		with open(path,'wb') as f:
			f.write(text.encode('utf8'))
		
	def render(self,mode='canvas'):
		vars = default.copy()
		vars.update(self.options)
		vars['groups'] = self.groups
		#
		self._preproc_gxy(vars)
		self._preproc_aux(vars)
		self._preproc_color(vars)
		#
		if mode=='canvas':
			pass
		elif mode=='svg':
			return template(svg_template, vars)
		else:
			return self.options, self.groups # DEBUG

	
	
	def _preproc_gxy(self, vars):
		x_min = min(self.x_min)
		y_min = min(self.y_min)
		x_max = max(self.x_max)
		y_max = max(self.y_max)
		size = vars['size']
		shape = vars['shape']
		height = vars['height']
		margin = int(vars['margin']+0.5*size)
		x_factor = 1.0*(vars['width']-2*margin) / (x_max-x_min)
		y_factor = 1.0*(vars['height']-2*margin) / (y_max-y_min)
		for g,(name,points,other) in enumerate(vars['groups']):
			for p in points:
				p['g'] = g
				if shape=='circle':
					p['_x'] = margin + int( x_factor * (p['x']-x_min))
					p['_y'] = height - margin - int( y_factor * (p['y']-y_min))
				else:
					p['_x'] = margin + int( x_factor * (p['x']-x_min) -0.5*size)
					p['_y'] = height - margin - int( y_factor * (p['y']-y_min) -0.5*size)
	
	
	def _preproc_aux(self, vars):
		for g,(name,points,other) in enumerate(vars['groups']):
			for p in points:
				keys = [k for k in p.keys() if not k.startswith('_') and k not in ('x','y')]
				p['_aux'] = u' '.join([u'{}={}'.format(k,quote(p[k])) for k in keys]
									+ [u'{}={}'.format(k,quote(v)) for k,v in other.items()])
	
	
	def _preproc_color(self, vars, mode='hash', force={}):
		for g,(name,points,kwargs) in enumerate(vars['groups']):
			h = abs(hash(name))
			if mode=='hash':
				rgb = ((h>>0)%255, (h>>8)%255, (h>>16)%255)
			elif mode=='mono_hash':
				v = h%240
				rgb = (v,v,v)
			else:
				rgb = (randint(0,255), randint(0,255), randint(0,255))
			if g in force:
				rgb = force[g]
			vars['g_color'][g] = rgb
	

def quote(x):
	try:
		return u'"'+x+u'"'
	except:
		return x

# -----------------------------------------------------------------------------

svg_template = u"""

<script>

	var g = -1
	
	function tooltip(event,elem) {
		var t = document.getElementById("tooltip")
		t.innerHTML = {{! inner_html }}
	}
	
	function highlight(event,elem) {
		pg = g
		g = elem.getAttribute("g")
		var points = document.getElementsByClassName("datapoint")
		if (g==pg) {
			g = -1
			for(var i in points) {
				points[i].style.fill = ''
			}
		} else {
			for(var i in points) {
				var p = points[i]
				if (p.getAttribute("g")==g) {
					p.style.fill = ''
				} else {
					p.style.fill = '#aaaaaa' 
				}
			}
		}
	}
	
</script>

<!-- ----------------------------------------------------------------------- -->

<svg width={{ width }} height={{ height }}>

	<style>
		svg {
			background-color: #FFFFFF;
		}
		
		.datapoint {
			width: {{ size }};
			height: {{ size }};
		}
		
		% for i,c in g_color.items():
			.g{{ i }} {
				fill: #{{ "{:02x}{:02x}{:02x}".format(c[0],c[1],c[2]) }};
			}
		% end
	</style>

	% for grp,points,grp_aux in groups:
		% for p in points:
			% if shape=='circle':
				<circle class="datapoint g{{ p.get('g','') }}" cx={{ p['_x'] }} cy={{ p['_y'] }} r={{ p.get('r',0.5*size) }} {{! p.get('_aux','') }}
					onmouseenter="tooltip(event,this)" onclick="highlight(event,this)" />				
			% else:
				<rect class="datapoint g{{ p.get('g','') }}" x={{ p['_x'] }} y={{ p['_y'] }} {{! p.get('_aux','') }}
					onmouseenter="tooltip(event,this)" onclick="highlight(event,this)" />
			% end
		% end
	% end

</svg>

<div id="tooltip" class="tooltip">
</div>
"""

# -----------------------------------------------------------------------------

if __name__=="__main__":
	from random import randint
	def r(): return randint(0,1000)
	plt = XY(width=900, height=500, size=10, shape='circle', inner_html='''`
		<br>id: ${elem.getAttribute('id')}
		<br>title: ${elem.getAttribute('title')}
		`''')
	plt.add('alpha',[{'x':r(),'y':r(),'id':r()} for _ in range(20)],xxx='yyy')
	plt.add('beta',[{'x':r(),'y':r(),'id':r()} for _ in range(20)], aaa='bbb')
	plt.add('gamma',[{'x':r(),'y':r(),'id':r()} for _ in range(20)],ccc='ddd')
	print(plt.render('svg'))
	plt.render_to_file('api_test.html',mode='svg')
