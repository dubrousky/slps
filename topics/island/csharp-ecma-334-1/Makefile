all:
	make cs.html

cs.1.bgf:
	cp ../../grammars/csharp/ecma-334-1/grammar.bgf cs.1.bgf

cs.2.bgf: cs.1.bgf
	subgrammar cs.1.bgf compilation-unit cs.2.bgf

cs.3.bgf: cs.2.bgf refactor.using.exbgf
	exbgf2xbgf refactor.using.exbgf refactor.using.xbgf
	xbgf refactor.using.xbgf cs.2.bgf cs.3.bgf

cs.4.bgf: cs.3.bgf refactor.global.exbgf
	exbgf2xbgf refactor.global.exbgf refactor.global.xbgf
	xbgf refactor.global.xbgf cs.3.bgf cs.4.bgf

cs.5.bgf: cs.4.bgf refactor.namespace.exbgf
	exbgf2xbgf refactor.namespace.exbgf refactor.namespace.xbgf
	xbgf refactor.namespace.xbgf cs.4.bgf cs.5.bgf

cs.6.bgf: cs.5.bgf skeletify.exbgf
	exbgf2xbgf skeletify.exbgf skeletify.xbgf
	xbgf skeletify.xbgf cs.5.bgf cs.6.bgf

cs.7.bgf: cs.6.bgf
	subgrammar cs.6.bgf compilation-unit cs.7.bgf

cs.html: cs.7.bgf
	bgf2html cs.7.bgf cs.html

clean:
	rm -f ~* *.html *.bgf