
  oc, ocp,ocpc
  sc, scp,scpc
  oc*  sc = 0;
  oc* scp = 1-ocpc;
  oc*scpc = oc;
 ocp*  sc = ocpc;
 ocp* scp = 0;
 ocp*scpc = 0;
ocpc*  sc = 0;
ocpc* scp = ocp;
ocpc*scpc = ocpc;
---
