from bottle import template

# TODO: inne podejscie - rysyjemy na canvas i odpytujemy strukture danych

svg_template = """

<style>
	.datapoint {
		width: {{ w }};
		height: {{ h }};
	}
	.g1 {
		fill: #FFaaaa;
	}
	.g2 {
		fill: #aaFFaa;
	}
</style>

<script>
	function tooltip_off(event,elem) {
		t = document.getElementById("tooltip")
		t.style.opacity = 0
		elem.style.opacity = 1
	}
	function tooltip(event,elem) {
		t = document.getElementById("tooltip")
		t.innerHTML = "<br>id:"+elem.getAttribute('id') + "<br>title: "+elem.getAttribute('title')
	}
</script>

<!-- ----------------------------------------------------------------------- -->

<svg width={{ width }} height={{ height }}>
    % for p in points:
        <rect class="datapoint {{ p.get('g','') }}" x={{ p['x'] }} y={{ p['y'] }} {{! p.get('__aux__','') }}
              onmouseenter="tooltip(event,this)"
              />
    % end
</svg>

<div id="tooltip" style="opacity:1">
    tu bedzie tooltip
</div>
"""

raw_points = [
    dict(x=100,y=200,title="to jest test",id=123),
    dict(x=200,y=50,g='g1',id=321)
]

from random import randint

for i in range(10000):
    raw_points += [dict(x=randint(1,800),y=randint(1,600),id=i,title="tytul -> "+str(i))]

# --------------------------

points = []
for r in raw_points:
    p = {}
    p['x'] = r['x'] # TODO: x vs screen_x
    p['y'] = r['y'] # TODO: y vs screen_y
    p['g'] = r.get('g','') # TODO: normalize to g1,g2,g3...
    aux = []
    for k in r:
        if k in ('x','y','g'): continue
        aux += ['{}="{}"'.format(k,r[k]) if type(r[k]) is str else '{}={}'.format(k,r[k])]
    p['__aux__'] = ' '.join(aux)
    points += [p]
   
w = 3
h = 3
width = 800
height = 600

text = template(svg_template,locals())
with open('v1.html','w') as f:
    f.write(text)
