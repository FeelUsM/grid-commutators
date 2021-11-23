cfun   cx,cy,cz,cc; *cten
set CC:cx,cy,cz;
nfun   sx,sy,sz,sc;
set SC:sx,sy,sz;

Function S,SS,Comm;

auto Symbols a,b,t;
auto Symbol n,i,j,k; * indices

sym hz,hx,hy;

cfun koef;

#procedure fun
id S(a?)=1;
argument koef;
	id hy=1;
endargument;
id koef(t?) = t^2;
#endprocedure

#define iter "45"
#define last "90"

*-------------------------
*input:-99029152

#do N = 1,`last'

L L = 
#include - test`iter'-`last'
;
#call fun

format mathematica;
.sort
*11223344

#enddo

#write <out-`iter'.mt> "%E" L
.end
