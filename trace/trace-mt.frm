* run it: form -d iter=7 trace-mt.frm

Function S,SS,Comm;
cfun koef;

sym v,a,t;

Load ../out`iter'.sav;  * pick up one of the save files
L F = N;

id S(a?)=1;
id koef(t?) = t^2;

.sort
#write <out-`iter'.mt> "%E" F
.end
