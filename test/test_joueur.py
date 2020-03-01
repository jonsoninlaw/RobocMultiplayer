# -*-coding:utf-8 -*

import unittest
import sys
sys.path.append("../objets")

from cls_joueur import *

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


class JoueurTest(unittest.TestCase):

    def test_position_depart(self):
                
        test = Joueur(id_joueur, carte_test)
        position_x_test = 3
        position_y_test = 9
        position_y, position_x = test._position_depart(carte_test)
        self.assertEqual(position_y, position_y_test)
        self.assertEqual(position_x, position_x_test)


    def test_analyser_choix_1(self):
        
        # On vérifie si le choix du joueur est cohérent
        # On commence par tester une commande non reconnue
        test = Joueur(id_joueur, carte_test)
        test.choix = "BERGé'(45"
        position_x = 3
        position_y = 9
        message_test = ""
        quitter, voir_regles, percer, murer, direction, message = test.analyser_choix(position_x, position_y)
        self.assertFalse(quitter)
        self.assertFalse(voir_regles)
        self.assertFalse(percer)
        self.assertFalse(murer)
        self.assertEqual("", direction)
        self.assertEqual(message_test, message)


    def test_analyser_choix_2(self):
        
        # On teste avec la commande pour quitter
        test = Joueur(id_joueur, carte_test)
        test.choix = "q"
        position_x = 3
        position_y = 9
        message_test = "fin"
        direction_test = ""
        quitter, voir_regles, percer, murer, direction, message = test.analyser_choix(position_x, position_y)
        self.assertTrue(quitter)
        self.assertFalse(voir_regles)
        self.assertFalse(percer)
        self.assertFalse(murer)
        self.assertEqual(direction_test, direction)
        self.assertEqual(message_test, message)


    def test_analyser_choix_3(self):
        
        # On teste avec la commande pour afficher les règles
        test = Joueur(id_joueur, carte_test)
        test.choix = "r"
        position_x = 3
        position_y = 9
        message_test = ""
        direction_test = ""
        quitter, voir_regles, percer, murer, direction, message = test.analyser_choix(position_x, position_y)
        self.assertFalse(quitter)
        self.assertTrue(voir_regles)
        self.assertFalse(percer)
        self.assertFalse(murer)
        self.assertEqual(direction_test, direction)
        self.assertEqual(message_test, message)


    def test_analyser_choix_4(self):
        
        # On teste avec la commande pour percer un mur
        test = Joueur(id_joueur, carte_test)
        test.choix = "pn"
        position_x = 3
        position_y = 9
        message_test = ""
        direction_test = "n"
        quitter, voir_regles, percer, murer, direction, message = test.analyser_choix(position_x, position_y)
        self.assertFalse(quitter)
        self.assertFalse(voir_regles)
        self.assertTrue(percer)
        self.assertFalse(murer)
        self.assertEqual(direction_test, direction)
        self.assertEqual(message_test, message)


    def test_analyser_choix_5(self):
        
        # On teste avec la commande pour percer un mur
        # mais avec une direction incohérente
        test = Joueur(id_joueur, carte_test)
        test.choix = "pt"
        position_x = 3
        position_y = 9
        message_test = "\nVous devez entrer P suivi d'une direction (N, S, E ou O)."
        direction_test = ""
        quitter, voir_regles, percer, murer, direction, message = test.analyser_choix(position_x, position_y)
        self.assertFalse(quitter)
        self.assertFalse(voir_regles)
        self.assertFalse(percer)
        self.assertFalse(murer)
        self.assertEqual(direction_test, direction)
        self.assertEqual(message_test, message)


    def test_analyser_choix_6(self):
        
        # On teste avec la commande pour murer une porte
        test = Joueur(id_joueur, carte_test)
        test.choix = "mn"
        position_x = 3
        position_y = 9
        message_test = ""
        direction_test = "n"
        quitter, voir_regles, percer, murer, direction, message = test.analyser_choix(position_x, position_y)
        self.assertFalse(quitter)
        self.assertFalse(voir_regles)
        self.assertFalse(percer)
        self.assertTrue(murer)
        self.assertEqual(direction_test, direction)
        self.assertEqual(message_test, message)


    def test_analyser_choix_7(self):
        
        # On teste avec la commande pour murer une porte
        # mais avec une direction incohérente
        test = Joueur(id_joueur, carte_test)
        test.choix = "mt"
        position_x = 3
        position_y = 9
        message_test = "\nVous devez entrer M suivi d'une direction (N, S, E ou O)."
        direction_test = ""
        quitter, voir_regles, percer, murer, direction, message = test.analyser_choix(position_x, position_y)
        self.assertFalse(quitter)
        self.assertFalse(voir_regles)
        self.assertFalse(percer)
        self.assertFalse(murer)
        self.assertEqual(direction_test, direction)
        self.assertEqual(message_test, message)


    def test_analyser_etape_1(self):
        
        # On vérifie si un déplacement d'une case fonctionne
        test = Joueur(id_joueur, carte_test)
        test.choix = "n"
        position_x = 3
        position_y = 9
        cible_x_test = 3
        cible_y_test = 8
        direction = "n"
        distance = 1
        cible_x, cible_y = test.analyser_etape(position_x, position_y, cible_x_test, cible_y_test, direction, distance)
        self.assertEqual(cible_x_test, cible_x)
        self.assertEqual(cible_y_test, cible_y)


    def test_analyser_etape_2(self):
        
        # On vérifie si un déplacement de 3 cases fonctionne
        test = Joueur(id_joueur, carte_test)
        test.choix = "n"
        position_x = 3
        position_y = 9
        cible_x_test = 3
        cible_y_test = 6
        direction = "n"
        distance = 3
        cible_x, cible_y = test.analyser_etape(position_x, position_y, cible_x_test, cible_y_test, direction, distance)
        cible_x, cible_y = test.analyser_etape(cible_x, cible_y, cible_x_test, cible_y_test, direction, distance)
        cible_x, cible_y = test.analyser_etape(cible_x, cible_y, cible_x_test, cible_y_test, direction, distance)        
        self.assertEqual(cible_x_test, cible_x)
        self.assertEqual(cible_y_test, cible_y)