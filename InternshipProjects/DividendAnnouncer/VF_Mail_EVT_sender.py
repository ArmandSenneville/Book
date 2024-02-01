#ces premières lignes nous permettent d'importer les bibliothèques python dont on se sert au cours du programme
import os
import glob
import os.path
import pandas as pd
#pd est un shortcut d'appel de la fonction
from xbbg import blp
from easygui import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from = import d'une fonction particilière de la bibliothèque
import smtplib, ssl
import datetime
from calendar import month_name
pd.options.mode.chained_assignment = None
import webbrowser

##=============================================================================##

err_msg = "Something went wrong"
sender_email = "TITLE_PLACEHOLDER <SENDER_EMAIL_PLACEHOLDER>"
smtp_server = 'SERVER_ADRESS_PLACEHOLDER'

list_months = [
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
]

liste_mois = [
    'Janvier','Février','Mars','Avril','Mai','Juin',
    'Juillet','Août','Septembre','Octobre','Novembre','Décembre'
]

date_format = "%d-%m-%Y"

##=============================================================================##
#On se sert de ces trois fonctions au cours du script

#lemois permet de sortir le nom d'un mois en anglais à partir de son numéro
def lemois(month_number):
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

#month_translator s'occupe de traduire le nom du mois en anglais vers le français, il n'a rien d'intelligent et comparre seulement les deux listes construites plus haut
def month_translator(month_name):   
    if month_name in list_months:
        poitou_charentes = list_months.index(month_name)
        month_name = liste_mois[poitou_charentes]
        return month_name
    else:
        print("""{} n'est pas un mois de l'année en anglais""".format(month_name))
        return None

def dataframe_to_html(dataframe,table_name):
#ici on converti le dtata frame en html
    zeheader = list(dataframe)
#enregistrement des noms des colonnes du tableau 
    zerangées = dataframe.values.tolist()
#ici chaques rangées sont transformée en liste qui sont mis dans une grande liste
    header = ""
    tablesplit = ""
    for i in range(len(zeheader)):
#definit le nombre de colonnes
        header = header + """\
            <th style='text-align:center;background:#B10C24;color:white;padding: 2px;padding-left: 2 px;padding-center: 2 px;'>""" + str(zeheader[i]) + """</th>
            """
    rang = 0
    zejour = zerangées[0][2].split('/')[0]
    for item in zerangées:
        if int(zejour) != int(item[2].split('/')[0]):
            rang += 1
            zejour = item[2].split('/')[0]
        if rang %2 == 0:
            tablesplit = tablesplit + """\
            <tr bgcolor = #ffffff>
            """
            for i in range(len(item)):
                if item[4] == "Dividend Ex-Date":
                    tablesplit = tablesplit + """\
                    <td style='text-align:center;border: 1px solid #CCC;padding : 2px;padding-left: 2 px;padding-center: 2 px;'>""" + '<b>' + str(item[i]) + '</b>' + """</td>"""
                else:
                    tablesplit = tablesplit + """\
                    <td style='text-align:center;border: 1px solid #CCC;padding : 2px;padding-left: 2 px;padding-center: 2 px;'>""" + str(item[i]) + """</td>"""
            tablesplit = tablesplit + """\
           </tr>
            """
        else:
            tablesplit = tablesplit + """\
            <tr bgcolor = #e7e7e7>
            """
            for i in range(len(item)):
                if item[4] == "Dividend Ex-Date":
                    tablesplit = tablesplit + """\
                    <td style='text-align:center;border: 1px solid #CCC;padding : 2px;padding-left: 2 px;padding-center: 2 px;bgcolor = #dadada ;'>""" + '<b>' + str(item[i]) + '</b>' + """</td>"""
                else:
                    tablesplit = tablesplit + """\
                    <td style='text-align:center;border: 1px solid #CCC;padding : 2px;padding-left: 2 px;padding-center: 2 px;bgcolor = #dadada ;'>""" + str(item[i]) + """</td>"""
            tablesplit = tablesplit + """\
            </tr>
            """


    html_table = """\
    <table id={} width=50% padding=5px cellspacing=0 cellpadding=1.5 color: #333;style='font-family: Calibri Light, Arial, sans-serif;font-size: 11pt;border-collapse: collapse;border-spacing: 0;'>
        <tr>
            {}
        </tr>
        {}
        </table>
        """.format(table_name,header,tablesplit)
    return html_table

def mail_to_html(dataframe,table_name):
#ici on converti le dtata frame en html
    zeheader = list(dataframe)
#enregistrement des noms des colonnes du tableau 
    zerangées = dataframe.values.tolist()
#ici chaques rangées sont transformée en liste qui sont mis dans une grande liste
    header = ""
    tablesplit = ""
    for i in range(len(zeheader)):
