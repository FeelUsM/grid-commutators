cfun   cx,cy,cz,cc; *cten
set CC:cx,cy,cz;

Function S,SS,Comm;
cfun koef;
polyfun koef;

sym v,a,b,t;

Load ../out`iter'.sav;  * pick up one of the save files
L F = N;

argument S; 
id cc?CC(a?,b?) = cc; 
endargument;


.sort
#write <out-`iter'.dxa> "%E" F
.end
