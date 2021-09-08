import os, re

with open('io'+os.sep+'in', 'r') as file:
	s = file.read().replace('\n', '').replace('[','(').replace(']',')').split('""')
s[0] = s[0].replace('{','').replace('}','').replace(' ','')
s[3] = int(s[3])
[syms,H,N,k,t,si]=s # si - save intermediate results
si = si=='True'

with open('io/out{}'.format(k), 'r') as f2:
	with open('io/out', 'w') as f1:
		f1.write(re.sub(r'[ \n\r\t\v]','',re.sub(r'i_','I',f2.read())))
