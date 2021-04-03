import serial
import time

ser=serial.Serial(port="/dev/ttyUSB0",baudrate=38400,timeout=3)
print ("hi")
ser.write(str.encode("on."))
time.sleep(1)
ser.write(str.encode("off."))
time.sleep(1)

conset={}
typeset={}
doneset=set()

def lqi(targetaddr):
	targetaddr=targetaddr.replace("0x","")
	if targetaddr=="": ser.write(str.encode("lqireq."))
	else: ser.write(str.encode("lqireq_"+targetaddr+"."))
	l="init"
	while (len(l)):
		l = ser.readline().decode('utf-8')
		l=l.replace("\n","")
		#if len(l): print (l)
		if l.startswith("lqi req "):
			print(l)
			l=l.replace(".","")
			myadd=l[8:]
			if targetaddr=="": targetaddr=myadd
			targetaddr=targetaddr.replace("0x","")
			print(targetaddr,"connected to")
			doneset.add(targetaddr)
		if l.startswith("entries_"):
			ent=l.split("_")[1]
			print(ent,"entries")
		if l.startswith("item_"):
			l=l.replace(".","")
			t=l.split("_")
			print(t)
			conset[myadd+"_"+t[2]]=t[3]
			typeset[t[2]]=t[4]

lqi("")

print(conset)
print(typeset)
print(doneset)

working=True
while (working):
	working=False
	for item in conset:
		items=item.split("_")
		a=items[0]
		b=items[1]
		print(a," ",b," ",conset[item])
		b=b.replace("0x","")
		if b in doneset: print(b,"is done already")
		else:
			print(b,"will be requested")
			lqi(b)
			working=True
			break

	print(conset)
	print(typeset)
	print(doneset)

ser.close()

import json
with open('typeset.json.txt', 'w') as typeset_file:
	json.dump(typeset, typeset_file)
with open('conset.json.txt', 'w') as conset_file:
	json.dump(conset, conset_file)


