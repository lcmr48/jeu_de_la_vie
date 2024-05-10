"""Module pour l'affichage du jeux."""

from dataclasses import dataclass
from tkinter import Canvas, Tk, Button, LEFT
from moteur import cellule_naissance_mort, placement_aleatoire, grille_jeu_de_la_vie


@dataclass
class Affichage:
    """Classe contenant l'etat de l'application"""

    matrice: list[list[int]]  # la matrice contenant les cellules
    formes: list[list[int]]  # une matrice contenant les identifiants des rectangles
    taille: int  # la taille du canevas en pixels
    canevas: Canvas  # le canevas contenant la grille
    fenetre: Tk  # la fenetre principale
    avance_auto: bool = False  # avancement automatique actif ou non


def dessiner_ligne(x1: int, y1: int, x2: int, y2: int, canvas: Canvas) -> None:
    """
    affiche une ligne dans le canvas
    Args:
        x1 (int): abscisse du point de départ
        y1 (int): ordonnée du point de départ
        x2 (int): abscisse du point de arrivée
        y2 (int): ordonnée du point de arrivée
        canvas (Canvas): _description_
    """
    largeur = 2
    canvas.create_line(x1, y1, x2, y2, width=largeur, fill="black")


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
        int: on retourne l'identifiant du rectangle se qui nous permet de l'identifier
    """
    return canvas.create_rectangle(x1, y1, x2, y2, fill="white")


def configure_clic_sur_forme(affichage: Affichage) -> None:
    """
    chaque rectangles a un identifiant qui permet de l'identifier, lors d'un clique sur le
    canvas donc dans un rectangles, un identifiant est donner, nous cherchons a quelle
    rectangles il appartient et nous changeons sa couleurs, se qui nous permet de changer
    les couleurs des cases en cliquant dessus.
    Args:
        affichage (Affichage): état de l'application
    """

    def clique_forme(x, y):
        """

        Args:
            y (_type_): indice du tableau dans la matrice
            x (_type_): indice de l'element dans ce tableau
        """

        def clique(_):
            if affichage.matrice[y][x] == 1:
                affichage.matrice[y][x] = 0
            else:
                affichage.matrice[y][x] = 1
            mise_a_jour_couleur_formes(
                affichage.matrice, affichage.formes, affichage.canevas
            )

        return clique

    for ymat, ligne in enumerate(affichage.formes):
        for xmat, _ in enumerate(ligne):
            forme = affichage.formes[ymat][xmat]
            affichage.canevas.tag_bind(
                forme, "<Button-1>", func=clique_forme(xmat, ymat)
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


def affiche_matrice_aleatoire(affichage: Affichage, densite: float):
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


def avancer(affichage: Affichage) -> callable:
    """
    cette fonction affiche l'etat du cadrillage en fonction de la matrice apres un jour
    Args:
        affichage (Affichage): class affichage contenant plusieurs variables

    Returns:
        callable: retourne la fonction avance
    """

    def avance():
        affichage.matrice = cellule_naissance_mort(affichage.matrice)
        mise_a_jour_couleur_formes(
            affichage.matrice, affichage.formes, affichage.canevas
        )

    return avance


def avance_auto(affichage: Affichage):
    """
    cette fonction affiche l'etat du cadrillage en fonction de la matrice apres un jour sans
    s'arreter avec une frequence d'avancement de 150ms
    Args:
        affichage (Affichage): class affichage contenant plusieurs variables
    """

    def boucle():
        avancer(affichage)()
        etape_suivante = avance_auto(affichage)
        if affichage.avance_auto:
            affichage.fenetre.after(150, etape_suivante)

    return boucle


def depart_arret(affichage: Affichage, bouton: Button):
    """
    lorsque le bouton est appuyer la fonction avance_auto est appeler et le label du bouton
    change, puis nous pouvons stopper l'avancement en rapuyant sur le bouton
    Args:
        affichage (Affichage): class affichage contenant plusieurs variables
        bouton (Button): bouton sur lequelle nous changeons le label
    """

    def depart():
        if affichage.avance_auto is False:
            affichage.avance_auto = True
            bouton.configure(text="Arrêt")
            avance_auto(affichage)()
        else:
            affichage.avance_auto = False
            bouton.configure(text="Départ")

    return depart


def main() -> None:
    """
    fonction principale
    """
    fenetre = Tk()
    taille = 700
    nb_ligne = 20
    nb_colonne = 20
    densite = 0.5
    matrice = grille_jeu_de_la_vie(nb_ligne, nb_colonne)
    can1 = Canvas(fenetre, bg="white", height=taille, width=taille)
    can1.pack(side=LEFT)
    grille(nb_ligne, nb_colonne, taille, can1)
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
        fenetre, text="Aléatoire", command=affiche_matrice_aleatoire(affichage, densite)
    )
    bouton_point.pack()

    bouton_avancer = Button(fenetre, text="Avancer", command=avancer(affichage))
    bouton_avancer.pack()

    bouton_depart_arret = Button(fenetre, text="Depart")
    bouton_depart_arret.configure(command=depart_arret(affichage, bouton_depart_arret))
    bouton_depart_arret.pack()

    fenetre.mainloop()


if __name__ == "__main__":
    main()
