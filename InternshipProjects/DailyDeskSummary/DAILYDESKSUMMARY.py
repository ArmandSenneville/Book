##=============================================================================##
##Imports##

import pandas as pd
pd.options.mode.chained_assignment = None
import datetime
from forex_python.converter import CurrencyRates 
from easygui import *
import os
import os.path
import webbrowser
import glob
from calendar import month_name
import shutil
from colour import Color
import json
import seaborn as sns
import time
import numpy as np
import matplotlib.pyplot as plt
import random
from fpdf import FPDF
import plotly.express as px
import re

##=============================================================================##
##Definitions##

date_format = "%d-%m-%Y"
file_format = ".xlsx"

list_months = [
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
]

liste_mois = [
    'Janvier','Février','Mars','Avril','Mai','Juin',
    'Juillet','Août','Septembre','Octobre','Novembre','Décembre'
]

directory = os.getcwd()
workingproject = directory + "\DataAnalyst"
Datatype = workingproject + "\RawData"

#Définitions pour le pdf#
WIDTH = 210
HEIGHT = 297

##=============================================================================##
##Quelle période##

text = "Pour quelle période souhaitez-vous obtenir un étude ?"
title = "Results getter"
choices = ["Aujourd'hui","Une semaine", "Un mois", "Une année","Une date spécifique","Entre deux dates"]
output = choicebox(text, title, choices)
title = "Message Box"
message = "Vous allez voir les résultats pour  : " + str(output)
msg = msgbox(message, title)

##=============================================================================##
##Fonctions##

def lemois(month_number):
    '''Cette fonction prend pour agrument un numéro de mois
    et retourne le nom de ce mois'''
# def = definition de la fonction , () est l'argument de la fonction ie f(x)
    try:
#try check si la fonction marche , si pas c le cas alors ça passe à except
        month_number = int(month_number)
        try:
            return month_name[month_number]
        except IndexError:
            print("'{}' is not a valid month number".format(month_number))
        except TypeError :
            print("'{}' is not an integer".format(month_number))
    except:
        print("'{}' is not a number".format(month_number))

def month_translator(month_name): 
    '''Cette fonction prend pour argument le nom d'un mois en Anglais avec pour
    première lettre une majuscule et retourne le nom de ce mois en Français'''
    if month_name in list_months:
        poitou_charentes = list_months.index(month_name)
        month_name = liste_mois[poitou_charentes]
        return month_name
    else:
        print("""{} n'est pas un mois de l'année en anglais""".format(month_name))
        return None
    
def mois_vers_numéro(mois):
    '''Cette fonction prend pour argument le nom d'un mois, le met au bon format
    pour le comparer à la liste des noms de mois et retourne le numéro du mois
    '''
    try : 
        mois = str(mois)
        mois = mois.lower()
        mois = mois.capitalize()
        if mois in liste_mois:
            nombre = liste_mois.index(mois) + 1
            if nombre < 10:
                nombre = '0{}'.format(str(nombre))
            return str(nombre)
        else:
            print(r"Votre entrée n'est pas un mois de l'année")
    except: 
        print('pas bon input')
        
def jours_dla_semaine(jour):
    ''' Cette fonction prend pour argument un jour et
    retourne une liste des jours travaillés dans la semaine
    '''
    if jour.strftime('%A') == 'Monday':
        weekdays = [jour + datetime.timedelta(days=i) for i in range(5)]
    elif jour.strftime('%A') == 'Tuesday':
        weekdays = [jour + datetime.timedelta(days=-1)]
        weekdays.extend([jour + datetime.timedelta(days=i) for i in range(4)])
    elif jour.strftime('%A') == 'Wednesday':
        weekdays = [jour + datetime.timedelta(days=-i) for i in range(3)]
        weekdays.extend([jour + datetime.timedelta(days=i+1) for i in range(2)])
        weekdays.sort()
    elif jour.strftime('%A') == 'Thursday':
        weekdays = [jour + datetime.timedelta(days=-i) for i in range(4)]
        weekdays.extend([jour + datetime.timedelta(days=i+1) for i in range(1)])
        weekdays.sort()
    elif jour.strftime('%A') == 'Friday':
        weekdays = [jour + datetime.timedelta(days=-i) for i in range(5)]
        weekdays.sort()
    elif jour.strftime('%A') == 'Saturday':
        weekdays = [jour + datetime.timedelta(days=-i) for i in range(6)]
        weekdays.remove(weekdays[0])
        weekdays.sort()
    elif jour.strftime('%A') == 'Sunday':
        weekdays = [jourji2 + datetime.timedelta(days=-i) for i in range(7)]
        weekdays.remove(weekdays[0])
        weekdays.remove(weekdays[0])
        weekdays.sort()
    
    return [a.strftime("%d-%m-%Y") for a in weekdays]

