# -*- coding: utf-8 -*-
import requests, sys, re, json
import unicodedata
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, uic


listMesures = ['cuillère à café','cuillères à café', 'c.c.', 'cuillère à dessert','cuillères à dessert', 'cuillère à soupe','cuillères à soupe',
                 'c.s.', 'tasse à café','tasses à café', 'bol','bols', 'verre à moutarde','verres à moutarde',
                 'verre à liqueur', 'grand verre', 'gallon', 'tasse', 'pincée', 'grammes',' g)','g ',' g ', 'litres', ' l ', ' cl', ' ml', ' dl', 'botte',
                 'kilo ','demi ', 'verre ','m.g.','poignée ','grosse ','petite ','petit ', 'quelques ','brins ','environ ','morceau ','quart ','demi ','trait ','petites ']
listeArticles = [" de ", " d’", '(',')', '®', '%',' le ', 'un ',' d ']
listeCourses = []


class Yara(QtWidgets.QMainWindow):
    def __init__(self):
        super(Yara, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('yara.ui', self) # Load the .ui file
        
        #gererla validation des recettes
        self.validRecette = self.findChild(QtWidgets.QPushButton, 'ValidRecettes')
        self.validRecette.clicked.connect(self.validRecettePressed)
        
        #gérer les inputs text
        self.lundiMidi = self.findChild(QtWidgets.QLineEdit, 'lundiMidi')
        self.lundiSoir = self.findChild(QtWidgets.QLineEdit, 'lundiSoir')
        self.mardiMidi = self.findChild(QtWidgets.QLineEdit, 'mardiMidi')
        self.mardiSoir = self.findChild(QtWidgets.QLineEdit, 'mardiSoir')
        self.mercrediMidi = self.findChild(QtWidgets.QLineEdit, 'mercrediMidi')
        self.mercrediSoir = self.findChild(QtWidgets.QLineEdit, 'mercrediSoir')
        self.jeudiMidi = self.findChild(QtWidgets.QLineEdit, 'jeudiMidi')
        self.jeudiSoir = self.findChild(QtWidgets.QLineEdit, 'jeudiSoir')
        self.vendrediMidi = self.findChild(QtWidgets.QLineEdit, 'vendrediMidi')
        self.vendrediSoir = self.findChild(QtWidgets.QLineEdit, 'vendrediSoir')
        self.samediMidi = self.findChild(QtWidgets.QLineEdit, 'samediMidi')
        self.samediSoir = self.findChild(QtWidgets.QLineEdit, 'samediSoir')
        self.dimancheMidi = self.findChild(QtWidgets.QLineEdit, 'dimancheMidi')
        self.dimancheSoir = self.findChild(QtWidgets.QLineEdit, 'dimancheSoir')

        #gerer la liste des ingredients
        self.ingredients = self.findChild(QtWidgets.QListWidget, 'listIngr')
        
        self.show() # Show the GUI
    
    def validRecettePressed(self):
        urlLundiM = self.lundiMidi.text()
        urlLundiS = self.lundiSoir.text()
        urlMardiM = self.mardiMidi.text()
        urlMardiS = self.mardiSoir.text()
        urlMercrediM = self.mercrediMidi.text()
        urlMercrediS = self.mercrediSoir.text()
        urlJeudiM = self.jeudiMidi.text()
        urlJeudiS = self.jeudiSoir.text()
        urlVendrediM = self.vendrediMidi.text()
        urlVendrediS = self.vendrediSoir.text()
        urlSamediM = self.samediMidi.text()
        urlSamediS = self.samediSoir.text()
        urlDimancheM = self.dimancheMidi.text()
        urlDimancheS = self.dimancheSoir.text()

        if urlLundiM:
            self.FindIngredient(urlLundiM)
        if urlLundiS:
            self.FindIngredient(urlLundiS)
        if urlMardiM:
            self.FindIngredient(urlMardiM)
        if urlMardiS:
            self.FindIngredient(urlMardiS)
        if urlMercrediM:
            self.FindIngredient(urlMercrediM)
        if urlMercrediS:
            self.FindIngredient(urlMercrediS)
        if urlJeudiM:
            self.FindIngredient(urlJeudiM)
        if urlJeudiS:
            self.FindIngredient(urlJeudiS)
        if urlVendrediM:
            self.FindIngredient(urlVendrediM)
        if urlVendrediS:
            self.FindIngredient(urlVendrediS)
        if urlSamediM:
            self.FindIngredient(urlSamediM)
        if urlSamediS:
            self.FindIngredient(urlSamediS)
        if urlDimancheM:
            self.FindIngredient(urlDimancheM)
        if urlDimancheS:
            self.FindIngredient(urlDimancheS)
            
        self.ingredients.clear()
        for elmt in listeCourses:
            self.ingredients.addItem(elmt)

    def formatString(self,nomString):
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

    def cleanIngredients(self,ingr):
        for mesure in listMesures:
            ingr = ingr.replace(mesure,' ')
        for article in listeArticles:
            ingr = ingr.replace(article,' ')
        cleaningr = ''.join([i for i in ingr if not i.isdigit()])
        cleaningr = cleaningr.strip()
        return cleaningr

    def getMarmiton(self,codeRecette):
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

    def getKonbini(self,codeRecette):
        response = requests.get(codeRecette)
        soup = BeautifulSoup(response.content,"html.parser")
        listElements = soup.find_all('li',attrs={'class': None})
        ListmIngredients = []
        for ingredient in listElements:
            ListmIngredients += ingredient
        return ListmIngredients

    def getSlate(self,codeRecette):
        response = requests.get(codeRecette)
        soup = BeautifulSoup(response.content,"html.parser")
        listElements = soup.find_all('li',attrs={'class': None})
        ListmIngredients = []
        for ingredient in listElements:
            ListmIngredients += ingredient
        return ListmIngredients

    def getMrCuisine(self,codeRecette):
        response = requests.get(codeRecette)
        soup = BeautifulSoup(response.content,"html.parser")
        globalElements = soup.findAll('div', attrs={'class':'recipe--ingredients-html-item col-md-8'})
        ListmIngredients = []
        for tempelements in globalElements:
            listElements = tempelements.find_all('li')
            for ingredient in listElements:
                ListmIngredients += ingredient
        return ListmIngredients

    def FindIngredient(self,recette):
        if 'marmiton' in recette:
            ListmIngredients = self.getMarmiton(recette)
            
        if 'konbini' in recette:
            ListmIngredients = self.getKonbini(recette)
        
        if 'slate' in recette:
            ListmIngredients = self.getSlate(recette)

        if 'monsieur-cuisine' in recette:
            ListmIngredients = self.getMrCuisine(recette)

        addUnique = True
        for uniqueIngr in ListmIngredients:
            uniqueIngr = self.cleanIngredients(uniqueIngr)
            uniqueIngr = self.formatString(uniqueIngr)
            havetoadd = True
            for elmt in listeCourses:
                if elmt in uniqueIngr:
                    havetoadd=False
            if havetoadd:
                listeCourses.append(uniqueIngr)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Yara()
    app.exec_()
    
    #listUrl = sys.argv[1:]
    # for url in listUrl:
    #     FindIngredient(url)
    # print(listeCourses)