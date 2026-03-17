from minigeo.polygone import Polygone
from minigeo.affichable import affiche
import subprocess
import tempfile
import os


class Noeud:
    def __init__(self, contenu):
        self.contenu = contenu
        self.enfants = []
    
    def ajouter_enfant(self, noeud):
        self.enfants.append(noeud)


    def affichage(self):
            """
            creation d'un fichier dot, conversion en png et affichage dans kitty
            """
            
            # construction de la dot
            lignes = ["digraph g {"]
            pile = [self]
            
            while pile :
                noeud = pile.pop()
                if noeud.contenu == "PLAN":
                    identifiant = "nPLAN"
                elif len(noeud.enfants) != 0 and noeud.contenu != "PLAN":
                    identifiant = f"n{id(noeud.contenu)}"
                    lignes.append(f"    {identifiant};")
                for enfant in noeud.enfants:
                    id_enfant = f"n{id(enfant.contenu)}"
                    lignes.append(f"    {identifiant} -> {id_enfant};")
                    pile.append(enfant)
                
            lignes.append("}")
            source_dot = "\n".join(lignes)

            print(source_dot)

            # convertir la dot en png puis affichage sur kitty
            
            with tempfile.TemporaryDirectory() as tmpdir:
                dot_path = os.path.join(tmpdir, "arbre.dot")
                png_path = os.path.join(tmpdir, "arbre.png")

                with open(dot_path, "w") as f:
                    f.write(source_dot)

                result = subprocess.run(
                    ["dot", "-Tpng", dot_path, "-o", png_path],
                    capture_output=True, text=True
                )
                if result.returncode != 0:
                    
                    return

                subprocess.run(["kitty", "+kitten", "icat", png_path])

def arbre_inclusion(polygones):
    """
    prend un ensemble de polygones qui ne s'intersectent pas (hormis sur leur bord).
    renvoie un arbre (le noeud racine etant le plan) indiquant qui est inclu dans qui.
    pre-condition: pas de doublons, pas d'intersections hors bordures.
    """
    polygones = list(polygones)
    polygones_triees = sorted(polygones, key=lambda p: p.surface(), reverse=True)
    arbre = Noeud("PLAN")
    noeuds = [Noeud(p) for p in polygones_triees] 
    for i in range(len(noeuds) - 1, -1, -1):
        j = i - 1
        while j > -1 and (not polygones_triees[j].contient(polygones_triees[i])):
            j -= 1 
        if j == -1:
            arbre.ajouter_enfant(noeuds[i])
        else:
            noeuds[j].ajouter_enfant(noeuds[i])
    return arbre

def main():
    p1 = Polygone.carre((0, 0), 10)
    p2 = Polygone.carre((0, 0), 8)
    p3 = Polygone.carre((-2, -2), 2)
    p4 = Polygone.carre((2, 2), 1)
    p5 = Polygone.carre((15, 15), 5)
    polygones = [p1, p4, p3, p2, p5]
    affiche(*polygones)
    racine = arbre_inclusion(polygones)
    racine.affichage()


if __name__ == "__main__":
    main()