def CA_Calculus(dataframe):
    '''Cette focntion prend un dataframe pandas et calcule le total du nominal et des commissions sur une période donnée
    '''
    if isinstance(dataframe, pd.DataFrame):
        c = CurrencyRates()
        dataframe['Dates'] = pd.to_datetime(dataframe['Creation Time']).dt.date
        dataframe = dataframe[dataframe['% Exec'] > 0]
        dataframe = dataframe[dataframe['ClientId'] != 'ERROR']
        indexCcy = dataframe[ dataframe['Ccy'].isnull()].index
        dataframe.drop(indexCcy , inplace=True)
        bonne_liste = ['Creation Time','FilledQty','FilledAvgPx','Ccy','ClientId','Dates']
        zecolonnes = list(dataframe)
        dataframe.drop([column_name for column_name in zecolonnes if column_name not in bonne_liste], axis = 1, inplace = True)
        dataframe = dataframe.replace(to_replace='GBX', value='GBP', regex=True)
        dataframe = dataframe.replace(to_replace='ZAC', value='ZAR', regex=True)
        dataframe['Amount'] = dataframe['FilledQty']*dataframe['FilledAvgPx']
        dataframe['Amount'] = [row[0]*0.01 if row[1] in ('GBP','ZAR') else row[0] for row in zip(dataframe['Amount'], dataframe['Ccy'])]
        directory = os.getcwd()
        comissions_path = directory + """\{}.xlsx""".format('commisions')
        df2 = pd.read_excel(r'{}'.format(comissions_path), header = None)
        df2.rename(columns = {0:'ClientId', 1:'Commission'}, inplace = True)
        com = {}
        for ind in df2.index:
            com[df2['ClientId'][ind]] = df2['Commission'][ind]
        keys = [i for i in com.keys()]
        dataframe['Bips'] = [x*0.0001 if x==float(x) else com[y]*0.0001 if y in keys else 5*0.0001 for (y,x) in zip(dataframe['ClientId'],dataframe['CE']) ]
        dataframe['Conversion Rate'] = [c.get_rate(str(row[0]),'EUR',row[1]) for row in zip(dataframe['Ccy'], dataframe['Dates'])]
        dataframe['Converted Amount'] = dataframe['Amount']*dataframe['Conversion Rate']
        dataframe['Commission'] = dataframe['Converted Amount'] * dataframe['Bips']
    else:
        print(r"C'est pas un dataframe")
    return (int(sum(dataframe['Commission']),int(sum(dataframe['Converted Amount']))))
        
def emplacement_enième_substr(str1,str2,occurence):
    '''
    Cette fonction prend pour argument deux chaînes de caractères et un numéro d'occurence,
    la fonction va chercher l'emplacement de la n-ième occcurence de la deuxième chaîne au sein de la première
    et le retourner
    '''
    inilist = [m.start() for m in re.finditer(str2, str1)]
    if len(inilist)>= occurence:        
        return inilist[occurence-1]
    else:
        return None

##=============================================================================##
##Classes##

#permet de construire le pdf final
class PDF(FPDF):
    def __init__(self, **kwargs):
        super(PDF, self).__init__(**kwargs)
        #adding custom font
        self.add_font('Ticketing','',
                     r'C:\Users\msp.intern5\Desktop\Stage Market\Projet_2_Analyse_données\PDFWIP\ticketing\TICKETING\Ticketing.ttf', uni = True)
        
     #ajoute un entête    
    def header(self):
        self.image('C:\\Users\\msp.intern5\\Desktop\\Stage Market\\Projet_2_Analyse_données\\header2.png',0, 0,WIDTH)
        if self.page_no() == 1:
            self.set_font('Ticketing', 'U', 16)
            self.set_text_color(51, 51, 51)
            self.set_x(0)
            self.set_y(45)
            self.cell(0,20, titre_du_pdf, align = 'L')
    #pied de page
    def footer(self):
        self.image('C:\\Users\\msp.intern5\\Desktop\\Stage Market\\Projet_2_Analyse_données\\footer.png',0,HEIGHT-24,WIDTH )
        self.set_x(0)
        self.set_y(HEIGHT-34)
        self.set_font('Ticketing', '', 8)
        self.set_text_color(51, 51, 51)
        self.cell(self.get_string_width(str('Page ' + str(self.page_no()) + '/{nb}')), 10, 'Page ' + str(self.page_no()) + '/{nb}', 0,0, 'C')
    
    #construit le titre des graphs
    def graph_title(self, graph_titre):
        self.set_font('Ticketing','',20)
        self.set_fill_color(51, 51, 51)
        self.set_x(0)
        self.set_y(60)
        self.cell(txt = graph_titre)
        self.ln()
    
    #Ajoute des infos supplémentaires sur les graphs
    def graph_cestquoi(self,graph_description):
        self.set_font('Ticketing','',10)
        self.set_text_color(51, 51, 51)
        if graph_description.count("\n") >= 25:
            spot = emplacement_enième_substr(graph_description, "\n", 2)
            head_description = graph_description[:spot]
            corps_decription = graph_description[spot+1:]
            self.set_xy(15,190)
            self.multi_cell(0,3,txt = head_description, align = 'L')
            
            spot2 = emplacement_enième_substr(corps_decription, "\n", 22)
            sub_description = corps_decription[:spot2]
            sub_descritpion2 = corps_decription[spot2 + 1 : ]
            
            self.set_xy(15,200)
            self.multi_cell(85,3,txt = sub_description, align = 'L')
            self.set_xy(101,200)
            self.multi_cell(85,3,txt = sub_descritpion2, align = 'L')
        else:
            self.set_xy(15,190)
            self.multi_cell(0,3,txt = graph_description)
        self.ln()
     
    #insère le graph dans la page
    def graph_body(self, graph_path):
        self.image(str(graph_path),(WIDTH-(WIDTH-50))/2, self.get_y(), WIDTH-50)
        self.ln()
        
    def graph_body_special(self, graph_path):
        self.image(str(graph_path),(WIDTH-(WIDTH-100))/2, self.get_y(), WIDTH-100)
        self.ln()
            
    #met les trois éléments précédents dans le bon ordre
    def print_graph(self, graph_titre, graph_description, graph_path):
        if graph_titre == "Distribution des commissions en euro":
            self.add_page()
            self.graph_title(graph_titre)
            self.graph_body_special(graph_path)
            self.graph_cestquoi(graph_description)
                
        else:
            self.add_page()
            self.graph_title(graph_titre)
            self.graph_body(graph_path)
            self.graph_cestquoi(graph_description)
            

