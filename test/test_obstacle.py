# -*-coding:utf-8 -*

import unittest
import sys
sys.path.append("../objets")

from cls_obstacle import *

symbole = " "
id_joueur = "1"
id_adversaires = ["2", "3"]
test = Obstacle(symbole, id_joueur, id_adversaires)


class ObstacleTest(unittest.TestCase):

    def test_verif_cible_mur(self):
        
        symbole = "O"
        passage, porte, victoire = test._verif_cible(symbole, id_joueur, id_adversaires)
        self.assertFalse(passage)
        self.assertFalse(porte)
        self.assertFalse(victoire)


    def test_verif_cible_porte(self):
        
        symbole = "."
        passage, porte, victoire = test._verif_cible(symbole, id_joueur, id_adversaires)
        self.assertTrue(passage)
        self.assertTrue(porte)
        self.assertFalse(victoire)


    def test_verif_cible_adversaire(self):
        
        symbole = "2"
        passage, porte, victoire = test._verif_cible(symbole, id_joueur, id_adversaires)
        self.assertFalse(passage)
        self.assertFalse(porte)
        self.assertFalse(victoire)


    def test_verif_cible_sortie(self):
        
        symbole = "U"
        passage, porte, victoire = test._verif_cible(symbole, id_joueur, id_adversaires)
        self.assertTrue(passage)
        self.assertFalse(porte)
        self.assertTrue(victoire)


    def test_verif_cible_vide(self):
        
        symbole = " "
        passage, porte, victoire = test._verif_cible(symbole, id_joueur, id_adversaires)
        self.assertTrue(passage)
        self.assertFalse(porte)
        self.assertFalse(victoire)