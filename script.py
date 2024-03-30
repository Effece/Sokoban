### IMPORTATION DES MODULES ###

import lvls as l

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### VALEURS INITIALES ###

# copie des niveaux dans lvls l
levels_save = l.levels_save

# levels_no_cross est la première étape pour séparer les croix du reste, puisque celles-ci sont superposables

levels_no_cross = [[j[:] for j in i] for i in levels_save]

# après avoir copié la liste, il faut changer tous les 2 (croix) en 0 (vide)
for i in levels_no_cross:
    for j in i:
        for k in j:
            if k == 2:
                k = 0

# on finit d'initialiser les variables et listes, en copiant levels_no_cross dans levels
# levels est une liste de tous les niveaux
#lorsqu'un élément bouge, levels[cur] (niveau actuel) s'adapte au mouvement ; mais après un restart ou un changement de niveau, levels[cur] (niveau actuel) redevient comme avant (levels_no_cross[cur])
levels = [[j[:] for j in i] for i in levels_no_cross]

# chaque point possède une liste, avec son index et, surtout, s'il est une croix (avec l'analyse 'j[k] == 2')
# c'est peut-être assez inoptimal
cross = [[[[k, j[k] == 2] for k in range(len(j))] for j in i] for i in levels_save]

# cur sert à désigner le niveau actuel ; automatiquement, il est défini sur 0, le premier niveau
# cur est utilisé pour trouver le niveau actuel en faisant 'levels[cur]' ou 'cross[cur]'
cur = 0

# sauvegarde de l'historique ; on compte dans une variable combien d'utilisations sont autorisées
history = []
hist_allowed = 3

# nombre de mouvements
nb_moves = 0

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### OBTENTION DES VALEURS ###

def gate():
    """Renvoie la grille du niveau actuel"""
    """
    Out :
      la grille du niveau actuel (levels[cur])
    """
    
    global cur
    
    if cur >= len(levels_save):
        cur = 0
    t = [len(k) for k in levels[cur]]
    if t.count(t[0]) == len(t):
        return levels[cur]
    else:
        return levels[0]

def gateC():
    """Renvoie la grille des croix du niveau actuel"""
    """
    Out :
      la grille avec les croix du niveau actuel (cross[cur])
    """

    global cur

    # analyse refaite souvent pour vérifier que cur n'est pas trop grand pour le nombre de niveaux
    if cur >= len(levels_save):
        cur = 0
    
    return cross[cur]

def get_cur():
    """Renvoie la variable CUR, du niveau actuel"""
    """
    Out :
      le niveau actuel (cur)
    """
    
    global cur

    # analyse refaite souvent pour vérifier que cur n'est pas trop grand pour le nombre de niveaux
    if cur >= len(levels_save):
        cur = 0
    
    return cur

def get_levels():
    """Renvoie la grille des niveaux"""
    """
    Out :
      la liste de tous les niveaux (avec l'actuel tel qu'il est représenté)
    """
    
    return levels

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### VALEURS UTILES ###

# valeurs permettant, si le premier niveau n'a qu'un seul joueur et qu'il n'est pas donné avec des x et y, de lui en donner
# si l'on veut peut-être élargir la technique à plusieurs joueurs, il faut retirer les '[0]' et ajouter des indexs à quelques endroits
x1 = [levels[0].index(k) for k in levels[cur] if - 1 in k][0]
x2 = [k.index(- 1) for k in levels[cur] if - 1 in k][0]

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### CREATION DES JOUEURS ###

class event:
    """Permet de créer un faux EVENT de Tkinter pour éxecuter des tests dans la console"""
    
    def __init__(self, keycode):
        """
        In :
          keycode : valeur du keycode demandée (37, 38, 39 ou 40 pour les flèches)
        """

        # ajout de la valeur keycode à self pour l'utilisation ultérieure
        self.keycode = keycode

        return