#classe qui permet la construction d'un graph en bulle            
class BubbleChart:
    def __init__(self, area, bubble_spacing=0):
        """
        Setup for bubble collapse.

        Parameters
        ----------
        area : array-like
            Area of the bubbles.
        bubble_spacing : float, default: 0
            Minimal spacing between bubbles after collapsing.

        Notes
        -----
        If "area" is sorted, the results might look weird.
        """
        area = np.asarray(area)
        r = np.sqrt(area / np.pi)

        self.bubble_spacing = bubble_spacing
        self.bubbles = np.ones((len(area), 4))
        self.bubbles[:, 2] = r
        self.bubbles[:, 3] = area
        self.maxstep = 2 * self.bubbles[:, 2].max() + self.bubble_spacing
        self.step_dist = self.maxstep / 2

        # calculate initial grid layout for bubbles
        length = np.ceil(np.sqrt(len(self.bubbles)))
        grid = np.arange(length) * self.maxstep
        gx, gy = np.meshgrid(grid, grid)
        self.bubbles[:, 0] = gx.flatten()[:len(self.bubbles)]
        self.bubbles[:, 1] = gy.flatten()[:len(self.bubbles)]

        self.com = self.center_of_mass()

    def center_of_mass(self):
        return np.average(
            self.bubbles[:, :2], axis=0, weights=self.bubbles[:, 3]
        )

    def center_distance(self, bubble, bubbles):
        return np.hypot(bubble[0] - bubbles[:, 0],
                        bubble[1] - bubbles[:, 1])

    def outline_distance(self, bubble, bubbles):
        center_distance = self.center_distance(bubble, bubbles)
        return center_distance - bubble[2] - \
            bubbles[:, 2] - self.bubble_spacing

    def check_collisions(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return len(distance[distance < 0])

    def collides_with(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        idx_min = np.argmin(distance)
        return idx_min if type(idx_min) == np.ndarray else [idx_min]

    def collapse(self, n_iterations=50):
        """
        Move bubbles to the center of mass.

        Parameters
        ----------
        n_iterations : int, default: 50
            Number of moves to perform.
        """
        for _i in range(n_iterations):
            moves = 0
            for i in range(len(self.bubbles)):
                rest_bub = np.delete(self.bubbles, i, 0)
                # try to move directly towards the center of mass
                # direction vector from bubble to the center of mass
                dir_vec = self.com - self.bubbles[i, :2]

                # shorten direction vector to have length of 1
                dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))

                # calculate new bubble position
                new_point = self.bubbles[i, :2] + dir_vec * self.step_dist
                new_bubble = np.append(new_point, self.bubbles[i, 2:4])

                # check whether new bubble collides with other bubbles
                if not self.check_collisions(new_bubble, rest_bub):
                    self.bubbles[i, :] = new_bubble
                    self.com = self.center_of_mass()
                    moves += 1
                else:
                    # try to move around a bubble that you collide with
                    # find colliding bubble
                    for colliding in self.collides_with(new_bubble, rest_bub):
                        # calculate direction vector
                        dir_vec = rest_bub[colliding, :2] - self.bubbles[i, :2]
                        dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))
                        # calculate orthogonal vector
                        orth = np.array([dir_vec[1], -dir_vec[0]])
                        # test which direction to go
                        new_point1 = (self.bubbles[i, :2] + orth *
                                      self.step_dist)
                        new_point2 = (self.bubbles[i, :2] - orth *
                                      self.step_dist)
                        dist1 = self.center_distance(
                            self.com, np.array([new_point1]))
                        dist2 = self.center_distance(
                            self.com, np.array([new_point2]))
                        new_point = new_point1 if dist1 < dist2 else new_point2
                        new_bubble = np.append(new_point, self.bubbles[i, 2:4])
                        if not self.check_collisions(new_bubble, rest_bub):
                            self.bubbles[i, :] = new_bubble
                            self.com = self.center_of_mass()

            if moves / len(self.bubbles) < 0.1:
                self.step_dist = self.step_dist / 2

    def plot(self, ax, labels, colors):
        """
        Draw the bubble plot.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
        labels : list
            Labels of the bubbles.
        colors : list
            Colors of the bubbles.
        """
        for i in range(len(self.bubbles)):
            circ = plt.Circle(
                self.bubbles[i, :2], self.bubbles[i, 2], color=colors[i])
            ax.add_patch(circ)
            ax.text(*self.bubbles[i, :2], labels[i],
                    horizontalalignment='center', verticalalignment='center')
            
