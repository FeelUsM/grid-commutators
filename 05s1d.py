import os
import re
import sys
#f = form.open("form -l",keep_log=100)

print('=== python started ===')

try:
	k = [[" 1 ", " 1 ", " 1 ", " 1 "], 
	     [" 1 ", " 1 ", " i_", "-i_"], 
	     [" 1 ", "-i_", " 1 ", " i_"], 
	     [" 1 ", " i_", "-i_", " 1 "]]


	n = [[" 1    ", "cx(i1)", "cy(i1)", "cz(i1)"], 
	     ["cx(i1)", " 1    ", "cz(i1)", "cy(i1)"], 
	     ["cy(i1)", "cz(i1)", " 1    ", "cx(i1)"], 
	     ["cz(i1)", "cy(i1)", "cx(i1)", " 1    "]]

	c = ["1","cx","cy","cz"]
	s = ["1","sx","sy","sz"]
	rules = '\n'.join('id ifmatch->endarg '+c[i]+'(i1?)*'+s[j]+'(i1?) = '+
			  k[i][j]+'*'+str(n[j][i])+';' 
	       for i in range(1,4) for j in range(1,4))

	procedures = '''
* === 05s1d ===

cfun   cx,cy,cz,cc; *cten
set CC:cx,cy,cz;
nfun   sx,sy,sz,sc;
set SC:sx,sy,sz;

Function S,SS,Comm;

auto Symbols a,b,t;
auto Symbol n,i,j,k; * indices

cfun koef;
polyfun koef;

S n,n1,n2,x;
Table ident(x?);  Fill ident() = x;
Table prod(n?symbol_,n1?int_,n2?int_,x?);
Fill prod() =
  + theta_(n2-n1) * prod(n,n1,n2-1,x) * ident(x * replace_(n,n2))
  + thetap_(n1-n2)
;

S x,y,z;
Table if(x?int_,y?,z?);
Fill if() = deltap_(x)*y+delta_(x)*z;

#procedure overlapping
*--- overlapping ---
argument Comm;
    multiply S(1,1);
    repeat id S(k1?,t?)*cc?CC(i1?) = S(max_(k1,i1),t*cc(i1));
* -> koef*S(max(i...),cc(i)...)
endargument;

*id Comm(a?,b?) = a*b;
*id S(?ss1)*S(?ss2) = Comm(S(?ss1),S(?ss2));
id Comm(S(n1?,a1?),S(n2?,a2?)) = 
                  Comm(        a1,        a2) + 
    sum_(i,1,n2-1,Comm(SS(i,1)*a1,        a2)) +
    sum_(i,1,n1-1,Comm(        a1,SS(i,1)*a2));
argument Comm;
    repeat id SS(i?,t?)*cc?CC(j?) = SS(i,t*cc(i+j));
    id SS(i?,a?) = a;
endargument;
#endprocedure

#procedure multiply
*--- multiply ---
*id Comm(a?,b?) = S(a)*b-S(b)*a;
label repeat;
    id ifnomatch->endrepeat S(a?)*cc?CC[n](i1?) = S(a*SC[n](i1));
    argument S;
*        id cc?CC(i1?,i2?)*sc?SC(i1?,i2?) = 1;
'''+rules+\
'''
        id sc?SC[n?](i1?) = CC[n](i1);
        label endarg;
    endargument;
goto repeat;
label endrepeat;
id S(a?) = a;
*.sort
#endprocedure

#procedure trim
*--- trim ---
if(match(cc?CC(i?)));
    id once cc?CC(i1?) = S(i1,cc(i1));
    repeat id S(n1?,t?)*cc?CC(i1?) = S(min_(n1,i1),t*cc(i1));
    id ifmatch->endif S(1,t?) = t;
        id S(n1?,t?) = S(n1-1,1)*t;
        repeat id S(n1?,t?)*cc?CC(i1?) = S(n1,t*cc(i1-n1));
        id S(n1?,t?) = t;
    label endif;
endif;
#endprocedure

#procedure trimS
*--- trimS ---
if(match(cc?CC(i?)));
    id once cc?CC(i1?) = S(i1,cc(i1));
    repeat id S(n1?,t?)*cc?CC(i1?) = S(min_(n1,i1),t*cc(i1));
    id ifmatch->endif S(1,t?) = S(t);
        id S(n1?,t?) = S(n1-1,1)*t;
        repeat id S(n1?,t?)*cc?CC(i1?) = S(n1,t*cc(i1-n1));
        id S(n1?,t?) = S(t);
    label endif;
endif;
#endprocedure
'''

	with open('io'+os.sep+'in', 'r') as file:
		s = file.read().replace('\n', '').replace('[','(').replace(']',')').split('""')
	s[0] = s[0].replace('{','').replace('}','').replace(' ','')
	s[3] = int(s[3])
	[syms,H,N,k,t,si]=s # si - save intermediate results
	si = si=='True'

	with open('io/code.frm', 'w') as f:
		f.write('''
on stats;
'''+procedures+'''
* === H ===
'''+'Sym '+syms+';\n'+
'Local H  = '+H+';'+
'''
* =========
id S(a?)*b?=Comm(a,1)*koef(b);
id S(a?)=Comm(a,1);
* Mul Comm(1,1);
* repeat id Comm(a?,b?)*cx?(?xxx) = Comm(a*cx(?xxx),b);
* Print;
.sort
skip;
* === N ===
'''+
'Local N1 = '+N+';'+
'''
* =========
id S(a?)*b?=a*koef(b);
id S(a?)=a;
* Print;
.sort
Skip;
'''+

''.join(
'''
* === iteration {} ===

Local N2 = H*N1;
repeat id Comm(a?,b?)*cx?CC(?xxx) = Comm(a,b*cx(?xxx));

#call overlapping
id Comm(a?,b?) = S(a)*b-S(b)*a;
#call multiply
* Print;
.sort
skip; nskip N2;
#call trimS

format mathematica;
* Print;
.sort
{}
Skip;

Local N1 = N2;
id S(t?) = t;
* Print;
.sort
Skip;
'''.format(i+1,'#write <io/out{}> "%E" , N2'.format(i+1) if si else '') for i in range(k-1) 
)+

'''
* === iteration {} ===

Local N2 = H*N1;
repeat id Comm(a?,b?)*cx?CC(?xxx) = Comm(a,b*cx(?xxx));

#call overlapping
id Comm(a?,b?) = S(a)*b-S(b)*a;
#call multiply
* Print;
.sort
skip; nskip N2;
#call trimS

format mathematica;
* Print;
.sort
Skip;
#write <io/out{}> "%E" , N2
.end
'''.format(k,k))


	if t=='1':
		f = os.system("form"+os.sep+"form -l io/code.frm")
	else:
		f = os.system("form"+os.sep+"tform -w"+t+" -l io/code.frm")



	with open('io/out{}'.format(k), 'r') as f2:
		with open('io/out', 'w') as f1:
			f1.write(re.sub(r'[ \n\r\t\v]','',re.sub(r'i_','I',f2.read())))
except Exception as e:
	import sys,traceback
	try:
		traceback.print_exception(type(e), e, sys.last_traceback)
	finally:
		print('!!!error!!!, press enter')
		input()