class player:
    """Class d'un joueur"""

    ALL = []
    nb = 0

    def __init__(self, x = x1, y = x2):
        """
        In :
          x = x1 : abscisse de départ du joueur
          y = x2 : ordonnée de départ du joueur
        """

        # ajout de self à player.ALL et (bien qu'inutile et non actualisé) augmentation de player.nb
        # l'ajout à player.ALL permet de retrouver facilement la trace du joueur
        player.ALL.append(self)
        player.nb += 1
        
        self.x, self.y = x, y

        return

    def get_c_move(self, event = None):
        """Donne les conditions de mouvement vers le haut, le bas, la droite et la gauche du joueur"""
        """
        In :
          event=None : obj de tk
        Out :
          c_up, c_do, c_ri, c_le
        """

        # afin de vérifier si le joueur peut bouger, on analyse :
        #   si le keycode est le bon                                                                                      | 'event.keycode == {}'
        #   si l'élément devant n'est pas un joueur ou un mur                                                             | '{not} gate()[self.x{}][self.y{}] in [- 1, 3]'
        #   si l'élément devant la position future n'est pas une caisse bloquée par un joueur, une autre caisse ou un mur | '{not} gate()[self.x{}][self.y{}] == 1 and {}gate()[self.x{}][self.y{}] in [- 1, 1, 3]'
        # pour c_up et c_le (up et left), on vérifie également que les coordonnées des positions devant ne sont pas négatives (ce qui renverrait aux derniers items)
        # la vérification pour c_do et c_ri (down et right) est faite par le 'try', qui évite l'erreur d'index supérieur à la longueur de la liste

        # c_up : condition up, c_do : condition down, c_ri : condition right, c_le : condition left
        
        try:
            c_up = event.keycode == 38 and not (gate()[self.x][self.y-1] in [- 1, 3] or (gate()[self.x][self.y-1] == 1 and (gate()[self.x][self.y-2] in [- 1, 1, 3] or self.y - 2 < 0)) or self.y - 1 < 0)
        except Exception:
            c_up = False
        try:
            c_do = event.keycode == 40 and not (gate()[self.x][self.y+1] in [- 1, 3] or (gate()[self.x][self.y+1] == 1 and gate()[self.x][self.y+2] in [- 1, 1, 3]))
        except Exception:
            c_do = False
        try:
            c_ri = event.keycode == 39 and not (gate()[self.x+1][self.y] in [- 1, 3] or (gate()[self.x+1][self.y] == 1 and gate()[self.x+2][self.y] in [- 1, 1, 3]))
        except Exception:
            c_ri = False
        try:
            c_le = event.keycode == 37 and not (gate()[self.x-1][self.y] in [- 1, 3] or (gate()[self.x-1][self.y] == 1 and (gate()[self.x-2][self.y] in [- 1, 1, 3] or self.x - 2 < 0))  or self.x - 1 < 0)
        except Exception:
            c_le = False

        return (c_up, c_do, c_ri, c_le)

    def move(self, event = None):
        """Permet de bouger un joueur et, parfois, une caisse"""
        """
        In :
          event = None : objet de tkinter tk lié à un bind avec ses propriétés
        Out :
          le résultat des conditions de déplacement du joueur (c_up, c_do, c_ri et c_le)
          les coordonnées de la caisse déplacée (- 1 si aucune n'a été déplacée)
        """

        # on trouve déjà si le joueur va bien pouvoir bouger vers le haut, le bas, la droite ou la gauche
        c_all = self.get_c_move(event)
        c_up, c_do, c_ri, c_le = c_all[0], c_all[1], c_all[2], c_all[3]

        # 'returned' est une liste de ce qui sera renvoyé (les conditions précédentes et les coordonnées d'une boîte déplacée (s'il y en a une)
        # returned[1] est défini de base sur - 1, ce qui veut dire qu'aucune caisse n'a été déplacée
        returned = [(c_up, c_do, c_ri, c_le), (- 1, - 1)]

        # si on peut bouger le joueur
        if c_up or c_do or c_ri or c_le:

            # on change l'endroit où il était par 0
            levels[cur][self.x][self.y] = 0

            # pour chaque mouvement possible, on change soit self.x, soit self.y
            # si une caisse a été touchée à la nouvelle position ('gate()[self.x][self.y] == 1') :
            #   on change sa future position par 1
            #   on change returned[1] avec les coordonnées de cette caisse
            #   on actualise la valeur de l'élément de gateC (croix activée ou non) en fonction de la position de la caisse, si comprise dans le premier élément des listes ('k[0]') de chaque élément de sa ligne

            # si le mouvement est vers le haut
            if c_up:
                self.y -= 1
                if gate()[self.x][self.y] == 1:
                    levels[cur][self.x][self.y - 1] = 1
                    returned[1] = (self.x, self.y - 1)
                    e = cross[cur][self.x][self.y - 1]
                    e[1] = not (self.y - 1 in [k[0] for k in gateC()[self.x]])

            # si le mouvement est vers le bas
            elif c_do:
                self.y += 1
                if gate()[self.x][self.y] == 1:
                    levels[cur][self.x][self.y+1] = 1
                    returned[1] = (self.x, self.y+1)
                    e = cross[cur][self.x][self.y+1]
                    e[1] = not (self.y+1 in [k[0] for k in gateC()[self.x]])

            # si le mouvement est vers la droite
            elif c_ri:
                self.x += 1
                if gate()[self.x][self.y] == 1:
                    levels[cur][self.x+1][self.y] = 1
                    returned[1] = (self.x+1, self.y)
                    e = cross[cur][self.x+1][self.y]
                    e[1] = not (self.y in [k[0] for k in gateC()[self.x+1]])

            # si le mouvement est vers la gauche
            elif c_le:
                self.x -= 1
                if gate()[self.x][self.y] == 1:
                    levels[cur][self.x- 1][self.y] = 1
                    returned[1] = (self.x- 1, self.y)
                    e = cross[cur][self.x- 1][self.y]
                    e[1] = not (self.y in [k[0] for k in gateC()[self.x- 1]])

            if not gateC()[self.x][self.y][1] and levels_save[cur][self.x][self.y] == 2:
                cross[cur][self.x][self.y][1] = True

            # on actualise la grille avec la position actuelle du joueur
            levels[cur][self.x][self.y] = - 1

        return returned

    def repos(self, x, y):
        """Actualise les coordonnées du joueur"""
        """
        In :
          x : la future abscisse du joueur
          y : la future ordonnée du joueur
        """
        
        self.x, self.y = x, y

        return

    def repos_all(cls):
        """Actualise les coordonnées de tous les joueurs"""

        # on récupère dans p toutes les positions des joueurs sur la grille (qui est souvent réinitialisée avant)
        p = []
        for i in range(len(gate())):
            for j in range(len(gate()[i])):
                if j == - 1:
                    p.append((i, j))

        # on repositionne chaque joueur avec les coordonnées obtenues précédemment
        for k in ALL:
            tup = p.pop()
            k.repos(tup[0], tup[1])

        # cette partie de programme doit pouvoir s'alleger si on fusionne les deux boucles, on repositionnant directement un joueur quand on obtient une position
        
        return

    repos_all = classmethod(repos_all)

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### FONCTION RESTART ###

