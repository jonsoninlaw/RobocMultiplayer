# -*-coding:utf-8 -*

import os
import socket
from threading import Thread
import time


# Connexion au serveur local
hote = "localhost"
port = 12800
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Vous êtes connecté à la partie.")
print("Veuillez attendre que le serveur ait choisi une carte.")
confirmation_serveur = connexion_avec_serveur.recv(1024)
while connexion_avec_serveur.recv(1024) != b"start":
    confirmation_serveur = connexion_avec_serveur.recv(1024)

# On crée 2 classes héritées de la classe Thread
# pour permettre de proposer au joueur de démarrer
# la partie et en même temps d'écouter si un autre
# joueur a déjà démarré la partie.

msg_a_envoyer = ""
msg_recu = ""

class Lancer_partie(Thread):

    """
    Classe héritée de Thread permettant de
    proposer au joueur de lancer lui-même
    la partie.

    Elle possède l'attribut suivant:
      pret: Vrai si le joueur a décidé
            de lancer la partie
    """

    def __init__(self):
        Thread.__init__(self)
        self.pret = False

    def run(self):
        
        while not self.pret:

            # On demande au joueur d'entrer C pour commencer
            print("\nEntrez C pour commencer la partie.")
            msg_a_envoyer = input("> ")
            if self.pret:
                continue

            # Quand il entre C on envoie l'ordre de démarrer la partie
            elif msg_a_envoyer.upper() == "C":
                connexion_avec_serveur.send(b"OK")
                print("\nLa partie va commencer. Veuillez attendre les autres joueurs.")
                self.pret = True
                break
            else :
                print("\nCette commande n'est pas reconnue.")
        

class Partie_lancee(Thread):

    """
    Classe héritée de Thread permettant
    d'écouter le serveur afin de savoir
    si un joueur a lancé la partie.

    Elle possède l'attribut suivant:
      pret: Vrai si un joueur a lancé
            la partie
    """

    def __init__(self):
        Thread.__init__(self)
        self.pret = False

    def run(self):

        # On attend que le serveur nous envoie "OK"
        msg_recu = connexion_avec_serveur.recv(1024)
        while msg_recu.decode() != "OK":
            msg_recu = connexion_avec_serveur.recv(1024)
        self.pret = True


# Création des 2 objets Thread
lancer_partie = Lancer_partie()
partie_lancee = Partie_lancee()

# Lancement des 2 objets Thread
lancer_partie.start()
partie_lancee.start()

# On attend que l'objet partie_lancee soit terminé.
# C'est celui qui attend que le serveur confirme
# que la partie a été démarrée par un des joueurs.
partie_lancee.join()
lancer_partie.pret = partie_lancee.pret
time.sleep(0.1)

# Si ce n'est pas le joueur qui a démarré la partie
# l'objet lancer_partie est toujours actif.
# On demande donc au joueur de le terminer en
# appuyant sur Entrée.
if lancer_partie.is_alive():
    print("\nLa partie va commencer. Appuyez sur Entrée pour continuer.")
lancer_partie.join()
connexion_avec_serveur.send(b"OK")
confirmation_serveur = connexion_avec_serveur.recv(1024)

# On attend la confirmation du serveur que
# tous les joueurs sont prêts.
while confirmation_serveur != b"pret":
    confirmation_serveur = connexion_avec_serveur.recv(1024)


# ---------- Boucle de jeu -------------------------------------------------

while msg_recu != "fin":
    
    # On écoute le serveur tant qu'il n'a pas
    # envoyé le message "fin".
    msg_recu = connexion_avec_serveur.recv(1024)
    msg_recu = msg_recu.decode()

    # Lorsque le serveur envoi le message "pret"
    # on demande au joueur d'entrer son choix.
    if msg_recu == "pret":
        msg_a_envoyer = ""
        while msg_a_envoyer == "":
            msg_a_envoyer = input("> ")
            if msg_a_envoyer == "":
                print("\nVous devez entrer quelque chose !")

    # Lorsque le serveur envoi le message "fin"
    # la partie est terminée et on déconnecte le joueur.
    elif msg_recu == "fin":
        print("\nLa partie est terminée, vous allez être déconnecté.\n")
        connexion_avec_serveur.close()
        os.system("pause")
        exit()
    else:
        print(msg_recu)
        continue

    # On envoie le choix du joueur au serveur
    msg_a_envoyer = msg_a_envoyer.encode()
    connexion_avec_serveur.send(msg_a_envoyer)