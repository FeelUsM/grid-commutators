cfun   cx,cy,cz,cc; *cten
set CC:cx,cy,cz;
nfun   sx,sy,sz,sc;
set SC:sx,sy,sz;

Function S,SS,Comm;

auto Symbols a,b,t;
auto Symbol n,i,j,k; * indices

sym hz,hx,hy;

cfun koef;


L L =
#include inctmp
;

id S(a?)=1;
argument koef;
	id hx=1;
	id hy=1;
	id hz=1;
endargument;
id koef(t?) = t^2;

*Print;
.sort
#append <rez>
#write <rez> "%E" , L
#close <rez>
.end