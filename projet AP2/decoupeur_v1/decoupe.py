#!/usr/bin/env python3
from sys import argv
from minigeo.stl import facettes_stl_binaire
from minigeo.affichable import affiche
from minigeo.utils import multiples_entre

def decoupe(facettes, epaisseur):

    """
    renvoie un vecteur de vecteurs de segments.
    chaque vecteur interne contient tous les segments 2d d'une seule tranche.
    le vecteur externe contient toutes les coupes de tranches de la plus basse
    (x minimal) a la plus haute (x maximal).
    """

    z_min_liste_facette = min(f.zmin_et_zmax()[0] for f in facettes) # on cherche la hauteur minimal de notre objet
    z_max_liste_facette = max(f.zmin_et_zmax()[1] for f in facettes) # on cherche la hauteur maximal de notre objet 
    tranches = []
    for hauteur in multiples_entre(z_min_liste_facette, z_max_liste_facette, epaisseur): # on parcourt les tranches choisis par l'epaisseur 
        segments_tranche = []
        for facette in facettes: # on parcourt nos facettes
            zmin , zmax = facette.zmin_et_zmax() # on cherche les hauteurs minimal et maximal de notre facette
            if not facette.est_horizontale(): # on verifie si notre facettte n'est pas horizontale , dans le cas écheant on coupe rien
                if zmin <= hauteur <= zmax : # on verifie que la facette est située dans une altitude qui aboutit à une coupure gagnante
                    segments = facette.intersection_plan_horizontal(hauteur) # on récupére les segments issus d'une découpe avec la methode intersection_plan_horizontal
                    segments_tranche.extend(segments) # on ajoute les segments issus de la decoupe a la liste des semgments issus de la decoupe des factettes de cette tranche
          
        tranches.append(segments_tranche) # on ajoute le vecteur de segments à la liste des coupures des tranches
    return tranches

def main():

    if len(argv) != 3:
        print("donnez un nom de fichier stl, une epaisseur de tranches")
        exit()
    fichier_stl = argv[1]
    epaisseur = float(argv[2])

    facettes = list(
        f for f in facettes_stl_binaire(fichier_stl) if not f.est_horizontale()
    )
    print("on a charge", len(facettes), "facettes")

    tranches = decoupe(facettes, epaisseur)

    for tranche in tranches:
        affiche(tranche)

if __name__ == "__main__":
    main()
