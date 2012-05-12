#!/Library/Frameworks/Python.framework/Versions/3.1/bin/python3
import os
import sys
sys.path.append(os.getcwd().split('slps')[0]+'slps/shared/python')
import slpsns
import xml.etree.ElementTree as ET
import BGF3,XBGF3,MBGF

namemap = {}

def applynamemap(e):
	if e.who()=='Expression':
		applynamemap(e.wrapped)
		return
	elif e.who()=='Nonterminal':
		if e.data in namemap:
			e.data = namemap[e.data]
		return
	print('[MBGF] applynamemap error:',e.who())
	sys.exit(1)

def wrapexp(exp,mod):
	if mod=='!':
		return str(exp)
	else:
		return str(exp)+mod
		# return '('+str(exp)+')'+mod

if __name__ == "__main__":
	if len(sys.argv)!=5:
		print('This tool needs MBGF as an input, XBGF as an output and a number of expected BGF input')
		print('\nUsage:')
		print('	',sys.argv[0],'<input-mbgf>','<in-num>','<out-num>','<output-xbgf>')
		sys.exit(1)
	else:
		mbgf = ET.parse(sys.argv[1])
		inname = sys.argv[2]
		outname = sys.argv[3]
		xbgf = XBGF3.Sequence()
		sources = {}
		predicates = []
		print('Reading the predicates...')
		for e in mbgf.findall('*'):
			if e.tag=='sources':
				predicates.append(MBGF.Sources(e))
				# for s in e.findall('src'):
				# 	sources[s.attrib['name']] = s.text
			elif e.tag=='naming-convention':
				predicates.append(MBGF.NamingConvention(e))
			elif e.tag=='name-bind':
				predicates.append(MBGF.NameBind(e))
			elif e.tag=='width':
				predicates.append(MBGF.Width(e))
			elif e.tag=='unification':
				predicates.append(MBGF.Unification(e))
			elif e.tag=='iteration':
				predicates.append(MBGF.Iteration(e))
			else:
				print('Predicate',e.tag,'not supported.')
				# print(sources)
				sys.exit(1)
		# executing
		print('Inferring unidirectional grammar transformations from',inname,'to',outname,'...')
		pbyid = {}
		unscheduled = []
		for p in predicates:
			# print(p.who(),'#',p.id,'@',p.depends)
			if p.who() == 'Sources':
				sources = p
			else:
				unscheduled.append(p.id)
				pbyid[p.id] = p
		scheduled = []
		while len(unscheduled)>0:
			for i in range(0,len(unscheduled)):
				candidate = pbyid[unscheduled[i]]
				if not(candidate.depends) or candidate.depends in scheduled:
					scheduled.append(unscheduled[i])
					unscheduled.remove(unscheduled[i])
					break
			else:
				print('Failed to schedule',unscheduled)
				sys.exit(2)
		print('Scheduled order:',scheduled)
		for id in scheduled:
			p = pbyid[id]
			print('[MBGF]',p.who(),'(',p.getSpecifics(),',',p.getData(inname),',',p.getData(outname),')', end=' ::= ')
			if p.who() == 'NamingConvention':
				if p.getData(inname) == p.getData(outname):
					print('id')
				else:
					print('mutation TODO')
			elif p.who() == 'NameBind':
				n1 = p.getData(inname)
				n2 = p.getData(outname)
				namemap[p.nt] = n2
				if n1 == n2:
					print('id')
				else:
					print('renameN(',n1,',',n2,')')
					ren = XBGF3.Step('rename')
					w = XBGF3.Wrapping('nonterminal')
					w.addChild(XBGF3.Leaf('from',n1))
					w.addChild(XBGF3.Leaf('to',n2))
					ren.addParam(w)
					xbgf.addStep(ren)
			elif p.who() == 'Width':
				exp = p.expr
				applynamemap(exp)
				e1 = p.getData(inname)
				e2 = p.getData(outname)
				i = p.scope # TODO
				yes = False
				if e1==e2:
					print('id')
				elif (e1,e2) in [('*','+'),('*','?'),('*','!'),('+','!'),('?','!')]:
					ren = XBGF3.Step('narrow')
					yes = True
				elif (e2,e1) in [('*','+'),('*','?'),('*','!'),('+','!'),('?','!')]:
					ren = XBGF3.Step('widen')
					yes = True
				else:
					print('ERROR: not in narrowing relation!')
					sys.exit(1)
				if yes:
					print(ren.name+'('+wrapexp(exp,e1)+','+wrapexp(exp,e2)+')')
					if e1=='!':
						ren.addParam(exp)
					elif e1=='+':
						p = BGF3.Plus()
						p.setExpr(exp)
						ren.addParam(BGF3.Expression(p))
					elif e1=='*':
						p = BGF3.Star()
						p.setExpr(exp)
						ren.addParam(BGF3.Expression(p))
					elif e1=='?':
						p = BGF3.Optional()
						p.setExpr(exp)
						ren.addParam(BGF3.Expression(p))
					else:
						print('ERROR: unknown in modifier!')
						sys.exit(1)
					if e2=='!':
						ren.addParam(exp)
					elif e2=='+':
						p = BGF3.Plus()
						p.setExpr(exp)
						ren.addParam(BGF3.Expression(p))
					elif e2=='*':
						p = BGF3.Star()
						p.setExpr(exp)
						ren.addParam(BGF3.Expression(p))
					elif e2=='?':
						p = BGF3.Optional()
						p.setExpr(exp)
						ren.addParam(BGF3.Expression(p))
					else:
						print('ERROR: unknown out modifier!')
						sys.exit(1)
					xbgf.addStep(ren)
			elif p.who() == 'Unification':
				n0 = p.nt
				n1 = p.getNTs(inname)
				n2 = p.getNTs(outname)
				if n0 in namemap:
					n3 = namemap[n0]
				else:
					n3 = n0
				if n1:
					# print('[MBGF] unification('+n1+','+n0+') ::= unite('+n1+','+n3+')')
					print('unite('+n1[0]+','+n3+')')
					ren = XBGF3.Step('unite')
					ren.addParam(XBGF3.Leaf('add',n1[0]))
					ren.addParam(XBGF3.Leaf('to',n3))
					xbgf.addStep(ren)
				elif n2:
					# print('[MBGF] unification('+n2+','+n0+') ::= split('+n3+','+n0+')')
					print('split('+n3+','+n0+')')
					ren = XBGF3.Step('split')
					ren.addParam(XBGF3.Leaf('nonterminal',n3))
					for q in p.getProds(outname):
						ren.addParam(q)
					for l in p.getScope(outname):
						ren.addParam(BGF3.LabelText(l.text))
					# print('!!!',e.findall('add')[outnum-1].attrib)
					# ren.addParam(XBGF3.Leaf('to',n3))
					xbgf.addStep(ren)
				else:
					# TODO: check for the situation when both n1 and n2 are not empty
					# print('[MBGF] unification(∅,'+n2+') ::= id')
					print('id')
			elif p.who() == 'Iteration':
				l = p.label
				n = p.nt
				s = p.sep
				k1 = p.getData(inname)
				k2 = p.getData(outname)
				if k1==k2:
					# print('[MBGF] iteration('+l+','+n+','+s+','+k1+','+k2+') ::= id')
					print('id')
				elif k1=='iterate' and k2.endswith('assoc'):
					if n in namemap:
						n1 = namemap[n]
					else:
						n1 = n
					if s in namemap:
						s1 = namemap[s]
					else:
						s1 = s
					# print('[MBGF] iteration('+l+','+n+','+s+','+k1+','+k2+') ::= '+k2+'(['+l+'] '+n1+' ← '+n1+' '+s1+' '+n1+')')
					print(k2+'(['+l+'] '+n1+' ← '+n1+' '+s1+' '+n1+')')
					ren = XBGF3.Step(k2)
					p = BGF3.Production()
					p.setLabel(l)
					p.setNT(n1)
					e = BGF3.Sequence()
					e2 = BGF3.Nonterminal()
					e2.setName(n1)
					e.add(BGF3.Expression(e2))
					if s:
						e2 = BGF3.Nonterminal()
						e2.setName(s1)
						e.add(BGF3.Expression(e2))
					e2 = BGF3.Nonterminal()
					e2.setName(n1)
					e.add(BGF3.Expression(e2))
					p.setExpr(BGF3.Expression(e))
					ren.addParam(p)
					xbgf.addStep(ren)
				elif k1.endswith('assoc') and k2=='iterate':
					if n in namemap:
						n1 = namemap[n]
					else:
						n1 = n
					if s in namemap:
						s1 = namemap[s]
					else:
						s1 = s
					if s1:
						ass = n1+' ('+s1+' '+n1+')*'
					else:
						ass = n1+'+'
					# print('[MBGF] iteration('+l+','+n+','+s+','+k1+','+k2+') ::= iterate(['+l+'] '+n1+' ← '+ass+')')
					print('iterate(['+l+'] '+n1+' ← '+ass+')')
					ren = XBGF3.Step('iterate')
					p = BGF3.Production()
					p.setLabel(l)
					p.setNT(n1)
					if s1:
						# N (S N)*
						e = BGF3.Sequence()
						e2 = BGF3.Nonterminal()
						e2.setName(n1)
						e.add(BGF3.Expression(e2))
						e3 = BGF3.Sequence()
						e4 = BGF3.Nonterminal()
						e4.setName(s1)
						e3.add(BGF3.Expression(e4))
						e3.add(BGF3.Expression(e2))
						e5 = BGF3.Star()
						e5.setExpr(BGF3.Expression(e3))
						e.add(BGF3.Expression(e5))
					else:
						# N+
						e = BGF3.Plus()
						e2 = BGF3.Nonterminal()
						e2.setName(n1)
						e.setExpr(BGF3.Expression(e2))
					p.setExpr(BGF3.Expression(e))
					ren.addParam(p)
					xbgf.addStep(ren)
				else:
					print('PROBLEM')
					sys.exit(1)
			else:
				print('UNKNOWN COMMAND')
		ET.ElementTree(xbgf.getXml()).write(sys.argv[4])
		print('Success',predicates)
        