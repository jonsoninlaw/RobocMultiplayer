# -*-coding:utf-8 -*

"""
Module contenant la classe Joueur.
"""

class Joueur:

    """
    Classe définissant l'identité du joueur et permettant
    de stocker toutes les variables qui lui sont propres.

    Elle a besoin du paramètre suivant:
      id: Le numéro du joueur
    
    Elle possède les attributs suivants:
      id: Le numéro du joueur
      socket: Le socket de connexion du joueur
      attente: Variable permettant de savoir si le robot
               doit se déplacer seul
      etape:   Variable permettant de connaître le nombre
               de fois où le robot doit se déplacer seul
      choix:   L'action choisie par le joueur
      porte:   Mémorise si le robot du joueur se trouve
               sur une porte
    """

    def __init__(self, id_joueur, carte):

        self.id = str(id_joueur)
        self.socket = None
        position_y, position_x = self._position_depart(carte)
        self.x = position_x
        self.y = position_y
        self.attente = False
        self.etape = 0
        self.choix = ""
        self.porte = False


    def _position_depart(self, carte):

        """
        Méthode interne qui vérifie la position de départ du robot
        et retourne un tuple contenant ses coordonnées.
        
        Elle a besoin des paramètres suivants:
          carte :     Chaîne de caractères contenant le labyrinthe
          id_joueur : Le numéro d'identification du joueur
        """

        # On transforme la chaîne de caractères carte
        # en liste pour simplifier l'accès aux caractères.
        # Puis on transforme chaque élément de liste en une
        # autre liste pour indexer facilement chaque caractère.
        carte_liste = carte.split("\n")
        compteur = 0
        
        for element in carte_liste:
            if self.id in element:
                ligne_depart = compteur
            else:
                compteur += 1
        compteur = 0
        for element in carte_liste[ligne_depart]:
            if self.id in element:
                colonne_depart = compteur
            else:
                compteur += 1

        # Le numéro de ligne représente la position en y
        # Le numéro de colonne représente la position en x
        return ligne_depart, colonne_depart


    def analyser_choix(self, position_x, position_y):

        """
        Méthode permettant d'analyser ce que souhaite faire
        le joueur.

        Elle a besoin des paramètres suivants:
          position_x: Position du robot en x
          position_y: Position du robot en y
        """

        quitter = False
        voir_regles = False
        percer = False
        murer = False
        direction = ""
        message = ""

        # Q pour quitter la partie
        if self.choix.upper() == "Q":
            quitter = True
            message = "fin"

        # R pour afficher les règles
        elif self.choix.upper() == "R":
            voir_regles = True

        # P pour percer un mur
        elif self.choix[0].upper() == "P":

            if len(self.choix) != 2 or self.choix[1].upper() not in "NSEO":
                message = "\nVous devez entrer P suivi d'une direction (N, S, E ou O)."
                percer = False
            else:
                direction = self.choix[1]
                percer = True

        # M pour murer une porte
        elif self.choix[0].upper() == "M":
            if len(self.choix) != 2 or self.choix[1].upper() not in "NSEO":
                message = "\nVous devez entrer M suivi d'une direction (N, S, E ou O)."
                murer = False
            else:
                direction = self.choix[1]
                murer = True

        return quitter, voir_regles, percer, murer, direction, message


    def position_cible(self, position_x, position_y):

        """
        Méthode qui retourne la position ciblée
        en fonction de la position de départ et de
        la direction et la distance choisies.
        
        Elle a besoin des paramètres suivants:
          position_x: Coordonnée de départ du robot en x
          position_y: Coordonnée de départ du robot en y
          direction:  Chaîne de caractère contenant la direction
                      demandée par le joueur
          distance:   Entier correspondant au nombre de cases que
                      doit parcourir le robot
        """

        deplacement_demande = False
        message = ""
        distance = None

        # On vérifie que le joueur a entré quelque chose de cohérent
        direction = str(self.choix[0])
        if direction.upper() in "NSEO":
            try:
                if len(self.choix) > 1:
                    distance = int(self.choix[1:])
                    if distance == 0:
                        message = "\nLe nombre de deplacement ne peut pas etre egal a 0"
                    else:
                        deplacement_demande = True
                else:
                    distance = 1
                    deplacement_demande = True
            except ValueError:
                message = "\nCette commande n'est pas reconnue."
        else:
            message = "\nCette commande n'est pas reconnue."

        if deplacement_demande:

            # On détermine la position d'arrivée du robot
            # en fonction du choix du joueur.
            # Verticalement :
            if direction.upper() == "N":
                cible_y = position_y - distance
            elif direction.upper() == "S":
                cible_y = position_y + distance
            else:
                cible_y = position_y

            # Horizontalement :
            if direction.upper() == "E":
                cible_x = position_x + distance
            elif direction.upper() == "O":
                cible_x = position_x - distance
            else : cible_x = position_x
        else:
            cible_y = False
            cible_x = False


        # Le numéro de ligne représente la position en y
        # Le numéro de colonne représente la position en x
        return cible_y, cible_x, direction, distance, deplacement_demande, message


    def analyser_etape(self, position_x, position_y, cible_x, cible_y, direction, distance):

        """
        Méthode permettant de vérifier si le robot
        doit avancer tout seul ou non en fonction
        du nombre d'étapes déjà effectué.

        Elle a besoin des paramètres suivants:
          position_x: Position de départ du robot en x
          position_y: Position de départ du robot en y
          cible_x:    Position cible du robot en x
          cible_y:    Position cible du robot en y
          direction:  La direction du déplacement souhaitée
          distance:   La distance de déplacement
        """

        # Si la distance choisie par le joueur est supérieure à 1
        # le robot se déplace automatiquement d'une seule case par tour.
        if abs(distance) > 1 and self.etape != distance:
            if direction.upper() == "N":
                cible_y = position_y - 1
            elif direction.upper() == "S":
                cible_y = position_y + 1
            elif direction.upper() == "E":
                cible_x = position_x + 1
            elif direction.upper() == "O":
                cible_x = position_x - 1

            # On note le nombre d'étapes qu'a déjà effectué le robot
            # et on indique que le robot n'a pas fini de se déplacer.
            self.etape += 1
            self.attente = True

        return cible_x, cible_y