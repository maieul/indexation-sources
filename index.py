#!/usr/bin/python
# -*- coding: utf-8 -*-
# auteur : Maïeul ROUQUETTE
# Licence http://creativecommons.org/licenses/by-sa/2.0/fr/
# version 2.3 pour Splitindex : on laisse faire le makeindex à la main


modification 	= 'principal.idx'		# A vous de modifier ici
splitindex		= 'sources'				# Le nom de l'index à concacéténer d'après splitindex	
seps				= ('&','-',',',';')		# ce qui peut séparer des nombres. Par exemple XX, 2
sepreference	= ('-','&')				# Ce qui peut séparer des références. Par exemple XX-XXI
#definition des fonctions

from roman import fromRoman
def trier(chaine):
	chaine = supprimer_accent(chaine)
	chaine = traiter_nombres(chaine)
	return chaine

def traiter_nombres(chaine):
	chaine = chaine.replace(' ','')
	global seps
	i = -1
	sep = 0 # position du separateur

	#1. convertir le nombre romain en entier
	for c in chaine: #parcourir la chaine
		i = i + 1
		if c in seps:
			morceau = chaine[sep:i].upper() 		#le morceau à traiter
			try:
				chaine = chaine[:sep] + str(fromRoman(morceau)) + chaine[i:]
			except:
				pass
			sep = i+1
		if sep == 0:
			try:
				chaine = str(fromRoman(chaine))
			except:
				pass 
		
	chaine = supprimer_sep_nombre(chaine)
	return chaine	

def ajouter_zeros(nombre):
	'''Ajout de zero devant un nombre'''
	return '0' * (30 - len(nombre)) + nombre 

def couper_chaine_nb_morceaux(chaine):
	# découpage de de la chaine, en morceau morceau
	global seps
	sep = 0
	i 	= -1
	morceaux = []
	for c in chaine:
		i = i +1
		if c in seps:
			morceaux.append(chaine[sep:i])
			morceaux.append(c)
			sep = i+1
		
	
	morceaux.append(chaine[sep:i+1])
	return morceaux	

def supprimer_sep_nombre(chaine):
	global sepreference
	for i in sepreference:
		sep = chaine.find(i)
		if sep > -1:
			break
		
	if sep == -1:
		try:
			int(chaine)
			return ajouter_zeros(chaine)
		except:
			return chaine
	morceaux = couper_chaine_nb_morceaux(chaine[0:sep])
	for i in range(len(morceaux)):
		#parcourir les morceaux
		if i%2 == 0: #dans le cas où on a affaire à un morceau
			try: 
				int(morceaux[i])
				morceaux[i] = ajouter_zeros(morceaux[i])
			except:
				# dès qu'un morceau n'est pas numérique, on renvoie la chaine brut
				return chaine
	chaine = ''.join(morceaux)
	return chaine
	
	
def supprimer_accent(chaine):
	'''http://www.peterbe.com/plog/unicode-to-ascii'''
	import unicodedata
	return unicodedata.normalize('NFKD', chaine).encode('ascii','ignore')


	
			
def convertir(index,split=False):
	'''Converti un fichier d'indexation pour remplacer trois série d'indexation par un nom'''
	
	import codecs
	lecture = codecs.open(index,encoding='utf-8')
	entrees = []			# tout les entree
	entree = []				# pour chaque entre, les trois variantes
	if split:
		sep 	= "\indexentry[" + split + "]{---}"
		debut 	= "\indexentry[" + split + "]{"
	else:
		sep 	= "\indexentry{---}"
		debut 	= "\indexentry{"
	for ligne in lecture:
		ligne = ligne.replace('|hyperpage','')
		if ligne[:len(sep)] == sep:
			entrees.append(concatener_entree(entree, split))
			entree = []
		elif ligne[:len(debut)] == debut:
			entree.append(ligne)
		else:
			entrees.append(ligne)
		
				
		
	lecture.close()
	ecriture = codecs.open(index,encoding='utf-8',mode='w')
	ecriture.writelines(entrees)
	ecriture.close()	

def concatener_entree(entre, split):
	'''Concatene 3 séries d'entrées en une seul'''
	
	if split :
		sorti = '\indexentry['+split+']{'
	else :
		sorti = '\'indexentry{'
	
	lg	  = len(sorti)
	infos = []
	for ligne in entre:
		texte = ligne[lg:ligne.rfind('}{')]
		arobase = texte.find('@')
		if arobase != -1:				# S'il y a un @
			infos.append(trier(texte[:arobase])+texte[arobase:])
		else:
			infos.append(trier(texte)+'@'+texte)
	sorti = sorti + '!'.join(infos)
	sorti = sorti + ligne[ligne.rfind('}{'):]
	return sorti
	
		

convertir(modification,splitindex)
def test():
	''' Système de test'''
	test_traiter_nombres = (('',''),
				('X',ajouter_zeros('10')),
				('XX-XX',ajouter_zeros('20')),
				('XX,1-XX',ajouter_zeros('20')+','+ ajouter_zeros('1')),
				('XX,x,11-XX',ajouter_zeros('20')+',' + ajouter_zeros('10') + ',' + ajouter_zeros('11')))	
	for i in test_traiter_nombres:
		if traiter_nombres(i[0]) !=i[1]:
			print 'erreur sur ' + i[0] + ' devrait être ' + i[1] + ' est ' + traiter_nombres(i[0])
	
#test()
