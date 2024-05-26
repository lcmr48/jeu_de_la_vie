"""Module pour l'affichage du jeux."""

from dataclasses import dataclass
from tkinter import Canvas, Tk, Button, LEFT
from moteur import cellule_naissance_mort, placement_aleatoire, grille_jeu_de_la_vie, vaisceau


@dataclass
class Affichage:
    """Classe contenant l'etat de l'application

    l'utilisation de dataclass permet de créer le constructeur de cette classe automatiquement
    """

    matrice: list[list[int]]  # la matrice contenant les cellules
    formes: list[list[int]]  # une matrice contenant les identifiants des rectangles
    taille: int  # la taille du canevas en pixels
    canevas: Canvas  # le canevas contenant la grille
    fenetre: Tk  # la fenetre principale
    avance_auto: bool = False  # avancement automatique actif ou non


def dessiner_ligne(x1: int, y1: int, x2: int, y2: int, canvas: Canvas) -> None:
    """
    affiche une ligne dans le canvas de largeur 2 pixels
    Args:
        x1 (int): abscisse du point de départ
        y1 (int): ordonnée du point de départ
        x2 (int): abscisse du point de arrivée
        y2 (int): ordonnée du point de arrivée
        canvas (Canvas): _description_
    """
    canvas.create_line(x1, y1, x2, y2, width=2, fill="black")


def grille(ligne: int, colonne: int, taille: int, canvas: Canvas) -> callable:
    """
    trace des lignes pour créer un cadrillages, avec des lignes horizontales et verticales
    Args:
        ligne (int): nombre de ligne de la grille
        colonne (int): nombre de colonne de la grille
        taille (int): taille en pixel du canvas(c'est un carré donc l=L)
        canvas (Canvas): préciser le canvas dans lequelle nous travaillons

    Returns:
        callable: les lignes se dessine
    """
    x1 = 0
    y1 = 0
    x2 = taille
    y2 = 0
    for _ in range(ligne):
        y1 = y1 + taille / ligne
        y2 = y2 + taille / ligne
        dessiner_ligne(x1, y1, x2, y2, canvas)
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = taille
    for _ in range(colonne):
        x1 = x1 + taille / colonne
        x2 = x2 + taille / colonne
        dessiner_ligne(x1, y1, x2, y2, canvas)


def tracer_rectangle(x1: int, y1: int, x2: int, y2: int, canvas: Canvas) -> int:
    """
    trace un rectangles avec des coordonnées donner en parametre dans le canvas
    Args:
        x1 (int): abscisse du point de départ
        y1 (int): ordonnée du point de départ
        x2 (int): abscisse point formant la diagonale du rectangle + 1px
        y2 (int): ordonnée point formant la diagonale du rectangle + 1px
        canvas (Canvas): presiser le canvas dans lequelle nous travaillons

    Returns:
        int: on retourne l'identifiant du rectangle se qui nous permet de l'identifier plus tard
    """
    return canvas.create_rectangle(x1, y1, x2, y2, fill="white")


def clique_forme(affichage: Affichage, x: int, y: int) -> callable:
    """Cré une fonction qui sera appelé lors du clic sur un rectangle

    la cellelue et le rectangle sont identifiés par ses coordonnées x et y

    Args:
        y (_type_): indice du tableau dans la matrice
        x (_type_): indice de l'element dans ce tableau
    Returns:
        la fonction appelé lors d'un clic sur un rectangle
    """

    def clique(_):
        """fonction appelée lors d'un clic ssur un rectrange

        Args:
            _: ce paramettre est passé par tkinter lors d'un clic, nous n'en avons pas besoin
            on l'appelle "_" pour cette raison
        """
        # on inverse l'état de la cellule
        if affichage.matrice[y][x] == 1:
            affichage.matrice[y][x] = 0
        else:
            affichage.matrice[y][x] = 1
        # et on rafraichi l'interface graphique
        mise_a_jour_couleur_formes(
            affichage.matrice, affichage.formes, affichage.canevas
        )

    return clique