def restart():
    """Fait le niveau actuel recommencer"""

    # pour l'instant, juste une simple commande, mais cela peut être améliorer facilement

    new_level(actu=False)
    
    #x1 = [levels[cur].index(k) for k in levels[cur] if - 1 in k][0]
    #x2 = [k.index(- 1) for k in levels[cur] if - 1 in k][0]
    #for k in player.ALL:
    #    k.repos(x1, x2)

    return

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### FONCTIONS HISTORY ###

def save_history():
    """Sauvegarde l'historique"""

    global history

    history.append([k[:] for k in levels[cur]])
    try:
        if history[- 1] == history[-2]:
            history.pop()
    except Exception:
        pass

    return

def undo(prt):
    """Annule le dernier mouvement"""
    """
    In :
      prt : la partie du script à éxecuter
    """

    global hist_allowed, history, levels, cross

    if prt == 1:

        levels[cur] = history.pop()
        hist_allowed -= 3

        # on trouve toutes les positions possibles pour les joueurs (tx1 et x1 pour x, tx2 et x2 pour y)

        tx1 = [[k]*levels[cur][k].count(- 1) for k in range(len(levels[cur])) if - 1 in levels[cur][k]]
        tx2 = []
        for i in levels[cur]:
            # t contient tous les indexs des - 1 dans la colonne actuelle i
            # si t n'est pas vide, on l'ajoute à tx2
            t = [j for j in range(len(i)) if i[j] == - 1]
            if len(t) > 0:
                tx2.append(t)

        # tx1 et tx2 sont des listes de listes ; on les fusionne dans x1 et x2 pour en faire des simples listes dont les éléments sont liés par leurs indexs
        x1, x2 = [], []
        for k in tx1:
            x1 += k
        for k in tx2:
            x2 += k

        return (x1, x2)

    elif prt == 2:

        # on recréé toutes les croix
        for i in range(len(levels[cur])):
            for j in range(len(levels[cur][i])):
                cross[cur][i][j][1] = levels_save[cur][i][j] == 2

        return

    elif prt == 3:
        
        for i in range(len(levels[cur])):
            for j in range(len(levels[cur][i])):
                cross[cur][i][j][1] = levels_save[cur][i][j] == 2 and levels[cur][i][j] != 1

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### FONCTIONS DE CHANGEMENT DE NIVEAU ###