#definit le nombre de colonnes
        header = header + """\
            <th style='text-align:center;background:#B10C24;color:white;padding: 2px;padding-left: 2 px;padding-center: 2 px;'>""" + str(zeheader[i]) + """</th>
            """
    
    for item in zerangées:
        tablesplit = tablesplit + """\
        <tr>
        """
        for i in range(len(item)):
            tablesplit = tablesplit + """\
            <td style='text-align:center;border: 1px solid #CCC;padding : 2px;padding-left: 2 px;padding-center: 2 px;'>""" + str(item[i]) + """</td>"""
        tablesplit = tablesplit + """\
        </tr>
        """
    html_table = """\
    <table id={} width=50% padding=5px cellspacing=0 cellpadding=1.5 color: #333;style='font-family: Calibri Light, Arial, sans-serif;font-size: 11pt;border-collapse: collapse;border-spacing: 0;'>
        <tr>
            {}
        </tr>
        {}
        </table>
        """.format(table_name,header,tablesplit)
    return html_table


    
def ordinal_english(a):
#pour les bons ordinaux (st, nd, rd, th) en anglais
    a = int(a)
    last_digit = a % 10
    last_digit = int(last_digit)
    if last_digit == 1 and a != 11:
        a = str(a) + "st"
    elif last_digit == 2 and a != 12:
        a = str(a) + "nd"
    elif last_digit == 3 and a != 13:
        a = str(a) + "rd"
    else:
        a = str(a) + "th"
    return a

##=============================================================================##

test_ou_pas = ccbox("Êtes-vous en train d'effectuer un test ?","To test or not to test ?",["Oui","Non"])
data_ou_pas = ccbox("Y a-t-il des évènements à partager cette semaine ?","T'as de la data ?",["Oui","Non"])

##=============================================================================##

#On va chercher le dernier fichier enregistré dans le dossier week_events, cette organisation nous permet de toujours exploiter les dernières données
directory = os.getcwd()
#ici on appelle la fonction getcwd de la librairie OS qui sort une chaine de caractere correspondant au chemin du fichier, .../... = path , endroit du ficher = directory
    
##=============================================================================##
#Ici c'est la partie "intelligente", on extrait les données, on nettoie, on effectue la request bdp et on met au propre

if data_ou_pas == True:
    while True:
        #une boucle while True va tourner à l'infini jusqu'à ce qu'on lui dise d'arrêter, ici avec l'instruction break
        try:
            folder_path = directory + '\week_events'
            folder_path = r'{}'.format(folder_path)
            file_type = r'\*xlsx'
            files = glob.glob(folder_path + file_type)
            latest_file = max(files, key=os.path.getctime)
            #selectionne le fichier Xlsx
            #chemin path du fichier le plus récent
            df = pd.read_excel(r'{}'.format(latest_file))
            #df = data frame
            break
        except IOError:
            msgbox("Vous avez laissé votre fichier excel ouvert, fermez-le et cliquez sur OK","Le script n'a pas pu accéder au fichier","Ok")
        
    df['Dates'] = pd.to_datetime(df['Date']).dt.date
    #converti la date
    df = df.drop(['Date'], axis = 1)
    df.rename(columns = {'Dates':'Date','Time':'MKTTime (CET Time)'}, inplace = True)
    zecolonnes = list(df)
    bonne_liste = ['Name', 'Ticker', 'Date', 'MKTTime (CET Time)', 'Description']
    #colonnes à garder
    for column_name in zecolonnes :
        if column_name not in bonne_liste:
            df = df.drop([column_name], axis = 1)
            #exclusion des mauvaises colonnes
    column_order = ['Name','Ticker','Date','MKTTime (CET Time)','Description','Amount']
    df = df.reindex(columns=column_order)
    #ordre des colonnes
    df.sort_values(['Date'], axis = 0, inplace = True)
    #sort by date
    df.reset_index(drop=True, inplace=True)
    for ind in df.index:
        df['Date'][ind] = df['Date'][ind].strftime(date_format)
        df['Date'][ind] = str(df['Date'][ind].replace('-','/'))
        #présentation date
        if df['Description'][ind] == """Dividend Ex-Date""":
            try:
                df1 = blp.bdp(tickers = "{} Equity".format(df['Ticker'][ind]),flds = ["DVD_SH_LAST"])
                a = df1['dvd_sh_last'][0]
                df['Amount'][ind] = a
            except:
                print("""BDP request failed, please check your script""")
    #request bdp pour chaque rangées du tableau
    df = df.fillna("")
    #si cellule = nan ou vide alors " "
    a = df['Date'].unique()
    c = [(datetime.date.today() + datetime.timedelta(days=i)).strftime("%d/%m/%Y") for i in range(5)]
    if len(set(a).intersection(set(c))) == 0:
        msgbox(r"Le programme n'a pas trouvé de jour de la semaine dans votre jeu de données, lors de la vérification, contrôlez bien la validité de la colonne 'Date'","Attention aux dates","Ok")



