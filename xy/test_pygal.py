import pygal
plt = pygal.XY(stroke=False)
plt.add('aaa',[(1,2),(3,4)],dots_size=1)
plt.add('bbb',[(1,4),(2,3)],dots_size=1)
plt.render_to_file('test_pygal.svg')
