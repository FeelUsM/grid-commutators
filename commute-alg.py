import os
import re
import sys
import argparse

parser = argparse.ArgumentParser(
	description = 'calculate k commutators [H,...[H,[H,N]]...]'
)

# -c --continue - всё прочитать из in файла и code.frm/log - добавляются, иначе всё перезаписывается
# -d --dim 1d/2d/3d
# -a --alg имя_файла[.alg]
# -S --syms символы из коэффициентов H и N
# -H --H гамильтониан
# -N --N наблюдаемая
# -s --stop K - крайняя итерация, количество коммутаторов
# -t --threads t
# -r --rules доп.правила преобразования коэфициентов

parser.add_argument('--continue','-c',action='store_true',dest='cont')
parser.add_argument('--force'   ,'-f',action='store_true')
parser.add_argument('--dim'     ,'-d',type=int,choices=[1,2,3])
parser.add_argument('--alg'     ,'-a')
parser.add_argument('--syms'    ,'-S')
parser.add_argument('--H'       ,'-H')
parser.add_argument('--N'       ,'-N')
parser.add_argument('--stop'    ,'-s',type=int)
parser.add_argument('--threads' ,'-t',type=int)
parser.add_argument('--rules'   ,'-r',dest='k_rules') # koefficient rules

#print(sys.argv,file=sys.stderr)
args = parser.parse_args()
#print("cont   ",args.cont   )
#print("force  ",args.force  )
#print("dim    ",args.dim    )
#print("alg    ",args.alg    )
#print("syms   ",args.syms   )
#print("H      ",args.H      )
#print("N      ",args.N      )
#print("stop   ",args.stop   )
#print("threads",args.threads)
#print("k_rules",args.k_rules)

if args.syms!=None:
	if not re.match('^\{.*\}$',args.syms):
		print('error: syms arg must be in curly braces',file=sys.stderr)
		exit(1)
if args.H!=None:
	args.H = args.H.replace('[','(').replace(']',')')
if args.N!=None:
	args.N = args.N.replace('[','(').replace(']',')')

if args.cont:
	# считываем in
	with open('in', 'r') as inf:
		[dim,alg,syms,H,N,stop,threads,k_rules] = inf.read().split('""')
	dim = int(dim)
	stop = int(stop)
	threads = int(threads)
	
	# обновляем параметры
	if args.dim ==None: args.dim  = dim
	if args.alg ==None: args.alg  = alg.strip()
	if args.syms==None: args.syms = syms.strip()
	if args.H   ==None: args.H    = H
	if args.N   ==None: args.N    = N
	if args.stop==None: args.stop = stop
	if args.threads==None: args.threads = threads
	if args.k_rules==None: args.k_rules = k_rules
	
	# пишем in
	with open('in', 'w') as inf:
		print(
			args.dim,'""',
			args.alg,'""',
			args.syms if args.syms!=None else '{}','""',
			args.H,'""',
			args.N,'""',
			args.stop,'""',
			args.threads,'""',
			args.k_rules if args.k_rules!=None else '',
		file=inf
		)
		
	# устанавливаем code_name
	ln = list(map(lambda s: int(re.sub(r'code(.*)\.frm',r'\1',s)) ,filter(lambda s: re.match(r'code.*\.frm',s),os.listdir())))
	code_name = 'code'+str(1 if len(ln)==0 else max(ln)+1)+'.frm'
	
	# если нет outN-файлов
	if len(list(filter(lambda s: re.match(r'out.+',s),os.listdir())))==0:
		# создаем out0
		with open('out0', 'w') as outf:
			print(re.sub(r'\bI\b','i_',args.N.replace('\n', '').replace('[','(').replace(']',')')),file=outf)
			
	# удаляем out файл
	if 'out' in os.listdir():
		os.remove('out')