##=============================================================================##
#Passage du tableau au format html, pour que le style du tableau (css) s'affiche correctement sur exchange il faut le rentrer ligne par ligne (on appelle cela du inline css)
#La façon la plus simple est de demander au script de convertir notre dataframe en une liste de listes, ie, chaque liste dans la liste correspond à une ligne du dataframe

if data_ou_pas == True:
    shit = dataframe_to_html(df,'Week Events')
else:
    shit = """<small>
    <p style="color:#212121">Hello All, no Equity Events for this week.<br>
    I wish you a good week</p>
    </small>"""
#on invoque notre data frame dont le talbeau s'appellera weekevent
corps = """\
<html>
  <head>
        </head><body>
<p style="color:#939393"><i>This report has been generated automatically.</i></p> </b>

    {}
    
  </body>
</html>
""".format(shit)

if data_ou_pas == True:
    Html_file= open("bruh.html","w")
    Html_file.write(corps)
    Html_file.close()
    #ici on inclue le tableau dans le format HTML
    webbrowser.open('bruh.html')
    #visulaisation dans le browser
    bon_contenu = ccbox('Après avoir vérifié vos données dans le navigateur, souhaitez-vous les envoyer ?','Week Events',["Oui","Non"])
    #invocation de la chatbox
    os.remove('bruh.html')

##=============================================================================##

msg = MIMEMultipart('alternative')
# ça singifie que le message du mail sera en text et ou HTML
msg['From'] = sender_email

receiver_email = sender_email
if test_ou_pas == False:
    liste_mails = pd.read_excel(r'{}\Mails.xlsx'.format(directory), header = None)
    #va lire les adresses mails
    liste_mails.rename(columns = {0:'email'}, inplace = True)
    zecollegues = mail_to_html(liste_mails,'Liste Mails')
    #mise en format des email en html 
    haute_savoie = open('affichage_html.html','w')
    haute_savoie.write(zecollegues)
    haute_savoie.close()
    webbrowser.open('affichage_html.html')
    #affichage du html mail dans le browser
    quivarecevoir = ccbox("Le mail sera envoyé aux adresses affichées","Destinataires",["Continuer","Annuler"])
    #if second de la chatbox email
    if quivarecevoir == True:
        for i in range(len(liste_mails)):
            receiver_email = receiver_email + "," + str(liste_mails.iloc[i]['email'])
            #on concatène les mails avec des ","
        msg['To'] = receiver_email
    os.remove('affichage_html.html')
        #ignore
else :
    msg['To'] = sender_email  
    
if data_ou_pas == False:
    msg['Subject'] = 'No Equity Events for the Week'
elif data_ou_pas == True and bon_contenu == True:
    plusieurs_semaines = ccbox("Vos données présent-elles des évènements sur plusieurs semaines? Le cas échéant, il conviendrait de mettre un objet de mail correspondant","Une ou plusieurs semaines ?",["Plusieurs Semaines","Une seule semaine"])
    release_date = datetime.date.today()
    release_date = release_date.strftime(date_format)
    bs = release_date.split('-')
    current_day = bs[0]
    current_month = bs[1]
    current_year = bs[2]
    year_path = folder_path + '\{}'.format(current_year)
    zemois = lemois(current_month)
    current_month = month_translator(zemois)
    #définition du nom et chemin du fichier que l'on va enregister
    if plusieurs_semaines == False:
        msg['Subject'] = 'Equity Events for the week of {} {}'.format(zemois,ordinal_english(current_day))
    else:
        msg['Subject'] = enterbox("Votre mail vaut pour plusieurs semaines, quel sera son objet ?", "Objet du mail")
    
part = MIMEText(corps, 'html')
msg.attach(part)

if test_ou_pas == True and data_ou_pas == False:
    try:
        smtp = smtplib.SMTP(smtp_server)
        smtp.sendmail(sender_email,receiver_email,msg.as_string())
        smtp.close()
    except(
        smtplib.SMTPConnectError,
        smtplib.SMTPDataError,
        smtplib.SMTPAuthenticationError,
        smtplib.SMTPException,
        smtplib.SMTPHeloError,
        smtplib.SMTPRecipientsRefused,
        smtplib.SMTPResponseException,
        smtplib.SMTPSenderRefused,
        smtplib.SMTPServerDisconnected) as lerreur:
        print( "Erreur = "+ str(lerreur))
