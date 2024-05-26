"""Moteur du jeux."""

import random


def grille_jeu_de_la_vie(y: int, x: int) -> list[list[int]]:
    """
    créer une matrice qui représente la grille du jeu de la vie avec 0 = mort et 1 = vivant

    Args:
        y (int): nombre de tableaux dans matrice
        x (int): nombre d'elements par tableaux

    Returns:
        list[list[int]]: matrice contenant des 0
    """
    return [[0 for i in range(x)] for j in range(y)]


def placement_aleatoire(matrice: list[list[int]], densite: float) -> list[list[int]]:
    """
    place aleatoirement une densité de 1 dans la matrice remplie préalablement de 0

    Args:
        matrice (list[list[int]]): matrice contenant des 0
        densite (float): pourcatage de nombre 1 dans la matrice

    Returns:
        list[list[int]]: matrice avec une densité de 1 donner et placer aléatoirement
    """
    for y in range(len(matrice)):
        for x in range(len(matrice[y])):
            if random.random() <= densite:
                matrice[y][x] = 1
            else:
                matrice[y][x] = 0
    return matrice


def voisin_case(y: int, x: int, matrice: list[list[int]]):
    """
    cherche le nombre de voisin d'une case donnée en parametre et le retourne en un entier

    Args:
        y (int): indice du tableau ou se trouve l'élement
        x (int): indice element dont nous voulons savoir le nombre de voisin dans le tableau
        matrice (list[list[int]]): _description_

    Returns:
        _type_: nombre de voisin de la case
    """
    nb_voisin = 0
    tab_actuelle = y - 1
    for j in range(3):
        if tab_actuelle >= 0 and tab_actuelle < len(matrice) and x != 0:
            if matrice[tab_actuelle][x - 1] == 1:
                nb_voisin = nb_voisin + 1
        if tab_actuelle >= 0 and tab_actuelle < len(matrice) and tab_actuelle != y:
            if matrice[tab_actuelle][x] == 1:
                nb_voisin = nb_voisin + 1
        if (
            tab_actuelle >= 0
            and tab_actuelle < len(matrice)
            and x != len(matrice[y]) - 1
        ):
            if matrice[tab_actuelle][x + 1] == 1:
                nb_voisin = nb_voisin + 1
        tab_actuelle = tab_actuelle + 1
    return nb_voisin


def somme_matrice(matrice: list[list[int]]) -> int:
    """
    renvoie le somme du nombre d'indice dans la matrice

    Args:
        matrice (list[list[int]]): matrice représentant la grille

    Returns:
        int: nombre d'element de la matrice
    """
    n = 0
    for tab in matrice:
        for i in tab:
            n = n + i

    return n


# une cellule meurt si elle possède moins de deux ou plus de trois cases voisines vivantes
def cellule_naissance_mort(matrice: list[list[int]]) -> list[list[int]]:
    """
    effectue l'équivalent d'une journée avec la matrice en argument et renvoie la matrice
    aprees une journée en respectant les regles du jeu de la vie et les cases sont des indices.
    Args:
        matrice (list[list[int]]): matrice représentant la grille

    Returns:
        list[list[int]]: nouveau tableau apres une étape ( un jour )
    """
    tableau_fin = []
    mort = 0
    for i in range(len(matrice)):
        tableau_2 = []
        for j in range(len(matrice[i])):
            voisins = voisin_case(i, j, matrice)
            if voisins < 2 or voisins > 3:
                tableau_2.append(mort)
            else:
                tableau_2.append(matrice[i][j])
            if voisins == 3:
                tableau_2[j] = 1
        tableau_fin.append(tableau_2)
    matrice = tableau_fin
    return matrice


def vaisceau(nb_ligne: int, nb_colonne: int) -> list[list[int]]:
    """crée une matrice de 0 en fonction du nombre de colonne et de ligne

        puis on place les 1 dans la matrices pour configurer
        un vaisceau dans le jeu de la vie

    Args:
        nb_ligne (int): nombre de tableau dans la matrice
        nb_colonne (int): nombre d'élément dans le tableau

    Returns:
        list[list[int]]: matrice avec le vaisceau
    """
    matrice = grille_jeu_de_la_vie(nb_colonne, nb_ligne)
    matrice[nb_ligne - 2][1] = 1
    matrice[nb_ligne - 4][1] = 1
    matrice[nb_ligne - 5][2] = 1
    matrice[nb_ligne - 5][3] = 1
    matrice[nb_ligne - 5][4] = 1
    matrice[nb_ligne - 5][5] = 1
    matrice[nb_ligne - 4][5] = 1
    matrice[nb_ligne - 3][5] = 1
    matrice[nb_ligne - 2][4] = 1
    return matrice