else:
	# проверяем обязательность параметров
	if args.dim==None:
		raise Exception('надо указать размерность --dim D (1d|2d|3d)')
	if args.alg==None:
		raise Exception('надо указать файл алгебры --alg file[.alg]')
	if args.H==None:
		raise Exception('надо указать гамильтониан --H expr')
	if args.N==None:
		raise Exception('надо указать наблюдаемую --N expr')
	if args.stop==None:
		raise Exception('надо указать номер последней итерации --stop N')
	if args.threads==None:
		args.threads = 1
	if args.k_rules!=None:
		args.k_rules = args.k_rules.strip()
		
	# очищает текущую директорию с вопросом
	lf = [ x for x in os.listdir() if x!='run.log' ]
	if len(lf)>0:
		if len(lf)>1 and not args.force:
			repl = ''
			while len(repl)!=1 or repl not in 'yYnN':
				print('хотите удалить все файлы (',len(lf),'шт) из',os.getcwd(),' (y/n) ?')
				repl =input()
			if repl in 'nN':
				print('чтобы продолжить вычисления, запустите программу с параметром --continue или -c',file=sys.stderr)
				print('чтобы не получать этот запрос, запустите программу с параметром --force или -f',file=sys.stderr)
				exit(1)
		for rf in lf:
			try:
				os.remove(rf)
			except Exception as e:
				print("can't remove",rf,file=sys.stderr)
		#continue
		
	# пишем in
	with open('in', 'w') as inf:
		print(
			args.dim,'""',
			args.alg,'""',
			args.syms if args.syms!=None else '{}','""',
			args.H,'""',
			args.N,'""',
			args.stop,'""',
			args.threads,'""',
			args.k_rules if args.k_rules!=None else '',
		file=inf
		)
		
	# устанавливаем code_name
	code_name = 'code1.frm'
	
	# создаем out0
	with open('out0', 'w') as outf:
		print(re.sub(r'\bI\b','i_',args.N.replace('\n', '').replace('[','(').replace(']',')')),file=outf)
	
print("arguments:",file=sys.stderr)
print("cont   ",args.cont   ,file=sys.stderr)
print("dim    ",args.dim    ,file=sys.stderr)
print("alg    ",args.alg    ,file=sys.stderr)
print("syms   ",args.syms   ,file=sys.stderr)
print("H      ",args.H      ,file=sys.stderr)
print("N      ",args.N      ,file=sys.stderr)
print("stop   ",args.stop   ,file=sys.stderr)
print("threads",args.threads,file=sys.stderr)
print("k_rules",args.k_rules,file=sys.stderr)
dim = args.dim
	
# ищем последний last_out
last_out_N = max(map(lambda s: int(re.sub(r'out(.+)',r'\1',s)) ,filter(lambda s: re.match(r'out.+',s),os.listdir())))
last_out = 'out'+str(last_out_N)

# если stop > last_out_N
if args.stop > last_out_N:
	# создаем code - code_name
	## считываем алгебру и создаем rules
	if not args.alg.endswith('.alg'):
		args.alg+='.alg'
	args.alg = '..'+os.sep+args.alg
	try:
		with open(args.alg,'r') as af:
	### строка с символами
			rule_syms = af.readline().strip() # <---
	### строка с коммут. операторами
			c_ops = list(map(lambda s: s.strip() , af.readline().split(','))) # <---
	### строка с некоммут. операторами
			s_ops = list(map(lambda s: s.strip() , af.readline().split(','))) # <---
	### правила до ---
			ind_patt = ','.join('i{}?'.format(i+1) for i in range(dim)) # индексный паттерн
			ind_repl = ','.join('i{}'.format(i+1) for i in range(dim)) # индексная замена
			cur_s = af.readline() # <---
			cur_s = cur_s[:-1] if cur_s[-1] in ' \n\r\t\v' else cur_s
			rule_list = []
			while cur_s and cur_s!='---':
				if '=' not in cur_s: print(repr(cur_s),file=sys.stderr)
				[lhs,rhs] = cur_s.split('=')
				for op in c_ops+s_ops:
					lhs = re.sub(r'\b{}\b'.format(op), op+'('+ind_patt+')', lhs)
					rhs = re.sub(r'\b{}\b'.format(op), op+'('+ind_repl+')', rhs)
				rule_list.append('id ifmatch->endarg '+lhs+'='+rhs)
				cur_s = af.readline() # <---
				cur_s = cur_s[:-1] if cur_s[-1] in ' \n\r\t\v' else cur_s
			rules = '\n'.join(rule_list)
	### ---
	### правила для коэф-тов
			cur_s = af.readline() # <---
			rule_k_list = []
			while cur_s:
				rule_k_list.append(cur_s)
				cur_s = af.readline() # <---
			k_rules = '\n'.join(rule_k_list).strip()
			
	except FileNotFoundError:
		print('не могу открыть файл алгебры',args.alg,file=sys.stderr)
		exit(1)
	print('rule_syms',rule_syms)
	print('c_ops    ',c_ops)	
	print('s_ops    ',s_ops)
	print('rules    ',rules)
	print('k_rules  ',k_rules)
	
	# проверяем допустимость имен операторов и смволов
	used_syms = 'cc,sc,CC,SC,koef,H,N'.split(',')
	used_sympatts = 'a,b,t,n,i,j,k,l'.split(',')
	for sym in c_ops + s_ops + rule_syms.split(',') + args.syms.replace('{','').replace('}','').split(',') :
		if sym in used_syms:
			print('illegal symbol',sym,file=sys.stderr)
			exit(1)
		for patt in used_sympatts:
			if re.match(patt+r'\d*',sym):
				print('illegal symbol',sym,file=sys.stderr)
				exit(1)
	
	## создаем код с заменами
	### alg		s1.alg
	### dim		1
	### c_ops	oc,ocp,ocpc
	### s_ops	sc,scp,scpc
	### rules	...
	### rule_syms	sym w;
	
	### ind_patt	i1?,i2?
	### ind_repl	i1,i2
	### ind_patt_n	n1?,n2?
	### ind_repl_n	n1,n2
	### min_ind	min_(n1,i1),min_(n2,i2)
	### ind_1	1,1
	### ind_n_minus_1	n1-1,n2-1
	### ind_i_minus_n	i1-n1,i2-n2
	
	### arg_syms	sym hx,hz,J;
	### H		1
	### last_out	out4
	code = \
