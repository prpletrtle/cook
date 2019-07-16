# -*- coding: utf-8 -*-
import requests, sys, re, json
import unicodedata
from bs4 import BeautifulSoup

# TODO
# donner le total des ingredients pour la liste des recettes (genre 5 tomates etc ..)

listMesures = ['cuillère à café','cuillères à café', 'c.c.', 'cuillère à dessert','cuillères à dessert', 'cuillère à soupe','cuillères à soupe',
                 'c.s.', 'tasse à café','tasses à café', 'bol','bols', 'verre à moutarde','verres à moutarde',
                 'verre à liqueur', 'grand verre', 'gallon', 'tasse', 'pincée', 'grammes',' g)','g ',' g ', 'litres', ' l ', ' cl', ' ml', ' dl', 'botte']
listeArticles = [" de ", " d’", '(',')', '®', '%']
listeCourses = []

def formatString(nomString):
	# Vire les espaces au debut et à la fin, vire les tirets et les
	# underscores. Et met en minuscule
	if (nomString is not None):
		try:
			nomString = nomString.lower()
			nomString = nomString.strip()
			nomString = nomString.replace("_", " ")
			nomString = nomString.replace("-", " ")
			nomString = nomString.replace("/", " ")
			nomString = nomString.replace("'", " ")
		except TypeError:
			pass
		except AttributeError:
			print(nomString)
			pass

	return nomString

def cleanIngredients(ingr):
    for mesure in listMesures:
        ingr = ingr.replace(mesure,' ')
    for article in listeArticles:
        ingr = ingr.replace(article,' ')
    cleaningr = ''.join([i for i in ingr if not i.isdigit()])
    cleaningr = cleaningr.strip()
    return cleaningr

def getMarmiton(codeRecette):
    response = requests.get(codeRecette)
    soup = BeautifulSoup(response.content,"html.parser")
    scriptvar = soup.find_all('script')
    ListmIngredients = []
    for script in scriptvar:
        if "ingredientsGroups" in str(script):
             script = str(script)
             listingredients = re.findall('(ingredient_group_items.*?\}\])', script, re.MULTILINE | re.DOTALL)
             mtrueList = listingredients[0]
             mtrueList = mtrueList.replace('ingredient_group_items":','')
             mjson = json.loads(mtrueList)
             for ingredient in mjson:
                 mIngredient = ingredient['ingredient']['name']
                 try:
                     mIngredient+= " " + str(ingredient['quantity'])
                 except KeyError as noQuantity:
                     pass
                 
                 try:
                     mIngredient+= " " +ingredient['unit']['name']
                 except KeyError as noUnit:
                     pass
                 ListmIngredients.append(mIngredient)
    return ListmIngredients

def getKonbini(codeRecette):
    response = requests.get(codeRecette)
    soup = BeautifulSoup(response.content,"html.parser")
    listElements = soup.find_all('li',attrs={'class': None})
    ListmIngredients = []
    for ingredient in listElements:
        ListmIngredients += ingredient
    return ListmIngredients

def getSlate(codeRecette):
    response = requests.get(codeRecette)
    soup = BeautifulSoup(response.content,"html.parser")
    listElements = soup.find_all('li',attrs={'class': None})
    ListmIngredients = []
    for ingredient in listElements:
        ListmIngredients += ingredient
    return ListmIngredients

def getMrCuisine(codeRecette):
    response = requests.get(codeRecette)
    soup = BeautifulSoup(response.content,"html.parser")
    globalElements = soup.findAll('div', attrs={'class':'recipe--ingredients-html-item col-md-8'})
    ListmIngredients = []
    for tempelements in globalElements:
        listElements = tempelements.find_all('li')
        for ingredient in listElements:
            ListmIngredients += ingredient
    return ListmIngredients

def FindIngredient(recette):
    if 'marmiton' in recette:
        ListmIngredients = getMarmiton(recette)
        
    if 'konbini' in recette:
        ListmIngredients = getKonbini(recette)
    
    if 'slate' in recette:
        ListmIngredients = getSlate(recette)

    if 'monsieur-cuisine' in recette:
        ListmIngredients = getMrCuisine(recette)

    addUnique = True
    for uniqueIngr in ListmIngredients:
        uniqueIngr = cleanIngredients(uniqueIngr)
        uniqueIngr = formatString(uniqueIngr)
        havetoadd = True
        for elmt in listeCourses:
            if elmt in uniqueIngr:
                havetoadd=False
        if havetoadd:
            listeCourses.append(uniqueIngr)


listUrl = sys.argv[1:]
for url in listUrl:
    FindIngredient(url)
print(listeCourses)