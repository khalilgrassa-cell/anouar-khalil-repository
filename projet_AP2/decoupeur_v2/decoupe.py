#!/usr/bin/env python3
from sys import argv
from minigeo.stl import facettes_stl_binaire
from minigeo.affichable import affiche
from minigeo.utils import multiples_entre
from minigeo.doublons import suppression_doublons
from minigeo.polygone import construction_polygones
from minigeo.classification import arbre_inclusion


# un algo un peu lent pour la decoupe

def decoupe(facettes, epaisseur):
    zmin = min(z for f in facettes for _, _, z in f.points)
    zmax = max(z for f in facettes for _, _, z in f.points)
    tranches = []
    for hauteur in multiples_entre(zmin, zmax, epaisseur):
        facettes_tranche = []
        for facette in facettes:
            facettes_tranche.extend(facette.intersection_plan_horizontal(hauteur))
        tranches.append(facettes_tranche)
    return tranches


def traitement_tranche(segments):
    segments_dedoublonnes = suppression_doublons(segments)
    affiche(segments_dedoublonnes)
    polygones = construction_polygones(segments_dedoublonnes)
    
    print(f"on a {len(polygones)} polygones")
    affiche(polygones)
    hierarchie = arbre_inclusion(polygones)
    hierarchie.affichage()


def main():
    if len(argv) != 4:
        print(
            "donnez un nom de fichier stl, une epaisseur de tranches, un numero de tranche a traiter"
        )
        exit()
    fichier_stl = argv[1]
    epaisseur = float(argv[2])
    tranche_cible = int(argv[3])

    facettes = list(
        f for f in facettes_stl_binaire(fichier_stl) if not f.est_horizontale()
    )
    print("on a charge", len(facettes), "facettes")

    tranches = decoupe(facettes, epaisseur)

    # for tranche in tranches:
    #     affiche(tranche)

    traitement_tranche(tranches[tranche_cible])

if __name__ == "__main__":
    main()
