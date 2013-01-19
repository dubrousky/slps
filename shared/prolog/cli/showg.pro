:- ensure_loaded('../slps.pro').
% wiki: ShowG

:- 
   current_prolog_flag(argv,Argv),
   append(_,['--',LgfFile],Argv),
   loadXml(LgfFile,Xml),
   xmlToG(Xml,G),
   ppG(G),
   halt.
