# -*-coding:utf-8 -*

# On importe les modules utiles au programme
import os
import time

# On importe les modules relatifs au réseau
import socket
import select

# On importe les classes d'objets
from objets.cls_labyrinthe import *
from objets.cls_joueur import *
from objets.cls_obstacle import *

# Création du serveur local, on limite le nombre de connexions à 5
hote = ""
port = 12800
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)


# ---------- Choix du labyrinthe -----------------------------------------

choix_labyrinthe = 0    # Le numéro de labyrinthe choisi par le joueur
index_cartes = []       # Liste contenant les numéros des cartes disponibles

# On récupère les noms des fichiers de cartes
# et on les affiche sous forme de liste numérotée
cartes = list(os.listdir("cartes"))
print("\nLabyrinthes existants:")
numero_carte = 0
for element in cartes:
    numero_carte += 1
    print("  {0} - {1}".format(numero_carte, element[:-4]))
    index_cartes.append(numero_carte)

# On demande à l'utilisateur de choisir un labyrinthe
while choix_labyrinthe not in index_cartes:
    try:
        choix_labyrinthe = int(input("\nEntrez un numero de labyrinthe pour commencer a jouer: "))
    except ValueError:
        print("\nVous devez entrer un nombre compris entre 1 et {}".format(numero_carte))
        continue
    if choix_labyrinthe not in index_cartes:
        print("\nVous devez entrer un nombre compris entre 1 et {}".format(numero_carte))
    print("En attente des joueurs...")

# On définit le chemin d'accès au fichier de labyrinthe choisi
chemin_carte = "cartes/{}".format(cartes[choix_labyrinthe - 1])


# ---------- Connexion des clients et validation du début de la partie ------------

# Le serveur écoute tous les clients connectés
# jusqu'à ce que l'un d'eux valide le début de la partie.
# Il n'est ensuite plus possible de s'y connecter.

clients_connectes = []
debut_partie = False

while not debut_partie:

    connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)
    for connexion in connexions_demandees:
        connexion_avec_client, infos_connexion = connexion.accept()
        clients_connectes.append(connexion_avec_client)
    for client in clients_connectes:
        client.send(b"start")
    clients_a_lire = []
    
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
    except select.error:
        pass
    else:
        for client in clients_a_lire:
            msg_recu = client.recv(1024)
            msg_recu = msg_recu.decode()
            if msg_recu == "OK":
                debut_partie = True
                for client in clients_connectes:
                    client.send(b"OK")


# Le principe est de proposer à chaque client connecté de choisir
# de démarrer la partie. Le client étant en même temps à l'écoute
# du serveur grâce au module threading, une seule validation suffit
# pour démarrer la partie. En revanche, on demandera quand même
# aux autres clients de taper Entrée pour sortir de l'invite de commande.


# ---------- Validation par les autres clients ------------------------

# La partie ayant été validée, on demande aux autres clients
# de valider par la touche Entrée pour sortir de l'invite.

nb_clients = len(clients_connectes)
compteur_client = 0
clients_prets = []

for client in clients_connectes:
    clients_prets.append([client, 0])
while compteur_client != nb_clients:
    compteur_client = 0
    for client in clients_prets:
        msg_recu = client[0].recv(1024)
        msg_recu = msg_recu.decode()
        if msg_recu == "OK":
            client[1] = 1
    for client in clients_prets:
        if client[1] == 1:
            compteur_client += 1
for client in clients_connectes:
    client.send(b"pret")

print("La partie a commencé.")


# ---------- Initialisation de la partie ----------------------------------

# Création de l'objet labyrinthe et
# placement des robots sur la carte
labyrinthe = Labyrinthe(chemin_carte)
labyrinthe.creer_robots(nb_clients)

# Création automatique des objets joueurs en fonction
# du nombre de joueurs grâce à la fonction exec.
# On les stocke ensuite dans une liste itérable
# et mutable (car on souhaite pouvoir supprimer des joueurs).
liste_joueurs = []
compteur_joueur = 1
for client in clients_connectes:
    exec("joueur_"+str(compteur_joueur)+" = Joueur("+str(compteur_joueur)+", labyrinthe.carte)")
    exec("liste_joueurs.append(joueur_"+str(compteur_joueur)+")")
    compteur_joueur += 1
