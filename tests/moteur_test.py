import jeu_vie.moteur as moteur

def test_voisin_case():
    grille = moteur.grille_jeu_de_la_vie(10, 10)
    grille[5][5] = 1
    assert moteur.voisin_case(5, 5, grille) == 0
    assert moteur.voisin_case(4, 4, grille) == 1
    assert moteur.voisin_case(4, 5, grille) == 1
    assert moteur.voisin_case(4, 6, grille) == 1
    assert moteur.voisin_case(5, 4, grille) == 1
    assert moteur.voisin_case(5, 6, grille) == 1
    assert moteur.voisin_case(6, 4, grille) == 1
    assert moteur.voisin_case(6, 5, grille) == 1
    assert moteur.voisin_case(6, 6, grille) == 1
    assert moteur.voisin_case(3, 4, grille) == 0
    assert moteur.voisin_case(7, 4, grille) == 0
    assert moteur.voisin_case(5, 2, grille) == 0

    grille[4][5] = 1
    assert moteur.voisin_case(4, 4, grille) == 2

def test_cellule_naissance_mort():
    grille = moteur.grille_jeu_de_la_vie(5, 5)
    grille = moteur.cellule_naissance_mort(grille)
    assert moteur.somme_matrice(grille) == 0
    grille[2][1] = 1
    grille[2][2] = 1
    grille[2][3] = 1
    assert moteur.somme_matrice(grille) == 3
    grille = moteur.cellule_naissance_mort(grille)
    assert moteur.somme_matrice(grille) == 3
    assert grille[2][1] == 0
    assert grille[2][3] == 0
    assert grille[2][2] == 1
    assert grille[1][2] == 1
    assert grille[3][2] == 1