'''
on stats;
off ThreadStats;

* === {alg} {dim}d ===

{rule_syms}
cfun   {c_ops},cc; *cten
set CC:{c_ops};
nfun   {s_ops},sc;
set SC:{s_ops};

Function S,SS,Comm;

auto Symbols a,b,t;
auto Symbol n,i,j,k,l; * indices

cfun koef;
polyfun koef;

*S n,n1,n2,x;
*Table ident(x?);  Fill ident() = x;
*Table prod(n?symbol_,n1?int_,n2?int_,x?);
*Fill prod() =
*  + theta_(n2-n1) * prod(n,n1,n2-1,x) * ident(x * replace_(n,n2))
*  + thetap_(n1-n2)
*;

*S x,y,z;
*Table if(x?int_,y?,z?);
*Fill if() = deltap_(x)*y+delta_(x)*z;

#procedure overlapping1d
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

#procedure overlapping2d
*--- overlapping ---
argument Comm;
    multiply S(1,1,1);
    repeat id S(k1?,k2?,t?)*cc?CC(i1?,i2?) = S(max_(k1,i1),max_(k2,i2),t*cc(i1,i2));
endargument;

*id Comm(a?,b?) = a*b;
*id S(?ss1)*S(?ss2) = Comm(S(?ss1),S(?ss2));
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

#procedure overlapping3d
*--- overlapping ---
argument Comm;
    multiply S(1,1,1,1);
    repeat id S(k1?,k2?,k3?,t?)*cc?CC(i1?,i2?,i3?) = S(max_(k1,i1),max_(k2,i2),max_(k3,i3),t*cc(i1,i2,i3));
endargument;

*id Comm(a?,b?) = a*b;
*id S(?ss1)*S(?ss2) = Comm(S(?ss1),S(?ss2));
id Comm(S(n1?,k1?,l1?,a1?),S(n2?,k2?,l2?,a2?)) = 
                  Comm(S(k1,l1,        a1),S(k2,l2,        a2))  + 
    sum_(i,1,n2-1,Comm(S(k1,l1,SS(i,1)*a1),S(k2,l2,        a2))) +
    sum_(i,1,n1-1,Comm(S(k1,l1,        a1),S(k2,l2,SS(i,1)*a2)));
argument Comm; argument S,3;
    repeat id SS(i?,t?)*cc?CC(j?,k?) = SS(i,t*cc(i+j,k));
    id SS(i?,a?) = a;
endargument;endargument;
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

#procedure multiply
*--- multiply ---
*id Comm(a?,b?) = S(a)*b-S(b)*a;
label repeat;
    id ifnomatch->endrepeat S(a?)*cc?CC[n]({ind_patt}) = S(a*SC[n]({ind_repl}));
    argument S;
*        id cc?CC(i1?)*sc?SC({ind_patt}) = 1;
{rules}
        id sc?SC[n?]({ind_patt}) = CC[n]({ind_repl});
        label endarg;
    endargument;
goto repeat;
label endrepeat;
id S(a?) = a;
*.sort
#endprocedure

#procedure trimS
*--- trimS ---
if(match(cc?CC({ind_patt})));
    id once cc?CC({ind_patt}) = S({ind_repl},cc({ind_repl}));
    repeat id S({ind_patt_n},t?)*cc?CC({ind_patt}) = S({min_ind},t*cc({ind_repl}));
    id ifmatch->endif S({ind_1},t?) = S(t);
        id S({ind_patt_n},t?) = S({ind_n_minus_1},1)*t;
        repeat id S({ind_patt_n},t?)*cc?CC({ind_patt}) = S({ind_repl_n},t*cc({ind_i_minus_n}));
        id S({ind_patt_n},t?) = S(t);
    label endif;
endif;
#endprocedure

*--------------------------------------------------

{arg_syms}
* === H ===
Local H  = {H};
id S(a?)*b?=Comm(a,1)*koef(b);
id S(a?)=Comm(a,1);

.sort
skip;

* === N ===
Local N = 
#include {last_out}
;
if(0==match(S(a?)*koef(b?)));
    id S(a?)*b?=S(a)*koef(b);
endif;
*id S(a?)=S(a);

.sort
Skip; Nskip N;
'''.format(
alg		=args.alg
,dim		=args.dim
,c_ops		=','.join(c_ops)
,s_ops		=','.join(s_ops)
,rules		=rules
,rule_syms	='' if rule_syms=='' else 'sym {};'.format(rule_syms)

,ind_patt	=','.join('i{}?'.format(i+1) for i in range(dim)) #i1?,i2?
,ind_repl	=','.join('i{}'.format(i+1) for i in range(dim)) #i1,i2
,ind_patt_n	=','.join('n{}?'.format(i+1) for i in range(dim)) #n1?,n2?
,ind_repl_n	=','.join('n{}'.format(i+1) for i in range(dim)) #n1,n2
,min_ind	=','.join('min_(n{k},i{k})'.format(k=i+1) for i in range(dim)) #min_(n1,i1),min_(n2,i2)
,ind_1		=','.join('1'.format(i+1) for i in range(dim)) #1,1
,ind_n_minus_1	=','.join('n{}-1'.format(i+1) for i in range(dim)) #n1-1,n2-1
,ind_i_minus_n	=','.join('i{k}-n{k}'.format(k=i+1) for i in range(dim))#i1-n1,i2-n2

,arg_syms	='' if args.syms=='{}' else 'sym {};'.format(args.syms.replace('{','').replace('}',''))
,H		=args.H
,last_out	=last_out
)+\
''.join(
'''
* === iteration {it} ===

multiply left H;
id Comm(a?,b?)*S(t?) = Comm(a,b*t);
#call overlapping{dim}d
id Comm(a?,b?) = S(a)*b-S(b)*a;
#call multiply

*Print +f "<%W> %t";
.sort
skip; nskip N;

#call trimS
{k_rules}

*Print +f "<%W> %t";
.sort
Skip;

#write <out{it}> "%E" , N

.sort
Skip; nskip N;
'''.format(it=i,dim=dim,k_rules=
	'''
	argument koef;
		{r1}
		{r2}
	endargument;
	'''.format(r1=k_rules, r2=args.k_rules) if k_rules and args.k_rules else ''
) for i in range(last_out_N+1,args.stop) 
)+\
'''
* === iteration {it} ===

multiply left H;
id Comm(a?,b?)*S(t?) = Comm(a,b*t);
#call overlapping{dim}d
id Comm(a?,b?) = S(a)*b-S(b)*a;
#call multiply

*Print +f "<%W> %t";
.sort
skip; nskip N;

#call trimS
{k_rules}

*Print +f "<%W> %t";
.sort
Skip;

#write <out{it}> "%E" , N

.end
'''.format(it=args.stop,dim=dim,k_rules=
	'''
	argument koef;
		{r1}
		{r2}
	endargument;
	'''.format(r1=k_rules, r2=args.k_rules) if k_rules and args.k_rules else ''
)

	## записываем его
	with open(code_name,'w') as cf:
		cf.write(code)
	# вызываем code_name
	if args.threads==1:
		invoke = " {}form       -l {}".format('..{s}form{s}'.format(s=os.sep),             code_name)
		print('run form:',invoke,file=sys.stderr)
		os.system(invoke)
	else:
		invoke = "{}tform -w{} -l {}".format('..{s}form{s}'.format(s=os.sep),args.threads,code_name)
		print('run form:',invoke,file=sys.stderr)
		os.system(invoke)


# преобразовываем stop в формат математики, если он меньше 100Мб
if os.path.getsize('out{}'.format(args.stop))<100_000_000:
	with open('out{}'.format(args.stop), 'r') as f2:
		with open('out', 'w') as f1:
			f1.write(re.sub(r'[ \n\r\t\v]','',re.sub(r'\bi_\b','I',f2.read().replace('(','[').replace(')',']'))))
else:
	print('file "out" too large for mathematica',file=sys.stderr)
