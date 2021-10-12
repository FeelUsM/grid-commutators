
  oc, ocp,ocpc
  nc, scp,scpc
  oc*  nc = 0;
  oc* scp = 1-ocpc;
  oc*scpc = oc;
 ocp*  nc = ocpc;
 ocp* scp = 0;
 ocp*scpc = 0;
ocpc*  nc = 0;
ocpc* scp = ocp;
ocpc*scpc = ocpc;
---