compteur_joueur = 1
for joueur in liste_joueurs:
    joueur.socket = clients_connectes[compteur_joueur - 1]
    compteur_joueur += 1

# Les règles du jeu
regles = "\
\n- Le X (majuscule) represente votre robot, vous devez l'amener\
\n  jusqu'a la sortie representee par le U\
\n- Les x (minuscule) sont vos adversaires\
\n- Les . sont des portes que vous pouvez traverser et les O\
\n  sont des murs que vous ne pouvez pas traverser\
\n- Vous devez entrer une direction dans laquelle vous deplacer :\
\n  N pour Nord, S pour Sud, E pour Est, O pour Ouest\
\n- Vous pouvez avancer automatiquement en indiquant un nombre (exemple: N3)\
\n- Vous pouvez percer un mur en tapant P suivi d'une direction\
\n- Vous pouvez murer une porte en tapant M suivi d'une direction\
\n- Tapez Q pour quitter la partie"

# On envoie les règles à chaque joueur
for client in clients_connectes:
    client.send(regles.encode())


# ---------- Début de la boucle principale -----------------------------

victoire = False
joueurs_presents = list(liste_joueurs)

while not victoire:

    joueur_supprime = None

    for joueur in liste_joueurs:

        if joueur not in joueurs_presents:
            continue

        joueur_suivant = False
        deplacement = False
        afficher_a_tous = True

        while not joueur_suivant:

            # On vérifie si quelqu'un s'est déconnecté.
            # Si c'est le cas on supprime son socket de la liste
            # pour que son robot n'apparaisse plus sur la carte.
            if joueur_supprime in liste_joueurs:
                joueurs_presents.remove(joueur_supprime)
                joueur_supprime = None
            nb_joueurs = len(joueurs_presents)

            # On crée une liste contenant les sockets des adversaires
            # pour pouvoir leur envoyer un message différent.
            id_joueurs = []
            liste_adversaires = []
            id_adversaires = []
            for present in joueurs_presents:
                id_joueurs.append(present.id)
                liste_adversaires.append(present)
                id_adversaires.append(present.id)
            liste_adversaires.remove(joueur)
            id_adversaires.remove(joueur.id)
            
            # On affiche le labyrinthe, soit seulement au joueur en cours,
            # soit à tous les joueurs si une action a été effectuée.
            # Le robot du joueur se différenciera des robots adverses :
            #   Une croix majuscule pour le joueur
            #   Des croix minuscules pour les adversaires
            if not afficher_a_tous:
                carte_perso = labyrinthe.afficher_croix(joueur.id, id_adversaires)
                carte_perso = "\n{}\n".format(carte_perso).encode()
                afficher_a_tous = True
                joueur.socket.send(carte_perso)
            else:
                for present in joueurs_presents:
                    id_adversaires = list(id_joueurs)
                    id_adversaires.remove(present.id)
                    carte_perso = labyrinthe.afficher_croix(present.id, id_adversaires)
                    carte_perso = "\n{}\n".format(carte_perso).encode()
                    present.socket.send(carte_perso)

                # On envoie un message d'attente à chaque adversaire
                for adversaire in liste_adversaires:
                    adversaire.socket.send(b"\nVeuillez attendre votre tour.")

            # Si le robot n'est pas en cours de déplacement automatique
            # on demande au joueur ce qu'il souhaite faire.
            if not joueur.attente:
                a_vous_de_jouer = "\nJoueur {} : A vous de jouer (R pour afficher les regles)".format(joueur.id).encode()
                joueur.socket.send(a_vous_de_jouer)

                # On utilise un délai pour éviter d'envoyer
                # les 2 messages en même temps
                time.sleep(0.3)

                # Quand le client reçoit "pret" il demande au joueur
                # d'entrer quelque chose.
                joueur.socket.send(b"pret")

                # On mémorise le choix du joueur
                joueur.choix = joueur.socket.recv(1024).decode()


                # ---------- Analyse du choix du joueur -----------------------

                # On analyse l'action choisie grâce à la méthode analyser_choix
                quitter, voir_regles, percer, murer, direction, message = joueur.analyser_choix(joueur.x, joueur.y)

                # Il est possible pour un joueur de quitter la partie.
                # Il est alors déconnecté et supprimé de la liste
                # des joueurs présents. Son robot sera ensuite effacé.
                if quitter:
                    joueur_suivant = True
                    joueur_supprime = joueur
                    joueur.socket.send(message.encode())
                    message = "\nLe joueur {} a quitté la partie".format(joueur.id)
                    for adversaire in liste_adversaires:
                    	adversaire.socket.send(message.encode())
                    labyrinthe.supprimer_joueur(joueur.id, joueur.porte)
                    print("Le joueur {} a quitté la partie.".format(joueur.id))
                    continue

                # Le joueur peut afficher les règles à tout moment.
                elif voir_regles:
                    joueur.socket.send(regles.encode())
                    afficher_a_tous = False
                    continue

                # Le joueur peut percer un mur
                elif percer:
                    percage, message = labyrinthe.percer_mur(joueur.x, joueur.y, direction)
                    joueur.socket.send(message.encode())
                    if percage:
                        joueur_suivant = True
                    else:
                        joueur_suivant = False
                        afficher_a_tous = False
                    continue

                # Ou murer une porte
                elif murer:
                    murage, message = labyrinthe.murer_porte(joueur.x, joueur.y, direction)
                    joueur.socket.send(message.encode())
                    if murage:
                        joueur_suivant = True
                    else:
                        joueur_suivant = False
                        afficher_a_tous = False
                    continue


            # ---------- Analyse du déplacement -----------------------------

            # On veut savoir si le choix du joueur est de déplacer son robot
            cible_y, cible_x, direction, distance, deplacement_demande, message = joueur.position_cible(joueur.x, joueur.y)

            # En cas de choix incohérent on lui redemandera
            # ce qu'il souhaite faire.
            #import pdb;pdb.set_trace()
            if not deplacement_demande:
                joueur.socket.send(message.encode())
                afficher_a_tous = False
            else:

                # On vérifie à quelle étape en est le robot.
                # Si il y a plusieurs étapes, on avant le robot
                # d'une seule case.
                cible_x, cible_y = joueur.analyser_etape(joueur.x, joueur.y, cible_x, cible_y, direction, distance)

                # On récupère le type d'obstacle présent sur la position cible
                symbole = labyrinthe.verif_symbole(cible_x, cible_y)
                obstacle = Obstacle(symbole, joueur.id, id_adversaires)
                victoire = obstacle.victoire

                # On vérifie que le déplacement demandé est possible
                # On vérifie également si le robot a atteint la sortie
                if not obstacle.passage:
                    joueur.etape = 0
                    joueur.attente = False
                    joueur_suivant = False
                    deplacement_valide = False
                    afficher_a_tous = False
                    joueur.socket.send(b"\nVous ne pouvez pas aller plus loin !")
                else:
                    joueur_suivant = True
                    deplacement_valide = True

                # Si le nombre d'étapes est égal à la distance
                # Le robot met fin à son déplacement automatique
                if joueur.etape >= abs(distance):
                    joueur.attente = False
                    joueur.etape = 0

                # Si un déplacement a été effectué, on vérifie si une porte était présente
                # Puis on modifie la chaîne de caractère labyrinthe.carte
                if deplacement_valide:
                    labyrinthe.deplacement_robot(joueur.x, joueur.y, cible_x, cible_y, joueur.porte, joueur.id)
                    joueur.x = cible_x
                    joueur.y = cible_y
                    joueur.porte = obstacle.porte


        # ---------- Victoire d'un joueur et fin de partie -----------------------

        if victoire:

            # On envoie un smiley content au joueur qui a gagné
            with open("objets/gagne.txt") as fichier:
                win = fichier.read()
            joueur.socket.send(win.encode())
            joueur.socket.send(b"\nFelicitations ! Vous avez gagne !")

            # On envoie un smiley pas content aux autres joueurs
            with open("objets/perdu.txt") as fichier:
                 lose = fichier.read()
            for adversaire in liste_adversaires:
                adversaire.socket.send(lose.encode())
                adversaire.socket.send(b"\nDommage, vous avez perdu !")

            # On marque une pause avant d'envoyer l'ordre de terminer
            # car si le client reçoit l'ordre en même temps que
            # le message précédent, il ne saura pas l'identifier
            time.sleep(0.5)
            for client in clients_connectes:
                client.send(b"fin")

            break

connexion_principale.close()
print("\nLa partie est terminée.\n")
os.system("pause")
exit()