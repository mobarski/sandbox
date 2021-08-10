from bottle import template

canvas_template = """
<canvas id="main_canvas" width="{{ width }}" height="{{ height }}" style="border:1px solid #000000;">
</canvas> 

<div id="tooltip" style="opacity:1">
    tu bedzie tooltip
</div>

<script>
    var c = document.getElementById("main_canvas");
    var ctx = c.getContext("2d");
    % for p in points:
        ctx.fillRect({{ p['x'] }},{{ p['y'] }},{{ w }},{{ h }});
    % end
</script>
"""

# TODO: js fun -> ustawia kolor i dodaje wiele punktow

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

text = template(canvas_template,locals())
with open('v2.html','w') as f:
    f.write(text)
