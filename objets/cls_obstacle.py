# -*-coding:utf-8 -*

"""
Module contenant la classe Obstacle.
"""

class Obstacle:

    """
    Classe définissant les différents types d'obstacles
    que l'on peut rencontrer dans le labyrinthe.

    Elle a besoin des paramètres suivants:
      symbole:    Le symbole représentant l'obstacle
      id_joueur:  Le numéro d'identification du joueur
      nb_joueurs: Le nombre de joueurs connectés
    
    Elle possède les attributs suivants:
      type:     Le type de l'obstacle
      passage:  Booléen indiquant si le robot peut passer
      victoire: Booléen indiquant si le robot a atteint la sortie
    """

    def __init__(self, symbole, id_joueur, id_adversaires):

        self.type = symbole
        passage, porte, victoire = self._verif_cible(symbole, id_joueur, id_adversaires)
        self.passage = passage
        self.porte = porte
        self.victoire = victoire


    def _verif_cible(self, symbole, id_joueur, id_adversaires):

        """
        Méthode interne qui vérifie si l'obstacle que contient
        la case à atteindre permet de l'atteindre ou non.
        Retourne un booléen.
        
        Elle a besoin des paramètres suivants:
          symbole:    Le symbole qui représente le type d'obstacle
          id_joueur:  Le numéro d'identification du joueur
          nb_joueurs: Le nombre de joueurs
        """

        victoire = False
        porte = False

        # Le symbole O représente un mur, il empêche le passage
        if symbole == "O" or symbole in id_adversaires:
            passage = False
        else:
            passage = True

        if symbole == ".":
            porte = True

        if symbole == "U":
            victoire = True

        return passage, porte, victoire