def configure_clic_sur_forme(affichage: Affichage) -> None:
    """
    chaque rectangles a un identifiant qui permet de l'identifier, lors d'un clique sur le
    canevas donc dans un rectangles, un identifiant est donner, nous cherchons a quelle
    rectangles il appartient et nous changeons sa couleurs, se qui nous permet de changer
    les couleurs des cases en cliquant dessus.
    Args:
        affichage (Affichage): état de l'application
    """

    # On boucle sur la matrice pour retrouver nos identifiants de rectangles
    # sur lesquels nous pouvons appeler la fonction tag_bind qui permet de lui associer
    # le clic du bouton gauche de la souris
    for ymat, ligne in enumerate(affichage.formes):
        for xmat, identifiant_forme in enumerate(ligne):
            # on écoute le bouton gauche de la souris qui appelera une fonction créée pour
            # mettre à jour l'état de la cellule aux coordonnées xmat, ymat
            affichage.canevas.tag_bind(
                identifiant_forme, "<Button-1>", func=clique_forme(affichage, xmat, ymat)
            )


def trace_formes(
    nb_ligne: int, nb_colonne: int, taille: int, can: Canvas
) -> list[list[int]]:
    """
    nous traçons les rectangles dans les cases definer par l'intersections des lignes
    Args:
        nb_ligne (int): nombre de ligne da la grille
        nb_colonne (int): nombre de colonne de la grille
        taille (int): taille du canvas en px
        can (Canvas): canvas dans lequelle nous travaillons

    Returns:
        list[list[int]]: renvoie la grille contenant des tableaux dans chaque case
    """
    matrice_formes = [None] * nb_ligne
    for y in range(nb_ligne):
        matrice_formes[y] = [None] * nb_colonne
        for x in range(nb_colonne):
            x1 = x * (taille / nb_colonne)
            y1 = y * (taille / nb_ligne)
            x2 = x1 + (taille / nb_colonne) - 1
            y2 = y1 + (taille / nb_ligne) - 1
            matrice_formes[y][x] = tracer_rectangle(x1, y1, x2, y2, can)
    return matrice_formes


def mise_a_jour_couleur_formes(
    matrice: list[list[int]], formes: list[list[int]], can: Canvas
):
    """
    remplaces la matrice de 1 et de 0 en un cadrillage remplie de rectangles soit vert soit blanc
    elle met a jour l'interface graphique apres chaque jour, lors de chaque modification de la
    grille, nous modifions d'abord la matrices, et nous mettons l'interface a jour apres chaque
    modification grace a cette fonction
    Args:
        matrice (list[list[int]]): matrice contenant des 1 et des 0
        formes (list[list[int]]): matrice ou chaque case sont des rectangles
        can (Canvas): _description_
    """
    nb_ligne = len(matrice)
    nb_colonne = len(matrice[0])
    for y in range(nb_ligne):
        for x in range(nb_colonne):
            etat_cellule = matrice[y][x]
            id_forme = formes[y][x]
            if etat_cellule == 1:
                couleur = "green"
            else:
                couleur = "white"
            can.itemconfig(id_forme, fill=couleur)


def clique_affiche_matrice_aleatoire(affichage: Affichage, densite: float):
    """
    cette fonction met a jour un cadrillage ou la disposition des cases vivantes ou mortes sera en
    fonction de la densité et placer aléatoirement comme dans la fonction placement_aleatoire
    Args:
        affichage (Affichage): la class affichage contenant plusieurs variables
        densite (float): pourcentage de case noir par rapport au total de case
    """

    def tracer_matrice_alea():
        matrice_alea = placement_aleatoire(affichage.matrice, densite)
        mise_a_jour_couleur_formes(matrice_alea, affichage.formes, affichage.canevas)

    return tracer_matrice_alea


def avancer(affichage: Affichage) -> None:
    """Appelle le moteur et met à jour l'affichage

    Appelle cellule_naissance_mort qui met à jour la matrice.
    Appelle ensuite mise_a_jour_couleur_formes qui raffraichi les couleurs des cellules
    en fonction de leurs etats

    Args:
        affichage (Affichage): classe contenant les variables d'affichages et la matricce
    """
    affichage.matrice = cellule_naissance_mort(affichage.matrice)
    mise_a_jour_couleur_formes(
        affichage.matrice, affichage.formes, affichage.canevas
    )


def clique_bouton_avancer(affichage: Affichage) -> callable:
    """cette fonction renvoie une fonction que affiche l'etat du cadrillage

    ceci en fonction de la matrice apres un jour

    Args:
        affichage (Affichage): class affichage contenant plusieurs variables

    Returns:
        callable: retourne la fonction avance qui sera appeler lors d'un clic
    """

    def avance():
        avancer(affichage)

    return avance