##=============================================================================##
##Rangeur de fichier##
try:
    if output == "Aujourd'hui" :
        if os.path.exists(r'{}'.format(workingproject)) == False:
            os.mkdir(workingproject)
        if os.path.exists(r'{}'.format(Datatype)) == False:
            os.mkdir(Datatype)
        while True:
            #une boucle while True va tourner à l'infini jusqu'à ce qu'on lui dise d'arrêter, ici avec l'instruction break
            try:
                Datatype = workingproject + "\RawData"
                file_type = r'\*xlsx'
                files = glob.glob(Datatype + file_type)
                latest_file = max(files, key=os.path.getctime)
                #selectionne le fichier Xlsx
                #chemin path du fichier le plus récent
                df = pd.read_excel(r'{}'.format(latest_file))
                #df = data frame
                break
            except IOError:
                msgbox("Vous avez laissé votre fichier excel ouvert, fermez-le et cliquez sur OK","Le script n'a pas pu accéder au fichier","Ok")

        release_date = datetime.date.today()
        release_date = release_date.strftime(date_format)
        bs = release_date.split('-')
        current_day = bs[0]
        current_month = bs[1]
        current_year = bs[2]
        year_path = donnée_brute + '\{}'.format(current_year)
        zemois = lemois(current_month)
        current_month = month_translator(zemois)
        month_path = year_path + '\{}'.format(current_month)
        destination_path = month_path + '\{}.xlsx'.format(release_date)
        try:
            latest_file = max(files, key=os.path.getctime)
            if os.path.exists(r'{}'.format(month_path)) == True:
                shutil.move(latest_file, destination_path)
            elif os.path.exists(r'{}'.format(year_path)) == True:
                os.mkdir(month_path)
                shutil.move(latest_file, destination_path)
            else:
                os.mkdir(year_path)
                os.mkdir(month_path)
                shutil.move(latest_file, destination_path)
        except:
            print('Aucun fichier touvé')
except:
    print('Aucun fichier touvé, celui-ci a peu être déjà été rangé')
    
##=============================================================================##
##Constructeur du dataframe à étudier##

if output == "Aujourd'hui":
    release_date = datetime.date.today()
    release_date = release_date.strftime(date_format)
    bs = release_date.split('-')
    current_day = bs[0]
    current_month = bs[1]
    current_month = month_translator(lemois(current_month))
    current_year = bs[2]
    year_path = Datatype + "\{}".format(current_year)
    month_path = year_path + "\{}".format(current_month)
    file_type = r'\*xlsx'
    files = glob.glob(month_path + file_type)
    latest_file = max(files, key=os.path.getctime)
    df = pd.read_excel(r'{}'.format(latest_file))

elif output == "Entre deux dates":
    start_date = enterbox("À partir de quelle date souhaitez-vous voir les résultats ?","Résultats")
    end_date = enterbox("Jusqu'à quelle date souahitez-vous voir les résultats ?","Résultats")
    start_date = start_date.split('/')
    end_date = end_date.split('/')
    range_checker = (start_date[2] == end_date[2],
                     start_date[1] == end_date[1],
                     start_date[0] == end_date[0])
    if range_checker == (True,True,False):
        year_path = Datatype + "\{}".format(start_date[2])
        month_path = year_path + "\{}".format(month_translator(lemois(start_date[1])))
        file_list = os.listdir(month_path)
        lilist = [a.split(".")[0] for a in file_list]
        files_to_read = [item for item in lilist if int(start_date[0]) <= int(item.split('-')[0]) <= int(end_date[0])]

    elif range_checker == (True, False, False) or range_checker == (True, False, True):
        files_to_read = []
        year_path = Datatype + "\{}".format(start_date[2])
        les_mois = list(range(int(start_date[1]),int(end_date[1])+1))
        les_mois = [month_translator(lemois(i)) for i in les_mois]
        for mois in les_mois:
            month_path = year_path + "\{}".format(mois)
            if mois == les_mois[0]:
                file_list = os.listdir(month_path)
                lilist = [a.split(".")[0] for a in file_list]
                zefichiers = [item for item in lilist if int(start_date[0]) <= int(item.split('-')[0])]
                files_to_read.extend(zefichiers)
            elif mois == les_mois[len(les_mois)-1]:
                file_list = os.listdir(month_path)
                lilist = [a.split(".")[0] for a in file_list]
                zefichiers = [item for item in lilist if int(end_date[0]) >= int(item.split('-')[0])]
                files_to_read.extend(zefichiers)
            else:
                file_list = os.listdir(month_path)
                lilist = [a.split(".")[0] for a in file_list]
                files_to_read.extend(lilist)
    elif range_checker[0] == False:
        files_to_read = []
        les_années = list(range(int(start_date[2]),int(end_date[2])+1))
        for année in les_années:
            year_path = Datatype + "\{}".format(année)
            if année == les_années[0]:
                les_mois = list(range(int(start_date[1]),12+1))
                les_mois = [month_translator(lemois(i)) for i in les_mois]
                for mois in les_mois:
                    month_path = year_path + "\{}".format(mois)
                    if mois == les_mois[0]:
                        file_list = os.listdir(month_path)
                        lilist = [a.split(".")[0] for a in file_list]
                        zefichiers = [item for item in lilist if int(start_date[0]) <= int(item.split('-')[0])]
                        files_to_read.extend(zefichiers)
                    else:
                        file_list = os.listdir(month_path)
                        lilist = [a.split(".")[0] for a in file_list]
                        files_to_read.extend(lilist)
            elif année == les_années[len(les_années)-1]:
                les_mois = list(range(1,int(end_date[1])+1))
                les_mois = [month_translator(lemois(i)) for i in les_mois]
                for mois in les_mois:
                    month_path = year_path + "\{}".format(mois)
                    if mois == les_mois[len(les_mois)-1]:
                        file_list = os.listdir(month_path)
                        lilist = [a.split(".")[0] for a in file_list]
                        zefichier = [item for item in lilist if int(end_date[0]) >= int(item.split(".")[0])]
                        files_to_read.extend(zefichiers)
                    else:
                        file_list = os.listdir(month_path)
                        lilist = [a.split(".")[0] for a in file_list]
                        files_to_read.extend(lilist)
            else:
                les_mois = list(range(1,12+1))
                les_mois = [month_translator(lemois(i)) for i in les_mois]
                for mois in les_mois:
                    file_list = os.listdir(month_path)
                    lilist = [a.split(".")[0] for a in file_list]
                    files_to_read.extend(zefichier)
                    
                    
    elif range_checker == (True,True,True):
        msgbox('Vos dates de début et de fin sont identiques, vous allez obtenir les résultats de la journée du {} {} {}'.format(start_date[0], month_translator(lemois(int(start_date[1]))), start_date[2]), 'Résultats pour une journée', 'Ok')
        year_path = Datatype + "\{}".format(start_date[2])
        month_path = year_path + "\{}".format(month_translator(lemois(int(start_date[1]))))
        files_to_read = ['{}-{}-{}'.format(start_date[0],start_date[1],start_date[2])]
        
    list_ = []
    for file_ in files_to_read:
        a = file_.split("-")
        try:
            gladata = pd.read_excel(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format)
            list_.append(gladata)
        except:
            print(r"Erreur, le fichier n'existe pas ou le chemin est incorrect: {}".format(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format))
    df = pd.concat(list_)
        
