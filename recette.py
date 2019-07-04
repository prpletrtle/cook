# -*- coding: utf-8 -*-
import requests, sys, re, json
import unicodedata
from bs4 import BeautifulSoup

def FindIngredient(recette):
    recette = str(recette).replace(" ","_")
    response = requests.get(recette)
    soup = BeautifulSoup(response.content)
    scriptvar = soup.find_all('script')
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
                     mIngredient+=ingredient['unit']['name']
                 except KeyError as noUnit:
                     pass
                 print(mIngredient)
#FindIngredient(sys.argv)
# TEST 
FindIngredient('https://www.marmiton.org/recettes/recette_tagliatelles-carbonara-speciales_15725.aspx')