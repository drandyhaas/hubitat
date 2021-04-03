import graphviz
print(graphviz.ENGINES)
#set(['twopi', 'patchwork', 'osage', 'fdp', 'circo', 'neato', 'dot', 'sfdp'])

f = graphviz.Digraph('zigbee mesh', filename='mesh.gv', engine='circo')

import json
with open('typeset.json.txt') as tt:
	typeset = json.load(tt)
with open('conset.json.txt') as gg:
	conset = json.load(gg)
with open('znames.json.txt') as gn:
	znames = json.load(gn)

for n in typeset:
	print(n, typeset[n])
	xn=n # xn=n.replace("0x","")
	print(znames[xn])
	if typeset[n]=="c": f.attr('node', shape='box', width="2", color="black", label=str(znames[xn]))
	elif typeset[n]=="r": f.attr('node', shape='doublecircle', width="1", color="red", label=str(znames[xn]))
	elif typeset[n]=="e": f.attr('node', shape='circle', width="1", color="blue", label=str(znames[xn]))
	else: print("what?!")
	f.node(n)

for e in conset:
	lqi=float(conset[e])/80.
	print(e, lqi)
	e=e.split("_")
	a=e[0]
	b=e[1]
	f.edge(a, b, weight=str(lqi), penwidth=str(lqi))

f.view()