elif output == "Une date spécifique":
    zedate = enterbox("Pour quelle date souhaitez-vous voir les résultats ?","Résultats")
    zedate = zedate.split('/')
    year_path = Datatype + "\{}".format(zedate[2])
    month_path = year_path + "\{}".format(month_translator(lemois(int(zedate[1]))))
    df = pd.read_excel(Datatype + r'\{}\{}\{}'.format(int(zedate[2]),month_translator(lemois(int(zedate[1]))),'-'.join(zedate)) + file_format)
    
elif output == "Une semaine":
    output2 = choicebox("Pour quelle semaine souhaitez-vous voir les résultats ?", "Quelle semaine ?", ["Cette semaine", "Une autre semaine"])
    if output2 == "Cette semaine":
        jourji = datetime.date.today()
        files_to_read = jours_dla_semaine(jourji)
        list_=[]
        for file_ in files_to_read:
            a = file_.split("-")
            try:
                gladata = pd.read_excel(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format)
                list_.append(gladata)
            except:
                print(r"Erreur, le fichier n'existe pas ou le chemin est incorrect: {}".format(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format))
        df = pd.concat(list_)
        
    elif output2 == "Une autre semaine":
        kellesemaine = enterbox("Pour quelle semaine souhaitez-vous voir les résultats ?","Résultats d'une semaine")
        kellesemaine = kellesemaine.split('/')
        jourji = datetime.date(int(kellesemaine[2]), int(kellesemaine[1]), int(kellesemaine[0]))
        files_to_read = jours_dla_semaine(jourji)
        list_=[]
        for file_ in files_to_read:
            a = file_.split("-")
            try:
                gladata = pd.read_excel(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format)
                list_.append(gladata)
            except:
                print(r"Erreur, le fichier n'existe pas ou le chemin est incorrect: {}".format(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format))
        df = pd.concat(list_)
        
    
elif output == "Un mois":
    output2= choicebox("Pour quel mois souhaitez-vous voir les résultats ?", "Quel mois ?", ["Ce mois-ci" , "Un autre mois"])
    
    if output2 == "Ce mois-ci":
        jourji = datetime.date.today().strftime(date_format).split("-")
        year_path = Datatype + "\{}".format(jourji[2])
        month_path = year_path + "\{}".format(month_translator(lemois(jourji[1])))
        file_list = os.listdir(month_path)
        lilist = [a.split(".")[0] for a in file_list]
        files_to_read = lilist
        list_ = []
        for file_ in files_to_read:
            a = file_.split("-")
            try:
                gladata = pd.read_excel(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format)
                list_.append(gladata)
            except:
                print(r"Erreur, le fichier n'existe pas ou le chemin est incorrect: {}".format(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format))
        df = pd.concat(list_)
        
    elif output2 == "Un autre mois":
        kelmois = multenterbox("Pour quel mois souhaitez-vous voir les résultats ?","Résultats mensuels",["Mois","Année"])
        year_path = Datatype + "\{}".format(kelmois[1])
        month_path = year_path + "\{}".format(kelmois[0].lower().capitalize())
        file_list = os.listdir(month_path)
        files_to_read = [a.split(".")[0] for a in file_list]
        list_ = []
        for file_ in files_to_read:
            a = file_.split("-")
            try:
                gladata = pd.read_excel(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format)
                list_.append(gladata)
            except:
                print(r"Erreur, le fichier n'existe pas ou le chemin est incorrect: {}".format(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format))
        df = pd.concat(list_)
        
