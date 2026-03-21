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
            
            #construction de la dot

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

    # on fait le tri des plolygones selon leur surface à l'ordre décroissant
    
    polygones = list(polygones)
    polygones_triees = sorted(polygones, key=lambda p: abs(p.surface()), reverse=True) 
    arbre = Noeud("PLAN")
    
    # on associe a chaque polygones de la lsite de spolygones triées un noeud 

    noeuds = [Noeud(p) for p in polygones_triees] 
    
    for i in range(len(noeuds) - 1, -1, -1): # on parcourt les polygones à l'ordre croissant
        j = i - 1 # on considere initilament le plus petit 
                # polygone qui est plus grand que le polygone designe par la nuemrotation i
        
        # on verifie si tout les polygones plus grand que i le contient ou pas si oui on sort sinon on décremente j
        while j > -1 and (not polygones_triees[j].contient(polygones_triees[i])): 
            j -= 1 
            
        if j == -1: # si on n'a pas trouvé un polygone qui contient i alors il est directement issu du plan (il n est pas le fils d'aucun polygone) 
            arbre.ajouter_enfant(noeuds[i])
        else: #sinon il est le fils du plus petit polygone qui le contient
            noeuds[j].ajouter_enfant(noeuds[i])
    """
    
    Calcul de Complexité au pire des cas:
        au pire des cas on a le plus que possible de l'operation contient , ie
        que la  boucle while s'arrete seuleme,t lorsque j vaut -1 donc aucun polygone 
        contient aucun polygone.

        Le nombre de fois que while se répete dépend de la valeur de i donc si i = len(noeuds) -1
        contient se répete len(noeuds) - 2 fois , si i = i = len(noeuds) - 2 contient se repete (len(noeuds) -3) fois ..
        donc en notant len(noeuds) = n , au pire de cas on fait appel à contient:
        n-1 + n-2 + n-3 + .... + 1 = n*(n-1)/2 fois soit alors O(n**2) fois de contient:
        en plus que ça en notant k = max{p = nb points d'un polygone) ; pour tout les polygones} et en retournant à la definition
        de la fonction contient la fonction contient est bien O(p**2) avec p = point d'un polygone donc 
        pour tout les polygones on a bien O(p**2) = O(k**2)
        on conclut alors que la complexité au pire des cas de la fonction arbre_inclusion est bien
        O((n**2) * (k**2))
    
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
