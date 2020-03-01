# -*-coding:utf-8 -*

import unittest
import sys
sys.path.append("../objets")

from cls_labyrinthe import *

chemin_carte = "../cartes/facile.txt"
id_joueur = "1"
nb_joueurs = 3
id_adversaires = ["2", "3"]
carte_test = "\
OOOOOOOOOO\n\
O O    O O\n\
O . OO   O\n\
O O O  3 O\n\
O OOOO O.O\n\
O O O    U\n\
O OOOOOO.O\n\
O O  2   O\n\
O O OOOOOO\n\
O .1O    O\n\
OOOOOOOOOO"
position_x = 3
position_y = 9


class LabyrintheTest(unittest.TestCase):

    def test_creer_robots(self):
        
        # On cherche à savoir si le nombre et les numéros
        # de robots créés sont bons et si ils ont bien été
        # créés sur des emplacements vides.
        test = Labyrinthe(chemin_carte)
        nb_murs = carte_test.count("O")
        nb_portes = carte_test.count(".")
        nb_sorties = carte_test.count("U")
        test.creer_robots(nb_joueurs)
        self.assertEqual(nb_murs, test.carte.count("O"))
        self.assertEqual(nb_portes, test.carte.count("."))
        self.assertEqual(nb_sorties, test.carte.count("U"))
        self.assertEqual(1, test.carte.count("1"))
        self.assertEqual(1, test.carte.count("2"))
        self.assertEqual(1, test.carte.count("3"))


    def test_afficher_croix(self):

        # On vérifie que la fonction a bien remplacé les
        # numéros des joueurs par des croix.
        test = Labyrinthe(chemin_carte)
        test.carte = carte_test
        carte_croix = test.afficher_croix(id_joueur, id_adversaires)
        self.assertNotIn("1", carte_croix)
        self.assertNotIn("2", carte_croix)
        self.assertNotIn("3", carte_croix)
        self.assertEqual(1, carte_croix.count("X"))
        self.assertEqual(2, carte_croix.count("x"))


    def test_supprimer_joueur_1(self):

        # On vérifie que le numéro du joueur a bien
        # été retiré de la carte et qu'une porte n'a
        # pas été placée.
        test = Labyrinthe(chemin_carte)
        test.carte = carte_test
        porte = False
        test.supprimer_joueur(id_joueur, porte)
        carte_liste = test.carte.split("\n")
        self.assertNotIn("1", test.carte)
        self.assertEqual(" ", carte_liste[9][3])


    def test_supprimer_joueur_2(self):

        # On refait le test avec une porte
        test = Labyrinthe(chemin_carte)
        test.carte = carte_test
        porte = True
        test.supprimer_joueur(id_joueur, porte)
        carte_liste = test.carte.split("\n")
        self.assertNotIn("1", test.carte)
        self.assertEqual(".", carte_liste[9][3])


    def test_deplacement_robot_1(self):

        # On va déplacer le robot sur une case vide
        test = Labyrinthe(chemin_carte)
        test.carte = carte_test
        depart_x = 3
        depart_y = 9
        arrivee_x = 3
        arrivee_y = 8
        porte = False
        test.deplacement_robot(depart_x, depart_y, arrivee_x, arrivee_y, porte, id_joueur)
        carte_liste = test.carte.split("\n")
        self.assertEqual("1", carte_liste[8][3])
        self.assertEqual(" ", carte_liste[9][3])


    def test_deplacement_robot_2(self):

        # On va déplacer le robot sur une porte
        test = Labyrinthe(chemin_carte)
        test.carte = carte_test
        depart_x = 3
        depart_y = 9
        arrivee_x = 2
        arrivee_y = 9
        porte = False
        test.deplacement_robot(depart_x, depart_y, arrivee_x, arrivee_y, porte, id_joueur)
        carte_liste = test.carte.split("\n")
        self.assertEqual("1", carte_liste[9][2])
        self.assertEqual(" ", carte_liste[9][3])


    def test_percer_mur_1(self):

        # On essaye de percer un mur intérieur
        test = Labyrinthe(chemin_carte)
        test.carte = carte_test
        direction = "e"
        percage_test = True
        message_test = "\nBravo, la voie est libre !"
        percage, message = test.percer_mur(position_x, position_y, direction)
        carte_liste = test.carte.split("\n")
        self.assertEqual(".", carte_liste[9][4])
        self.assertEqual(percage_test, percage)
        self.assertEqual(message_test, message)


    def test_percer_mur_2(self):

        # On essaye de percer un mur de contour
        test = Labyrinthe(chemin_carte)
        test.carte = carte_test
        direction = "s"
        percage_test = False
        message_test = "\nIl est interdit de percer ce mur !"
        percage, message = test.percer_mur(position_x, position_y, direction)
        carte_liste = test.carte.split("\n")
        self.assertEqual(percage_test, percage)
        self.assertEqual(message_test, message)


    def test_percer_mur_3(self):

        # On essaye de percer un emplacement vide
        test = Labyrinthe(chemin_carte)
        test.carte = carte_test
        direction = "n"
        percage_test = False
        message_test = "\nIl n'y a aucun mur à percer !"
        percage, message = test.percer_mur(position_x, position_y, direction)
        carte_liste = test.carte.split("\n")
        self.assertEqual(percage_test, percage)
        self.assertEqual(message_test, message)


    def test_murer_porte_1(self):

        # On essaye de murer une porte
        test = Labyrinthe(chemin_carte)
        test.carte = carte_test
        direction = "o"
        murage_test = True
        message_test = "\nVoilà, la porte est murée !"
        murage, message = test.murer_porte(position_x, position_y, direction)
        carte_liste = test.carte.split("\n")
        self.assertEqual("O", carte_liste[9][2])
        self.assertEqual(murage_test, murage)
        self.assertEqual(message_test, message)


    def test_murer_porte_2(self):

        # On essaye de murer un emplacement vide
        test = Labyrinthe(chemin_carte)
        test.carte = carte_test
        direction = "n"
        murage_test = False
        message_test = "\nIl n'y a aucune porte à murer !"
        murage, message = test.murer_porte(position_x, position_y, direction)
        carte_liste = test.carte.split("\n")
        self.assertEqual(murage_test, murage)
        self.assertEqual(message_test, message)


    def test_verif_symbole_1(self):

        # On teste le symbole sur un mur
        test = Labyrinthe(chemin_carte)
        test.carte = carte_test
        cible_x = 4
        cible_y = 9
        symbole_test = "O"
        symbole = test.verif_symbole(cible_x, cible_y)
        self.assertEqual(symbole_test, symbole)


    def test_verif_symbole_2(self):

        # On teste le symbole sur un emplacement vide
        test = Labyrinthe(chemin_carte)
        test.carte = carte_test
        cible_x = 3
        cible_y = 8
        symbole_test = " "
        symbole = test.verif_symbole(cible_x, cible_y)
        self.assertEqual(symbole_test, symbole)


    def test_verif_symbole_3(self):

        # On teste le symbole sur une porte
        test = Labyrinthe(chemin_carte)
        test.carte = carte_test
        cible_x = 2
        cible_y = 9
        symbole_test = "."
        symbole = test.verif_symbole(cible_x, cible_y)
        self.assertEqual(symbole_test, symbole)