elif output == "Une année":
    output2 = choicebox("Pour quelle année souhaitez-vous voir les résultats ?", "Quelle année ?", ["Cette année-là", "Une autre année"])
    if output2 == "Cette année-là":
        jourji = datetime.date.today().strftime(date_format).split("-")
        year_path = Datatype + "\{}".format(jourji[2])
        les_mois = os.listdir(year_path)
        files_to_read = []
        for mois in les_mois:
            month_path = year_path + "\{}".format(mois)
            file_list = os.listdir(month_path)
            lilist = [a.split(".")[0] for a in file_list]
            files_to_read.extend(lilist)
        list_ = []
        for file_ in files_to_read:
            a = file_.split("-")
            try:
                gladata = pd.read_excel(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format)
                list_.append(gladata)
            except:
                print(r"Erreur, le fichier n'existe pas ou le chemin est incorrect: {}".format(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format))
        df = pd.concat(list_)
        
    elif output2 == "Une autre année":
        kelannée = enterbox("Pour quelle année souhaitez-vous voir les résultats ?", "Quelle année ?")
        year_path = Datatype + "\{}".format(kelannée)
        les_mois = os.listdir(year_path)
        files_to_read = []
        for mois in les_mois:
            month_path = year_path + "\{}".format(mois)
            file_list = os.listdir(month_path)
            lilist = [a.split(".")[0] for a in file_list]
            files_to_read.extend(lilist)
        list_ = []
        for file_ in files_to_read:
            a = file_.split("-")
            try:
                gladata = pd.read_excel(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format)
                list_.append(gladata)
            except:
                print(r"Erreur, le fichier n'existe pas ou le chemin est incorrect: {}".format(Datatype + r'\{}\{}\{}'.format(int(a[2]),month_translator(lemois(int(a[1]))),file_) + file_format))
        df = pd.concat(list_)

##=============================================================================##            
##Ajout des données nécessaires

c = CurrencyRates()
df['Dates'] = pd.to_datetime(df['Creation Time']).dt.date
df = df[df['% Exec'] > 0]
df = df[df['ClientId'] != 'ERROR']
indexCcy = df[ df['Ccy'].isnull()].index
df.drop(indexCcy , inplace=True)
df = df.replace(to_replace='GBX', value='GBP', regex=True)
df = df.replace(to_replace='ZAC', value='ZAR', regex=True)
df['Amount'] = df['FilledQty']*df['FilledAvgPx']
df['Amount'] = [row[0]*0.01 if row[1] in ('GBP','ZAR') else row[0] for row in zip(df['Amount'], df['Ccy'])]
directory = os.getcwd()
comissions_path = directory + """\{}.xlsx""".format('commisions')
df2 = pd.read_excel(r'{}'.format(comissions_path), header = None)
df2.rename(columns = {0:'ClientId', 1:'Commission'}, inplace = True)
com = {}
for ind in df2.index:
    com[df2['ClientId'][ind]] = df2['Commission'][ind]
keys = [i for i in com.keys()]
df['Bips'] = [x*0.0001 if x==float(x) else com[y]*0.0001 if y in keys else 5*0.0001 for (y,x) in zip(df['ClientId'],df['CE']) ]
df['Conversion Rate'] = [c.get_rate(str(row[0]),'EUR',row[1]) for row in zip(df['Ccy'], df['Dates'])]
df['Converted Amount'] = df['Amount']*df['Conversion Rate']
df['Commission'] = df['Converted Amount'] * df['Bips']

            
##=============================================================================##
##Que fait-on ?##

question = "Sélectionnez les graphiques que vous souhaitez voir dans le rapport PDF"
title = "On met quoi dans l'PDF"
listOfOptions = ["Commissions et nominal","distribution des commissions", "commissions/Desk", "commissions/Client", "commissions/Pays"]
graphs_a_faire = multchoicebox(question , title, listOfOptions)
            

##=============================================================================##
##Fabrication des graphiques##
###On met en place un environnement spécifique pour s'y retrouver###
rapports = workingproject + "\Reports"
chemin_graph = rapports + "\GraphForPDF"
if os.path.exists(f'{rapports}') == False:
    os.mkdir(f'{rapports}')
if os.path.exists(f'{chemin_graph}') == False:
    os.mkdir(f'{chemin_graph}')
###le dictionnaire la_clé va nous permettre de retouver nos graphiques au moment de construire le PDF###
la_clé = {"path" : list(),
         "nom" : list(),
         "description" : list()}
#génération des graphiques et enregistrement dans le bon fichier#
            
            
if "distribution des commissions" in graphs_a_faire:
    
    #construisons le graph
    sns.displot(x = df['Commission'],data = df)
    plt.xlabel("Commissions en €")
    plt.ylabel("Nombre de commissions")
    path_to_file = chemin_graph + "\RepartitionCommissions.png"
    plt.savefig(chemin_graph, bbox_inches='tight')
    
    #Faisons une description
    tt_com = f"Total des commissions : {sum(df['Commission'])}€"
    tt_nom = f"Total du nominal      : {sum(df['Converted Amount'])}€"
    description_distrib = f"{tt_com}\n{tt_nom}"
    
    #Ajout des éléments au dictionnaire la_clé
    la_clé["path"].append(path_to_file)
    la_clé["nom"].append("Distribution des commissions en euro")
    la_clé["description"].append(description_distrib)
            