def boucle_avance_auto(affichage: Affichage) -> callable:
    """Créé une fonction boucle qui se rappelle elle même a intervalle régulier

    Cette fonction avance d'un jour, met à jour l'affichage et utilise tkinter que se lancer elle
    même à nouveau dans le future.
    Args:
        affichage (Affichage): class affichage contenant plusieurs variables
    """

    def boucle():
        # On avance au jour suivant
        avancer(affichage)
        if affichage.avance_auto:
            # Si l'avance auto est toujours active on utilise tkinter pour
            # rappeler la fonction boucle dans 150millisecondes dans le future
            fonction_jour_suivant = boucle
            affichage.fenetre.after(150, fonction_jour_suivant)

    return boucle


def clique_depart_arret(affichage: Affichage, bouton: Button) -> callable:
    """
    lorsque le bouton est appuyer la fonction depart est appeler et le label du bouton
    change, puis nous pouvons stopper l'avancement en rapuyant sur le bouton
    Args:
        affichage (Affichage): class affichage contenant plusieurs variables
        bouton (Button): bouton sur lequelle nous changeons le label
    """

    def depart():
        if affichage.avance_auto is False:
            # on active l'avancement automatique
            affichage.avance_auto = True
            # on change le texte du bouton pour indiquer que si on re-appui
            # on arrête l'avancement auto
            bouton.configure(text="Arrêt")
            # On cré la fonction boucle avec affichage
            fonction_boucle = boucle_avance_auto(affichage)
            # on appelle la fonction boucle qui se rappelera elle-même à intervale régulier
            fonction_boucle()
        else:
            # on désactive l'avance auto
            # la fonction boucle arretera de se re-lancer automatiquement
            affichage.avance_auto = False
            # on change le texte du bouton pour indiquer que si on re-appui
            # on lance l'avancement auto
            bouton.configure(text="Départ")

    # on renvoie la fonction qui sera appeler par tkinter lors du clic sur le bouton Arrêt/Départ
    return depart


def affichage_vaisceau(affichage: Affichage, nb_colonne: int, nb_ligne: int) -> callable:
    """met a jour la matrice crée dans la fonction vaisceau du moteur
        grace a la fonction mise_a_jour_couleur_formes
    Args:
        affichage (Affichage): class affichage contenant plusieurs variables
        nb_colonne (int): nombre de colonne de la matrice
        nb_ligne (int): nombre de ligne de la matrice

    Returns:
        callable: retourne affiche_vaisceau
    """
    def affiche_vaisceau():
        affichage.matrice = vaisceau(nb_ligne, nb_colonne)
        mise_a_jour_couleur_formes(affichage.matrice, affichage.formes, affichage.canevas)
    return affiche_vaisceau


def main() -> None:
    fenetre = Tk()
    taille = 700
    nb_ligne = 50
    nb_colonne = 50
    densite = 0.5
    # Cré la matrice contenant les cellules
    matrice = grille_jeu_de_la_vie(nb_ligne, nb_colonne)
    can1 = Canvas(fenetre, bg="white", height=taille, width=taille)
    can1.pack(side=LEFT)
    grille(nb_ligne, nb_colonne, taille, can1)
    # Trace des rectangles dans la grille et renvoi une matrice de meme taille
    # que la matrice des cellule et contenant les identifiants des rectangles créés
    matrice_formes = trace_formes(nb_ligne, nb_colonne, taille, can1)
    affichage = Affichage(
        matrice=matrice,
        formes=matrice_formes,
        taille=taille,
        canevas=can1,
        fenetre=fenetre,
        )
    configure_clic_sur_forme(affichage)

    bouton_point = Button(
        fenetre, text="Aléatoire", command=clique_affiche_matrice_aleatoire(affichage, densite)
    )
    bouton_point.pack()

    bouton_avancer = Button(fenetre, text="Avancer", command=clique_bouton_avancer(affichage))
    bouton_avancer.pack()

    bouton_depart_arret = Button(fenetre, text="Depart")
    bouton_depart_arret.configure(command=clique_depart_arret(affichage, bouton_depart_arret))
    bouton_depart_arret.pack()

    bouton_vaisceau = Button(fenetre,
                             text='configurer un vaisceau',
                             command=affichage_vaisceau(affichage, nb_colonne, nb_ligne))
    bouton_vaisceau.pack()
    fenetre.mainloop()


if __name__ == "__main__":
    # technique utilisé pour éviter de lancer l'affichage
    # si le fichier est importer par un autre module
    # https://docs.python.org/fr/3.8/library/__main__.html
    main()
