#We import the modules we are going to need throughout the minigame
import os
from random import randrange
from math import ceil

#Small function to indicate the color of the roulette spots, it is optional but makes the whole thing nicer
def couleur(case):
    if case % 2 == 0:
        return 'rouge'
    else:
        return 'noir'

#the function that runs every turn, it determines the amount of money won each time
def partie_roulette(mise, place):
    winner = randrange(50)
    couleur_winner = couleur(winner)
    print("la boule est tombée sur le",winner,couleur_winner)
    if winner == place:
        mise = 3*mise
        print(f"""La chance est de votre côté, c'est la bonne case, remportez trois fois votre mise, soit {mise}€ !""")
    elif winner % 2 == place % 2:
        mise = ceil(mise/2)
        print(f"""C'est la bonne couleur! Pas la bonne case, reprenez la moitié de votre mise,soit {mise}€""")
    else:
        mise = 0
        print("""Dommage, essayez à nouveau pour vous refaire""")
    return mise



#We initialize the game by asking and asserting that the player has a correct amount of money
pocket = 0

#the boolean will makes the game start automatically at the end of each turn, until the ending conditions are met
continuer_jeu = True

#while loop to make sure the player enters a correct value for the money they have brought to the casino
while pocket == 0:
    pocket = input('Combien avez-vous en poche en arrivant au casino ?')
    try:
        pocket = float(pocket)
        assert pocket > 0  
    except ValueError:
        print("La somme que vous avez déclarée avoir en poche n'est pas un nombre !")
        pocket = 0
    except AssertionError:
        print("La somme que vous avez en poche ne peut pas être négative ou nulle")
        pocket = 0

#Short message to greet the player and remind them how much money they have
print("Bienvenue à  la table de roulette, vous avez",pocket,"€ en poche")



#Starting the game
while continuer_jeu:

#The player is asked how much he will bet on this turn, and we assert that the amount is correct
    mise = "vide"
    while mise == "vide":
        mise = input('Combien souhaitez-vous miser pour ce tour ?')
        try:
            mise = float(mise)
            assert mise >= 0
            #sub try loop to assert the bet is possible with starting money
            try:
                assert mise <= pocket
            except AssertionError:
                print("Vous ne pouvez pas miser plus que ce que vous avez sur vous...")
                mise = "vide"

        except ValueError:
            print("La somme que vous souhaitez miser n'est pas un nombre !")
            mise = "vide"
        except AssertionError:
            print("La somme que vous misez ne peut pas être négative")
            mise = "vide"
    
    #the bet is discounted from the player's money
    pocket = pocket - mise

#same methodology as the one use to confirm that the spot on which the bet is placed is correct
    place = "vide"
    while place == "vide":
        place = input('Sur quel emplacement de la roulette souhaitez-vous placer votre mise ?')
        try:
            place = int(place)
            assert place >= 0 and place <= 49 
        except ValueError:
            print("Indiquez une case par un entier compris entre 0 et 49 inclus")
            place = "vide"
        except AssertionError:
            print("Assurez-vous de placer votre mise sur une bonne case")
            place = "vide"

    #we determine the color of the selected roulette spot
    couleur_place = couleur(place)
    #print a summary of current situation
    print("Vous placez votre mise de",mise,"€ sur le",place,couleur_place)

    #the function partie_roulette determines how much is won
    gain = partie_roulette(mise,place)
    #profits are added to the player's money
    pocket = pocket + gain

#now we must determine if the player is able/willing to continue the game
    if pocket <= 0:
        print("""C'est la fin des haricots, vous êtes ruiné, le jeu s'arrête pour vous...""")
        continuer_jeu = False
        #out of money, the game ends

    else:
        #the choice to continue is in the player's hands
        print("Vous avez encore",pocket,"€ en poche")
        quitter = 'vide'
        #the player must enter yes or no, if something else, the input loops until good input
        while quitter == 'vide':
            quitter = input("Désirez-vous continuer la partie ? Yes/No")
            try:
                assert quitter.lower() in ['yes','no']
            except AssertionError:
                print("Entrez une réponse valide")
                quitter = 'vide'

        #player chose to stop here, the game ends
        if quitter.lower() == "no":
            print("Vous quittez le casino avec vos gains")
            continuer_jeu = False
            
#pauses the system
os.system("pause")