if "commissions/Desk" in graphs_a_faire:
    with open('noms_des_desks.txt') as f:
        data = f.read()
    data = data.replace("\'", "\"")
    noms_desk = json.loads(data)
    
    new_desk = list()
    for i in df['Desk']:
        if i not in noms_desk.keys():
             new_desk.append(i)
    new_desk = list(set(new_desk))
    if len(new_desk) > 0:
        text_desk = "Des noms de desk jamais vus avant sont dans le jeu de données, veuillez indiquer auxquels ils correspondent, l'information sera enregistrée pour plus tard"
        titre_desk = "Nouveaux Desks Trouvés"
        output_desk = multenterbox(text_desk, titre_desk, new_desk)
        for x,y in zip(new_desk, output_desk):
            noms_desk.update({ x : y })
        try: 
            geeky_file = open('noms_des_desks.txt', 'wt')
            geeky_file.write(str(noms_desk))
            geeky_file.close()
        except:
             print("unable to write file")
    #construire le sous df
    for a,b in noms_desk.items():
        df = df.replace(to_replace= a, value= b, regex=True)
    liste_desk = df['Desk'].unique()
    sums = {'Desk Name': liste_desk , 'Desk Sum' : [sum(df[df['Desk']==desk]['Commission']) for desk in liste_desk] }
    les_desks = pd.DataFrame.from_dict(sums)
    les_desks['Proportion totale'] = [(a/sum(les_desks['Desk Sum']))*100 for a in les_desks['Desk Sum']]
    les_desks.sort_values(by=['Desk Sum'], inplace = True)
    les_desks_elite = les_desks[les_desks['Proportion totale']>=5]
    les_desks_low = les_desks[les_desks['Proportion totale']<5]
    values = ['Smaller Desks', sum(les_desks_low['Desk Sum']),(sum(les_desks_low['Desk Sum'])/(sum(les_desks_low['Desk Sum']) + sum(les_desks_elite['Desk Sum'])))*100 ]
    length = len(les_desks_elite)
    les_desks_elite.loc[length] = values
             
    
    #construisons une description
    description_desk = "Ne sont affichés sur ce graphique que les desk dont la proportion du total des commissions dépasse les 5%"
    description_desk = description_desk + '\nVue détaillée :'
    a = len(max(les_desks['Desk Name'], key = len))
    for x,y,z in zip(les_desks['Desk Name'],les_desks['Desk Sum'],les_desks['Proportion totale']):
        espace_posay = " "*(a-len(x))
        description_desk = description_desk + f"\n{x}{espace_posay} : {round(y,2)}€ (soit {round(z,2)}%)"
    
    #construisons le graph    
    les_desks_elite.sort_values(by=['Desk Sum'], inplace = True)
    data = les_desks_elite['Desk Sum']
    labels = ['{}:{:,.0f}€'.format(x,int(y)) for x,y in zip(les_desks_elite['Desk Name'],les_desks_elite['Desk Sum'])]
    plt.pie(data, labels = les_desks_elite['Desk Name'], autopct = '%1.1f%%' ,startangle=90, labeldistance = 1.2 )
    plt.legend(labels, loc = "upper right",bbox_to_anchor=(1.7, 1.),title = 'Desk Amount')
    path_to_file = chemin_graph + "\commissions_desks.png"
    plt.savefig(path_to_file, bbox_inches='tight')
    
    #Ajout des éléments au dictionnaire la_clé
    la_clé["path"].append(path_to_file)
    la_clé["nom"].append("Répartition des commissions par desks")
    la_clé["description"].append(description_desk)
            
            
if "commissions/Client" in graphs_a_faire:
    
    #construction d'un sous dataframe
    laliste = list(df['ClientId'].unique())
    tah_les_clients = { 'Client' : laliste , 'Client Sum' : [sum(df[df['ClientId']==client]['Commission']) for client in laliste] }
    lesclients = pd.DataFrame.from_dict(tah_les_clients)
    lesclients['Proportion totale'] = [(a/sum(lesclients['Client Sum']))*100 for a in lesclients['Client Sum']]
    lesclients['Label'] = [f'{x} {int(y)}%' for x,y in zip(lesclients['Client'],lesclients['Proportion totale'])]
    lesclients.sort_values(by=['Client Sum'], inplace = True)
    lesclients_elite = lesclients[lesclients['Proportion totale']>=2.5]
    
    #construction du graph
            
    data = lesclients_elite['Proportion totale']
    labels = ['{}\n{}%\n{}'.format(a,int(b), int(c)) for a,b,c in zip(lesclients_elite['Client'],lesclients_elite['Proportion totale'],lesclients_elite['Client Sum'])]
    Label_per = [str(round(i*100/sum(lesclients_elite['Client Sum']),1))+' %' for i in lesclients_elite['Client Sum']]
    fig = px.treemap(lesclients_elite, path=['Label'], values='Client Sum')
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25), showlegend=True)
    path_to_file = chemin_graph + "\commissions_clients.png"
    fig.write_image(path_to_file) 
    
    #Construction de la description
    description_client = "Ne sont affichés sur ce graphique que les clients dont la proportion du total des commissions dépasse les 2,5%"
    description_client = description_client + '\nVue détaillée :'
    a = len(max(lesclients['Client'], key = len))
    for x,y,z in zip(lesclients['Client'],lesclients['Client Sum'],lesclients['Proportion totale']):
        if round(z,2) >= 0.05 :
            espace_posay = " "*(a-len(x))
            description_client = description_client + f"\n{x}{espace_posay} : {round(y,2)}€ (soit {round(z,2)}%)"
    
    #Ajout au dictionnaire la_clé
    
    la_clé["path"].append(path_to_file)
    la_clé["nom"].append("Répartition des commissions par client")
    la_clé["description"].append(description_client)
            

