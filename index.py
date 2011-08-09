#!/usr/bin/python
# -*- coding: utf-8 -*-
# auteur : Maïeul ROUQUETTE
# Licence http://creativecommons.org/licenses/by-sa/2.0/fr/
# version 2.2 pour Splitindex : on laisse faire le makeindex à la main


modification 	= 'principal.idx'		# A vous de modifier ici
splitindex		= 'sources'			# Le nom de l'index à concacéténer d'après splitindex	

#definition des fonctions

import re

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
			infos.append(supprimer_accent(texte[:arobase-1])+texte[arobase-1:])
		else:
			infos.append(supprimer_accent(texte)+'@'+texte)
	sorti = sorti + '!'.join(infos)
	sorti = sorti + ligne[ligne.rfind('}{'):]
	return sorti
	
		

convertir(modification,splitindex)
		
