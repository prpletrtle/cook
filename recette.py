# -*- coding: utf-8 -*-
import requests, sys, re, json
import unicodedata
from bs4 import BeautifulSoup

# TODO
# gérer multiples url
# donner le total des ingredients pour la liste des recettes (genre 5 tomates etc ..)


def getMarmiton(codeRecette):
    response = requests.get(codeRecette)
    soup = BeautifulSoup(response.content)
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
    soup = BeautifulSoup(response.content)
    listElements = soup.find_all('li',attrs={'class': None})
    ListmIngredients = []
    for ingredient in listElements:
        ListmIngredients += ingredient
    return ListmIngredients

def getSlate(codeRecette):
    response = requests.get(codeRecette)
    soup = BeautifulSoup(response.content)
    listElements = soup.find_all('li',attrs={'class': None})
    ListmIngredients = []
    for ingredient in listElements:
        ListmIngredients += ingredient
    return ListmIngredients

def FindIngredient(recette):
    print(recette)
    if 'marmiton' in recette:
        ListmIngredients = getMarmiton(recette)
        
    if 'konbini' in recette:
        ListmIngredients = getKonbini(recette)
    
    if 'slate' in recette:
        ListmIngredients = getSlate(recette)

    print(ListmIngredients)

FindIngredient(sys.argv[1])
# TEST 
#FindIngredient('https://www.marmiton.org/recettes/recette_tagliatelles-carbonara-speciales_15725.aspx')