def check_end(ins=False, want_ins=True):
    """Renvoie si le niveau est terminé"""
    """
    In :
      ins=False     : permet de directement passer au prochain niveau ; variable intérieure au programme, à ne pas spéficier en dehors (console ou interface)
      want_ins=True : permet de gérer si le programme passe automatiquement au prochain niveau (peu recommandé)
    Out :
      un boolean affirmant si le niveau est fini ou non
    """

    # si l'on veut automatiquement passer au niveau suivant
    if want_ins and not ins:
        if check_end(True, want_ins):
            new_level()
            player.repos_all()

    # on "additionne" (addition de booleans) toutes les valeurs des croix du niveau actuel (si la croix est valide pour chaque élément) et on compare à 0 ; si toutes les croix sont "désactivées" (une caisse dessus), cette somme renvoie 0 et le boolean est validé
    return sum([sum([k[1] for k in i]) for i in gateC()]) == 0

def new_level(actu=True):
    """Actualise et reset la grille et parfois cur"""
    """
    In :
      actu=True : boolean qui détermine si CUR doit être incrémenté
    """
    
    global cur, history, hist_allowed

    # réinitialisation du niveau actuel dans levels et cross
    levels[cur] = [k[:] for k in levels_no_cross[cur]]
    cross[cur] = [[[j, i[j] == 2] for j in range(len(i))] for i in levels_save[cur]]

    # réinitialisation de l'historique
    history = []
    hist_allowed = 3

    # réinitialisation du nombre de mouvements
    nb_moves = 0

    # destruction de tous les joueurs et réinitialisation de player.ALL
    # player.ALL n'est pas rerempli ici, il est mieux de le reremplir dans le programme utilisant ce module, puisque la classe player doit être étendue
    for k in player.ALL:
        del k
    player.ALL = []

    # si demandé, la valeur de cur est incrémentée
    if actu:
        cur += 1
        if cur > len(levels_save):
            cur = 0
    
    return

def get_score():
    """Renvoie le score effectué"""
    """
    Out :
      score effectué
    """

    s = 0
    s += hist_allowed * 10
    s += (50 - nb_moves) * 5

    return s

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### MAIN ###

if __name__ == '__main__':
    pass
