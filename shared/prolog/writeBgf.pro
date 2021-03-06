%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Map Prolog-based BGF representation to XML representation %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% wiki: WriteBGF

gToXml(g(Rs1,Ps1),G)
 :-
    maplist(rToXml,Rs1,Rs2),
    maplist(pToXml,Ps1,Ps2),
    append(Rs2,Ps2,Kids),
    e(bgf:grammar,[],Kids,G).

rToXml(N,R)
 :-
    e(root,[],[N],R).   

pToXml(p(As1,V,X1),P)
 :-
    ( member(l(L),As1) -> 
          ( 
            As2 = [LA],
            e(label,[],[L],LA)
          )
        ;
          As2 = []
    ),
    e(nonterminal,[],[V],N),
    xToXml(X1,X2),
    xToExpression(X2,X3),
    append(As2,[N,X3],Cs),
    e(bgf:production,[],Cs,P).

xToXml(true,X) 
 :-
    e(epsilon,[],[],X).

xToXml(fail,X) 
 :-
    e(empty,[],[],X).

xToXml(t(T),X) 
 :-
    e(terminal,[],[T],X).

xToXml(n(N),X) 
 :-
    e(nonterminal,[],[N],X).

xToXml(a,X) 
 :-
    e(any,[],[],X).

xToXml(v(T),X) 
 :-
    e(value,[],[T],X).

xToXml(s(S,M),X) 
 :-
    xToXml(M,X1),
    xToExpression(X1,X2),
    e(selector,[],[S],S1),
    e(selectable,[],[S1,X2],X).

xToXml(','(Ms),X) 
 :-
    maplist(xToXml,Ms,Xs1),
    maplist(xToExpression,Xs1,Xs2),
    e(sequence,[],Xs2,X).

xToXml(';'(Ms),X) 
 :-
    maplist(xToXml,Ms,Xs1),
    maplist(xToExpression,Xs1,Xs2),
    e(choice,[],Xs2,X).

xToXml('?'(M),X) 
 :-
    xToXml(M,X1),
    xToExpression(X1,X2),
    e(optional,[],[X2],X).

xToXml('*'(M),X) 
 :-
    xToXml(M,X1),
    xToExpression(X1,X2),
    e(star,[],[X2],X).

xToXml(sls(M1,M2),X) 
 :-
    xToXml(M1,X1),
    xToXml(M2,X2),
    xToExpression(X1,X3),
    xToExpression(X2,X4),
    e(sepliststar,[],[X3,X4],X).

xToXml(slp(M1,M2),X) 
 :-
    xToXml(M1,X1),
    xToXml(M2,X2),
    xToExpression(X1,X3),
    xToExpression(X2,X4),
    e(seplistplus,[],[X3,X4],X).

xToXml({M},X) 
 :-
    xToXml(M,X1),
    xToExpression(X1,X2),
    e(marked,[],[X2],X).

xToXml('+'(M),X) 
 :-
    xToXml(M,X1),
    xToExpression(X1,X2),
    e(plus,[],[X2],X).

xToExpression(X1,X2)
 :-
    e(bgf:expression,[],[X1],X2).
