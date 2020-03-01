# -*-coding:utf-8 -*

"""
Module contenant la classe Labyrinthe.
"""

import random


class Labyrinthe:

    """
    Classe définissant le labyrinthe à utiliser dans le jeu Roboc.

    Elle a besoin des paramètres suivants:
      chemin_carte: Le chemin vers le labyrinthe en fichier txt
      nb_joueurs:   Le nombre de joueurs

    Elle possède l'attribut suivant:
      carte: La chaîne de caractère représentant le labyrinthe
    """

    def __init__(self, chemin_carte):

        with open(chemin_carte, "r") as fichier:
            self.carte = fichier.read()


    def creer_robots(self, nb_joueurs):

        """
        Méthode interne qui place aléatoirement les robots
        de tous les joueurs sur le labyrinthe.
        Chaque robot est représenté par le numéro du joueur.
        
        Elle a besoin du paramètre suivant:
          nb_joueurs: Le nombre de joueurs
        """

        # On transforme la chaîne de caractères carte
        # en liste pour simplifier l'accès aux caractères.
        carte_liste = self.carte.split("\n")
        ligne = len(carte_liste) - 1
        colonne = len(carte_liste[0]) - 1
        id_joueur = 1

        # On utilise le module random sur chaque case
        # jusqu'à ce qu'on en trouve une vide et on
        # y place le premier robot.
        # On répète l'opération pour chaque robot.
        while id_joueur <= nb_joueurs:
            test = False
            while not test:
                ligne_robot = random.randint(1, ligne - 1)
                colonne_robot = random.randint(1, colonne - 1)
                if carte_liste[ligne_robot][colonne_robot] == " ":
                    test = True
            ligne_creation = list(carte_liste[ligne_robot])
            ligne_creation[colonne_robot] = str(id_joueur)
            carte_liste[ligne_robot] = "".join(ligne_creation)
            id_joueur += 1
        self.carte = "\n".join(carte_liste)


    def afficher_croix(self, id_joueur, id_adversaires):

        """
        Méthode qui remplace les numéros des joueurs
        sur le labyrinthe par des croix.
        Une croix majuscule pour son propre robot
        et des croix minuscules pour les adversaires.
        
        Elle a besoin des paramètres suivants:
          id_joueur:      Le numéro du joueur
          id_adversaires: Liste contenant les numéros
                          des joueurs adverses
        """

        # On remplace les identifiants par des croix
        carte = self.carte.replace(id_joueur, "X")
        for adversaire in id_adversaires:
            carte = carte.replace(adversaire, "x")
        return carte


    def supprimer_joueur(self, id_joueur, porte):

        """
        Méthode qui supprime un joueur du labyrinthe.
        Elle place éventuellement une porte sur son emplacement.
        
        Elle a besoin du paramètre suivant:
          id_joueur: Le numéro du joueur à supprimer
          porte:     Présence ou absence d'une porte
        """

        if porte:
            self.carte = self.carte.replace(id_joueur, ".")
        else:
            self.carte = self.carte.replace(id_joueur, " ")


    def deplacement_robot(self, depart_x, depart_y, arrivee_x, arrivee_y, porte, id_joueur):

        """
        Méthode qui modifie la position du robot
        sur le labyrinthe et replace éventuellement
        une porte sur sa position de départ.
        
        Elle a besoin des paramètres suivants:
          depart_x:  Position de départ du robot en x
          depart_y:  Position de départ du robot en y
          arrivee_x: Position d'arrivée du robot en x
          arrivee_y: Position d'arrivée du robot en y
          porte:     Présence ou absence d'une porte
                     sur la position de départ
          id_joueur: Le numéro du joueur
        """

        # On convertit les lignes de départ et d'arrivée
        # du labyrinthe en listes indexables
        carte_liste = self.carte.split("\n")
        ligne_depart = list(carte_liste[depart_y])
        ligne_arrivee = list(carte_liste[arrivee_y])

        # On cherche à savoir si la ligne de départ est
        # différente de la ligne d'arrivée pour savoir si
        # le robot se déplace verticalement ou horizontalement
        if ligne_arrivee != ligne_depart:
            ligne_arrivee[arrivee_x] = id_joueur
            if porte == True:
                ligne_depart[depart_x] = "."
            else:
                ligne_depart[depart_x] = " "    
            carte_liste[arrivee_y] = "".join(ligne_arrivee)
            carte_liste[depart_y] = "".join(ligne_depart)
        else:
            ligne_arrivee[arrivee_x] = id_joueur
            if porte == True:
                ligne_arrivee[depart_x] = "."
            else:
                ligne_arrivee[depart_x] = " "
            carte_liste[arrivee_y] = "".join(ligne_arrivee)
        
        # On regroupe les lignes modifiées sous forme de
        # chaîne de caractères
        self.carte = "\n".join(carte_liste)


    def percer_mur(self, position_x, position_y, direction):

        """
        Méthode permettant de remplacer certains murs
        par des portes.

        Elle a besoin des paramètres suivants:
          cible_x: Position en x du mur ciblé
          cible_y: Position en y du mur ciblé
        """

        ligne_porte = []
        carte_liste = self.carte.split("\n")

        # On récupère l'emplacement à percer
        # En y
        if direction.upper() == "N":
            cible_y = position_y - 1
        elif direction.upper() == "S":
            cible_y = position_y + 1
        else:
            cible_y = position_y

        # Puis en x
        if direction.upper() == "E":
            cible_x = position_x + 1
        elif direction.upper() == "O":
            cible_x = position_x - 1
        else : cible_x = position_x

        # On vérifie que la cible contient bien un mur
        # et qu'il ne se trouve pas sur le contour de la carte
        if carte_liste[cible_y][cible_x] == "O":
            if cible_y == 0 or cible_y == len(carte_liste) - 1 \
            or cible_x == 0 or cible_x == len(carte_liste[0]) - 1:
                message = "\nIl est interdit de percer ce mur !"
                percage = False
            else:
                ligne_porte = list(carte_liste[cible_y])
                ligne_porte[cible_x] = "."
                carte_liste[cible_y] = "".join(ligne_porte)
                message = "\nBravo, la voie est libre !"
                percage = True
        else :
            message = "\nIl n'y a aucun mur à percer !"
            percage = False

        self.carte = "\n".join(carte_liste)

        return percage, message


    def murer_porte(self, position_x, position_y, direction):

        """
        Méthode permettant de remplacer certaines portes
        par des murs.

        Elle a besoin des paramètres suivants:
          cible_x: Position en x de la porte ciblée
          cible_y: Position en y de la porte ciblée
        """

        ligne_porte = []
        carte_liste = self.carte.split("\n")

        # On récupère l'emplacement à percer
        # En y
        if direction.upper() == "N":
            cible_y = position_y - 1
        elif direction.upper() == "S":
            cible_y = position_y + 1
        else:
            cible_y = position_y

        # Puis en x
        if direction.upper() == "E":
            cible_x = position_x + 1
        elif direction.upper() == "O":
            cible_x = position_x - 1
        else : cible_x = position_x

        # On vérifie que la cible contient bien une porte
        if carte_liste[cible_y][cible_x] == ".":
            ligne_porte = list(carte_liste[cible_y])
            ligne_porte[cible_x] = "O"
            carte_liste[cible_y] = "".join(ligne_porte)
            message = "\nVoilà, la porte est murée !"
            murage = True
        else :
            message = "\nIl n'y a aucune porte à murer !"
            murage = False

        self.carte = "\n".join(carte_liste)

        return murage, message


    def verif_symbole(self, cible_x, cible_y):

        """
        Méthode qui retourne le symbole présent sur la position cible.
        
        Elle a besoin des paramètres suivants:
          arrivee_x:  Position d'arrivée du robot en x
          arrivee_y:  Position d'arrivée du robot en y
        """

        carte_liste = self.carte.split("\n")
        symbole = carte_liste[cible_y][cible_x]

        return symbole