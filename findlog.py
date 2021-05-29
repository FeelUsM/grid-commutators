import form
f = form.open()
with open('out1', 'w') as ff:
	print('"'+f.read("`NAME_'")+'"',file=ff)
f.close()
