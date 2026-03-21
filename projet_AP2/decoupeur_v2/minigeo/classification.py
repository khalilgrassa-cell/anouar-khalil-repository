from minigeo.polygone import Polygone
from minigeo.affichable import affiche
import subprocess

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
                    
                for enfant in noeud.enfants:
                    id_enfant = f"n{id(enfant.contenu)}"
                    lignes.append(f"    {identifiant} -> {id_enfant};")
                    pile.append(enfant)
                
            
            lignes.append("}")
            source_dot = "\n".join(lignes)
            print(source_dot)

            dot_path = "arbre.dot"
            png_path = "arbre.png"

            

            with open(dot_path, "w") as f:
                f.write(source_dot)

            # coversion au format png
            
            result = subprocess.run(
                ["dot", "-Tpng", dot_path, "-o", png_path],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                print("Erreur graphviz:", result.stderr)
                return

            subprocess.run(["kitty", "+kitten", "icat", png_path])

def arbre_inclusion(polygones):
    
    """
    prend un ensemble de polygones qui ne s'intersectent pas (hormis sur leur bord).
    renvoie un arbre (le noeud racine etant le plan) indiquant qui est inclu dans qui.
    pre-condition: pas de doublons, pas d'intersections hors bordures.
    """

    # on fait le tri des polygones selon la surface à l'ordre décroissant
    
    polygones = list(polygones)
    polygones_triees = sorted(polygones, key=lambda p: abs(p.surface()), reverse=True) 
    arbre = Noeud("PLAN")
    
    # on associe à chaque polygone de la liste des polygones triés un noeud 

    noeuds = [Noeud(p) for p in polygones_triees] 
    
    for i in range(len(noeuds) - 1, -1, -1): # on parcourt les polygones à l'ordre croissant
        j = i - 1 
        # on considère initialement le plus petit polygone qui est plus grand que le polygone désigné par i
        
        # on décrémente j jusqu'à ce qu'on trouve un polygone père ou j vaut -1

        while j > -1 and (not polygones_triees[j].contient(polygones_triees[i])): 
            j -= 1 
            
        if j == -1: # si on n'a pas trouvé un polygone qui contient i alors il est directement issu du plan (il n'est le fils d'aucun polygone) 
            arbre.ajouter_enfant(noeuds[i])
        else: # sinon il est le fils du polygone j 
            noeuds[j].ajouter_enfant(noeuds[i])
    """
    
    Calcul de complexité au pire cas :
 
    Soit n = nombre de polygones et k = nombre maximal de points d'un polygone.
 
    La boucle externe parcourt les n noeuds (indice i de n-1 à 0).
    Pour chaque i, la boucle while effectue au plus i appels à `contient`
    (elle s'arrête dès qu'un polygone contenant le polygone i est trouvé,
    ou lorsque j atteint -1 si aucun ne le contient).
 
    Le pire cas correspond à la situation où aucun polygone n'en contient un autre
    (tous les polygones sont disjoints) : la boucle while va jusqu'à j = -1
    pour chaque i. Le nombre total d'appels à `contient` est alors :
 
        (n-1) + (n-2) + ... + 1 = n*(n-1)/2 = O(n²)
 
    Complexité de `contient(self, autre)` :
    La méthode calcule d'abord les coordonnées x pertinentes en O(k),
    puis pour chaque y trouvé sur la droite verticale (au plus O(k) valeurs),
    elle appelle `contient_point` qui parcourt tous les segments de self en O(k).
    La complexité de `contient` est donc O(k²).
 
    Complexité totale de `arbre_inclusion` :
 
        O(n²) appels à contient * O(k²) par appel = O(n² * k²)
 
    """
 
    return arbre


def main():
    p1 = Polygone.carre((0, 0), 10)
    p2 = Polygone.carre((0, 0), 8)

    p3 = Polygone.carre((15, 15),5)
    p5 = Polygone.carre((0, 0), 1)
    p4 = Polygone.carre((-3, -3), 2)
    polygones = [p1 , p2 , p3 , p4 , p5]
    affiche(polygones)
    racine = arbre_inclusion(polygones)
    racine.affichage()


if __name__ == "__main__":
    main()