#erreur de protocol mail
elif test_ou_pas == True and data_ou_pas == True and bon_contenu == True:
    try:
        smtp = smtplib.SMTP(smtp_server)
        smtp.sendmail(sender_email,receiver_email,msg.as_string())
        smtp.close()
    except(
        smtplib.SMTPConnectError,
        smtplib.SMTPDataError,
        smtplib.SMTPAuthenticationError,
        smtplib.SMTPException,
        smtplib.SMTPHeloError,
        smtplib.SMTPRecipientsRefused,
        smtplib.SMTPResponseException,
        smtplib.SMTPSenderRefused,
        smtplib.SMTPServerDisconnected) as lerreur:
        print( "Erreur = "+ str(lerreur))
elif test_ou_pas == False and quivarecevoir == True and data_ou_pas == False:
    try:
        smtp = smtplib.SMTP(smtp_server)
        smtp.sendmail(sender_email,receiver_email.split(","),msg.as_string())
        smtp.close()
    except(
        smtplib.SMTPConnectError,
        smtplib.SMTPDataError,
        smtplib.SMTPAuthenticationError,
        smtplib.SMTPException,
        smtplib.SMTPHeloError,
        smtplib.SMTPRecipientsRefused,
        smtplib.SMTPResponseException,
        smtplib.SMTPSenderRefused,
        smtplib.SMTPServerDisconnected) as lerreur:
        print( "Erreur = "+ str(lerreur))
#erreur de protocol mail
elif test_ou_pas == False and quivarecevoir == True and data_ou_pas == True and bon_contenu == True:
    try:
        smtp = smtplib.SMTP(smtp_server)
        smtp.sendmail(sender_email,receiver_email.split(","),msg.as_string())
        smtp.close()
    except(
        smtplib.SMTPConnectError,
        smtplib.SMTPDataError,
        smtplib.SMTPAuthenticationError,
        smtplib.SMTPException,
        smtplib.SMTPHeloError,
        smtplib.SMTPRecipientsRefused,
        smtplib.SMTPResponseException,
        smtplib.SMTPSenderRefused,
        smtplib.SMTPServerDisconnected) as lerreur:
        print( "Erreur = "+ str(lerreur))
#erreur de protocol mail

##=============================================================================##

if data_ou_pas == True and bon_contenu == False:
    msgbox("Vous avez jugé que les données traitées par le script n'étaient pas bonnes, rien n'a été envoyé, et le fichier initial va être supprimé", "Annulation du Script", "Ok")
    os.remove(r'{}'.format(latest_file))
    
elif test_ou_pas == False and quivarecevoir == False:
    msgbox("Un de vos destinataires avait un souci, le fichier initial n'a pas été supprimé, vérifiez vos destinataires dans le fichier mails et relancez le programme", "Annulation du Script", "Ok")
    
elif test_ou_pas == False and quivarecevoir == True and data_ou_pas == True and bon_contenu == True:
    month_path = year_path + '\{}'.format(current_month)
    zefile = '\Semaine_du_{}_{}'.format(current_day,current_month)
    zefile = zefile + '.xlsx'
    if os.path.exists(r'{}'.format(month_path)) == True:
        df.to_excel(month_path + zefile)
    elif os.path.exists(r'{}'.format(year_path)) == True:
        os.mkdir(month_path)
        df.to_excel(month_path + zefile)
    else:
        os.mkdir(year_path)
        os.mkdir(month_path)
        df.to_excel(month_path + zefile)
    os.remove(r'{}'.format(latest_file))
    msgbox("Le programme a fonctionné dans son intégralité, le fichier initial a été supprimé et votre version a été enregistrée dans votre base de données locale", "Succès Complet!", "Ok")
    
elif test_ou_pas == True and data_ou_pas == True and bon_contenu == True:
    save_ou_pas = ccbox("Vous venez d'effectuer un test et tout a fonctionné, voulez-vous enregistrer vos données et supprimer le fichier initial ?", """[Test]Succès Complet""",["Oui","Non"])
    if save_ou_pas == True:
        month_path = year_path + '\{}'.format(current_month)
        zefile = '\Semaine_du_{}_{}'.format(current_day,current_month)
        zefile = zefile + '.xlsx'
        if os.path.exists(r'{}'.format(month_path)) == True:
            df.to_excel(month_path + zefile)
        elif os.path.exists(r'{}'.format(year_path)) == True:
            os.mkdir(month_path)
            df.to_excel(month_path + zefile)
        else:
            os.mkdir(year_path)
            os.mkdir(month_path)
            df.to_excel(month_path + zefile)
        os.remove(r'{}'.format(latest_file))
        msgbox("Le programme a fonctionné dans son intégralité, le fichier initial a été supprimé et votre version a été enregistrée dans votre base de données locale", """[Test]Succès Complet!""","Ok")
    else:
        msgbox("Suite à votre test, votre fichier n'a été ni supprimé ni enregistré, mais tout fonctionne, pour le partager relancez le programme !","""[Test]Succès Complet!""","Ok")
