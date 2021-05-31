import form
import re
f = form.open("form -l",keep_log=100)

print('=== python started ===')

k = [[" 1 ", " 1 ", " 1 ", " 1 "], 
     [" 1 ", " 1 ", " i_", "-i_"], 
     [" 1 ", "-i_", " 1 ", " i_"], 
     [" 1 ", " i_", "-i_", " 1 "]]


n = [[" 1       ", "cx(i1,i2)", "cy(i1,i2)", "cz(i1,i2)"], 
     ["cx(i1,i2)", " 1       ", "cz(i1,i2)", "cy(i1,i2)"], 
     ["cy(i1,i2)", "cz(i1,i2)", " 1       ", "cx(i1,i2)"], 
     ["cz(i1,i2)", "cy(i1,i2)", "cx(i1,i2)", " 1       "]]

c = ["1","cx","cy","cz"]
s = ["1","sx","sy","sz"]
rules = '\n'.join('id ifmatch->endarg '+c[i]+'(i1?,i2?)*'+s[j]+'(i1?,i2?) = '+
                  k[i][j]+'*'+str(n[j][i])+';' 
       for i in range(1,4) for j in range(1,4))

procedures = '''
cfun   cx,cy,cz,cc; *cten
set CC:cx,cy,cz;
nfun   sx,sy,sz,sc;
set SC:sx,sy,sz;

Function S,SS,Comm;

auto Symbols a,b,t;
auto Symbol n,i,j,k; * indices

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

*--- expand ---
#procedure expand
splitarg Comm,1;
repeat id Comm(a?,a1?,?centr,b?) = Comm(a,b) + Comm(a1,?centr,b);
id Comm(a?,a1?,b?) = Comm(a,b)+Comm(a1,b);
splitarg Comm,2;
repeat id Comm(a?,?centr,b1?,b?) = Comm(a,b) + Comm(a,?centr,b1);
id Comm(a?,b1?,b?) = Comm(a,b)+Comm(a,b1);
#endprocedure

*--- overlapping ---
#procedure overlapping
argument Comm;
    multiply S(1,1,1);
    repeat id S(k1?,k2?,t?)*cc?CC(i1?,i2?) = S(max_(k1,i1),max_(k2,i2),t*cc(i1,i2));
endargument;
id Comm(a?,b?) = a*b;
id S(?ss1)*S(?ss2) = Comm(S(?ss1),S(?ss2));
id Comm(S(n1?,k1?,a1?),S(n2?,k2?,a2?)) = 
                  Comm(S(k1,        a1),S(k2,        a2))  + 
    sum_(i,1,n2-1,Comm(S(k1,SS(i,1)*a1),S(k2,        a2))) +
    sum_(i,1,n1-1,Comm(S(k1,        a1),S(k2,SS(i,1)*a2)));
argument Comm; argument S,2;
    repeat id SS(i?,t?)*cc?CC(j?,k?) = SS(i,t*cc(i+j,k));
    id SS(i?,a?) = a;
endargument;endargument;
id Comm(S(n1?,a1?),S(n2?,a2?)) = 
                  Comm(        a1,        a2) + 
    sum_(i,1,n2-1,Comm(SS(i,1)*a1,        a2)) +
    sum_(i,1,n1-1,Comm(        a1,SS(i,1)*a2));
argument Comm;
    repeat id SS(i?,t?)*cc?CC(k?,j?) = SS(i,t*cc(k,i+j));
    id SS(i?,a?) = a;
endargument;
#endprocedure

*--- multiply ---
#procedure multiply
*id Comm(a?,b?) = S(a)*b-S(b)*a;
label repeat;
    id ifnomatch->endrepeat S(a?)*cc?CC[n](i1?,i2?) = S(a*SC[n](i1,i2));
    argument S;
*        id cc?CC(i1?,i2?)*sc?SC(i1?,i2?) = 1;
'''+rules+\
'''
        id sc?SC[n?](i1?,i2?) = CC[n](i1,i2);
        label endarg;
    endargument;
goto repeat;
label endrepeat;
id S(a?) = a;
*.sort
#endprocedure

*--- trim ---
#procedure trim
if(match(cc?CC(i?,j?)));
    multiply S(1000000,1000000,1);
    repeat id S(n1?,n2?,t?)*cc?CC(i1?,i2?) = S(min_(n1,i1),min_(n2,i2),t*cc(i1,i2));
    id ifmatch->endif S(1,1,t?) = t;
        id S(n1?,n2?,t?) = S(n1-1,n2-1,1)*t;
        repeat id S(n1?,n2?,t?)*cc?CC(i1?,i2?) = S(n1,n2,t*cc(i1-n1,i2-n2));
        id S(n1?,n2?,t?) = t;
    label endif;
endif;
#endprocedure

*--- trimS ---
#procedure trimS
if(match(cc?CC(i?,j?)));
    multiply S(1000000,1000000,1);
    repeat id S(n1?,n2?,t?)*cc?CC(i1?,i2?) = S(min_(n1,i1),min_(n2,i2),t*cc(i1,i2));
    id ifmatch->endif S(1,1,t?) = S(t);
        id S(n1?,n2?,t?) = S(n1-1,n2-1,1)*t;
        repeat id S(n1?,n2?,t?)*cc?CC(i1?,i2?) = S(n1,n2,t*cc(i1-n1,i2-n2));
        id S(n1?,n2?,t?) = S(t);
    label endif;
endif;
#endprocedure
'''

with open('in1', 'r') as f:
    s = f.read().replace('\n', '').replace('[','(').replace(']',')').split('""')
s[0] = s[0].replace('{','').replace('}','').replace(' ','')
s[3] = int(s[3])
[syms,H,N,k]=s

f.close()
f = form.open("form -l",keep_log=100)
f.write('''
on stats;
'''+procedures+'Sym '+syms+';'+
'Local H  = '+H+';'+
'Local N1 = '+N+';'+
'''
id S(a?)=a;
.sort
'''+
'''
Skip;

Local N2 = Comm(H,N1);

#call expand
#call overlapping
id Comm(a?,b?) = S(a)*b-S(b)*a;
#call multiply
.sort
skip; nskip N2;
Local N1 = N2;
#call trim

format mathematica;
.sort
'''*(k-1)+
'''
Skip;

Local N2 = Comm(H,N1);

#call expand
#call overlapping
id Comm(a?,b?) = S(a)*b-S(b)*a;
#call multiply
.sort
skip; nskip N2;
Local N1 = N2;
#call trimS

format mathematica;
.sort
''')
tmp = re.sub(r'i_','I',f.read('N2'))

with open('out1', 'w') as f:
    f.write(tmp)