if "commissions/Pays" in  graphs_a_faire:
    #va chercher les tickers des pays enregistrés
    with open('tickers_countries.txt') as f:
        data = f.read()
    data = data.replace("\'", "\"")
    js = json.loads(data)
             
    #on doir prendre en compte le cas où le dataframe contient un ticker de pays jamais rencontré auparavant
    new_countries = list()
    for i in df['Bbrg']:
        if i.split(" ")[1] not in js.keys():
            new_countries.append(i.split(" ")[1])
    new_countries = list(set(new_countries))
    if len(new_countries) > 0 :
        text_pays = "Des indices de pays jamais vus avant sont dans le jeu de données, veuillez indiquer à quels pays ils correspondent, l'information sera enregistrée pour plus tard"
        titre_pays = "Nouveaux Pays Trouvés"
        output_pays = multenterbox(text_pays, titre_pays, new_countries)
        for x,y in zip(new_countries, output_pays):
            js.update({ x : y })
        try:
            geeky_file = open('tickers_conutries.txt', 'wt')
            geeky_file.write(str(js))
            geeky_file.close()
        except:
            print("Unable to write to file")
    
    #on construit un sous dataframe pour avoir les pays et les commissions     
    df['Pays'] = [js[a.split(" ")[1]] for a in df['Bbrg']]
    liste_pays = df['Pays'].unique()
    somme_par_pays = { 'Pays' : liste_pays , 'Pays Sum' : [sum(df[df['Pays']==pays]['Commission']) for pays in liste_pays] }
    lespays = pd.DataFrame.from_dict(somme_par_pays)
    lespays['Proportion totale'] = [(a/sum(lespays['Pays Sum']))*100 for a in lespays['Pays Sum']]
    lespays.sort_values(by=['Pays Sum'], inplace = True)
    les_pays_elite = lespays[lespays['Proportion totale']>=1]
             
    #une fois notre sous dataframe prêt, on peut passer le tout pour en faire un graph
    #ici on va utiliser la classe bubble chart
    data = les_pays_elite['Pays Sum']
    labels = ['{}\n{}%'.format(a,int(b)) for a,b in zip(les_pays_elite['Pays'],les_pays_elite['Proportion totale'])]
    data = list(data)
    
             
    #On prépare la description du graphique
    description_pays = "Ne sont affichés sur ce graphique que les pays dont la proportion du total des commissions dépasse les 1%"
    description_pays = description_pays + '\nVue détaillée :'
    a = len(max(lespays['Pays'], key = len))
    for x,y,z in zip(lespays['Pays'],lespays['Pays Sum'],lespays['Proportion totale']):
        if round(z,2) >= 0.05 :
            espace_posay = " "*(a-len(x))
            description_pays = description_pays + f"\n{x}{espace_posay} : {round(y,2)}€ (soit {round(z,2)}%)"
    
    #On fait une liste de couleurs pour accompagner le graph
    yellow = Color("#fea50a")
    colors = list(yellow.range_to(Color("#a7ec0d"),len(les_pays_elite)))
    colors = [str(a) for a in colors]
            
    donnees_de_construction = {
        'labels': labels,
        'donnees': data,
        'couleur': colors
    }
    bubble_chart = BubbleChart(area = donnees_de_construction['donnees'],
                           bubble_spacing=0.1)
    bubble_chart.collapse()
    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    bubble_chart.plot(ax, donnees_de_construction['labels'], donnees_de_construction['couleur'])
    ax.axis("off")
    ax.relim()
    ax.autoscale_view()
    path_to_file = chemin_graph + "\commissions_pays.png"
    plt.savefig(path_to_file)
    la_clé["path"].append(path_to_file)
    la_clé["nom"].append("Répartition des commissions par pays")
    la_clé["description"].append(description_pays)
 
             
##=============================================================================##

#construit l'objet pdf
##titre du pdf
###Quel scénario ?
#["Aujourd'hui","Une semaine", "Un mois", "Une année","Une date spécifique","Entre deux dates"]

if output == "Aujourd'hui":
    a = min(df['Dates'])
    a = a.strftime(date_format)
    a = a.replace('-','/')
    titre_du_pdf = f'PNL - Rapport du {a}'
            
elif output == "Une semaine":
    a = min(df['Dates'])
    a = a.strftime(date_format)
    a = a.replace('-','/')
    titre_du_pdf = f'PNL - Rapport de la semaine du {a}'
                        
elif output == "Un mois":
    a = min(df['Dates'])
    a = a.strftime(date_format)
    a = a.split('-')
    titre_du_pdf =f'PNL - Rapport {month_translator(lemois(int(a[1])))} {a[2]}'
            
elif output == "Une année":
    a = min(df['Dates'])
    a = a.strftime(date_format)
    a = a.split('-')
    titre_du_pdf = f"PNL - Rapport de l'année {a[2]}"
    
elif output == "Une date spécifique":
    a = min(df['Dates'])
    a = a.strftime(date_format)
    a = a.replace('-','/')
    titre_du_pdf = f'PNL - Rapport du {a}'
            
elif output == "Entre deux dates":
    a = min(df['Dates'])
    b = max(df['Dates'])
    a = a.strftime(date_format)
    b = b.strftime(date_format)
    a = a.replace('-','/')
    b = b.replace('-','/')
    titre_du_pdf = f'PNL - Rapport Période entre le {a} et le {b}'
                      
pdf = PDF(orientation = 'P', unit = 'mm', format = 'A4')

for i in range(len(graphs_a_faire)):
    pdf.print_graph(la_clé["nom"][i], la_clé["description"][i], la_clé["path"][i])
    
#métadonnées
pdf.set_title(titre_du_pdf)
pdf.set_author('Exec Desk Python')

#Saut de page auto
pdf.set_auto_page_break(auto = False, margin = 15)

release_date = datetime.date.today()
release_date = release_date.strftime(date_format)
bs = release_date.split('-')
current_day = bs[0]
current_month = bs[1]
current_year = bs[2]             

titre_a_enregistrer = 'Rapport du {}-{}-{}'.format(current_day, current_month, current_year)
path_to_pdf = rapports + "\{}.pdf".format(titre_a_enregistrer) 
pdf.output(path_to_pdf)
