### IMPORTATION DES MODULES ###

import tkinter as tk

import time as time

import script as m
import graphics as g

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### CREATION DE LA FENETRE ###

win = tk.Tk()
win.title('Sokoban')

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### CREATION DES CONSTANTES ###

class r:
    """Ensemble des constantes initiales"""

    # le module graphics contient des données (rap, des, fill_can) qui peuvent être utiles et sont donc récupérées ici
    
    rap = g.r.rap
    des = g.r.des

    fill_can = g.r.fill_can

    # vitesse d'arrivée du bouton next
    v_butnext = 20

    # temps maximal
    max_t = len(m.levels[m.cur]) * len(m.levels[m.cur][0])

    # taille de laquelle déplacer un objet (comme le timer) pour s'assurer qu'il ne soit pas visible lors d'un changement de taille du Canvas
    outscreen = 1000

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### CREATION DU CANVAS ###

class new_can(tk.Canvas):
    """Nouveau Canvas"""

    def __init__(self, width = None, height = None):
        """
        In :
          width = None  : taille possible du Canvas (width)
          height = None : taille possible du Canvas (height)
        """

        if width == None or height == None:
            # si aucune donnée n'est fournie, la taille du Canvas est adaptée à la taille de la grille
            # sinon, elle est adaptée aux critères
            self.width, self.height = len(m.gate()) * r.rap, len(m.gate()[0]) * r.rap
        else:
            self.width, self.height = width, height
        self.bg = r.fill_can
        
        tk.Canvas.__init__(self, win, width = self.width, height = self.height, bg = self.bg)

        self.grid(row = 0, column = 0, sticky = 'n')

        return

    def update_size(self, width = None, height = None):
        """Actualise la taille du Canvas"""
        """
        In :
          width = None  : taille possible du nouveau Canvas (width)
          height = None : taille possible du nouveau Canvas (height)
        """

        # si aucune donnée n'est fournie, la taille du Canvas est adaptée à la taille de la grille
        # sinon, elle est adaptée aux critères
        if width == None or height == None:
            self.width, self.height = len(m.gate()) * r.rap, len(m.gate()[0]) * r.rap
        else:
            self.width, self.height = width, height

        self.config(width = self.width, height = self.height)

        return

    def move(self, obj, x, y):
        """Permet de bouger un objet OBJ_DESIGN dans le Canvas"""
        """
        In :
          obj : ensemble d'objets dans le Canvas à bouger des mêmes coordonnées
          x   : valeur de changement sur l'abscisse de obj
          y   : valeur de changement sur l'ordonnée de obj
        """
        # obj est de type "obj_design" dans le module graphics g ; c'est une liste d'éléments can.create
        
        for k in obj:
            # on récupère chaque élément de obj (qui est une liste), des can.create, et on applique la formule basique move d'un Canvas dessus
            super(new_can, self).move(k, x, y)

        return

    def lift(self, obj):
        """Met au premier plan un objet"""
        """
        In :
          obj : ensemble d'objets dans le Canvas à mettre au premier plan
        """

        for k in obj:
            # on récupère chaque élément de obj (qui est une liste), des can.create, et on applique la formule basique lift d'un Canvas dessus
            super(new_can, self).lift(k)

        return

    def delete(self, obj):
        """Permet de détruire un objet OBJ_DESIGN dans le Canvas"""
        """
        In :
          obj : ensemble d'objets dans le Canvas à détruire
        """
        # obj est de type "obj_design" dans le module graphics g ; c'est une liste d'éléments can.create

        for k in obj:
            # on récupère chaque élément de obj (qui est une liste), des can.create, et on applique la formule basique delete d'un Canvas dessus
            super(new_can, self).delete(k)

        return

    def click(self, event = None):
        """Détection et traitement d'un clique dans le Canvas"""
        """
        In :
          event = None : objet de tkinter tk lié à un bind avec ses propriétés
        """

        for k in new_button.ALL:
            # si le clique a été fait dans le bouton
            if k.x < event.x < k.x + k.width and k.y < event.y < k.y + k.height:
                eval(k.command)

        return

    def motion(self, event = None):
        """Détection et traitement d'un mouvement de souris dans le Canvas"""
        """
        In :
          event = None : objet de tkinter tk lié à un bind avec ses propriétés
        """

        for k in new_button.ALL:
            # si le pointeur est allé dans le bouton
            if k.x < event.x < k.x + k.width and k.y < event.y < k.y + k.height:
                k.view.color_motion()
                k.is_touched = True
            elif k.is_touched:
                k.is_touched = False
                k.view.usual_color()

        return

can = new_can()

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### CREATION DU BOUTON ###

class new_button:
    """Pour tous les boutons à créer sur le Canvas"""

    ALL = []
    commands = {50: 'restart()', 51: 'keep()', 52: 'undo()'}

    def __init__(self, master, nb, width = r.rap, height = r.rap, x = None, y = None):
        """
        In :
          master         : le Canvas dans lequel le bouton doit se trouver
          width = r.rap  : la largeur du bouton
          height = r.rap : la hauteur du bouton
          x = None       : l'abscisse initiale du bouton
          y = None       : l'ordonnée initiale du bouton
        """

        new_button.ALL.append(self)

        # sauvegarde du Canvas associé et de la commande associée à NB
        self.master, self.nb = master, nb
        self.command = new_button.commands[self.nb]

        self.width, self.height = width, height

        # si aucune donnée n'a été fournie pour x et y
        if x == None or y == None:
            if self.nb == 50:
                self.x, self.y = self.master.width - r.des-self.width, r.des
            elif self.nb == 51:
                self.x, self.y = (self.master.width - self.width) / 2, (self.master.height - self.height) / 2 + self.master.height
            elif self.nb == 52:
                #self.x, self.y = r.des, r.des
                self.x, self.y = self.master.width - (r.des + self.width) * 2, r.des
        else:
            self.x, self.y = x, y

        self.view = g.obj_design(master, self.nb, self.x, self.y, self.x + self.width, self.y+self.height)

        self.is_touched = False

        return

    def refresh_view(self):
        """Permet de recharger la représentation du bouton (mettre au premier plan)"""

        if self.nb == 50:
            self.x, self.y = self.master.width-r.des - self.width, r.des
        elif self.nb == 51:
            self.x, self.y = (self.master.width - self.width) / 2, (self.master.height - self.height) / 2 + self.master.height
        elif self.nb == 52:
            self.x, self.y = self.master.width - (r.des + self.width) * 2, r.des

        # destruction puis recréation de new_button.view
        self.master.delete(self.view)
        self.view = g.obj_design(self.master, self.nb, self.x, self.y, self.x + self.width, self.y + self.height)

        return

    def show(self):
        """Fait apparaître un bouton tel qu'un 51, situé à sa coordonnée y future + la hauteur du Canvas"""

        v = r.v_butnext
        
        # on avance progressivement le bouton
        for k in range(self.master.height // v):
            self.master.move(self.view, 0, - v)
            self.y -= v
            time.sleep(0.01)
            can.update()

        #puisqu'on a fait une division euclidienne ('self.master.height // v'), il peut rester quelques imperfections, corrigées ici
        rest = abs(self.master.height // 2 - self.y - self.height // 2)
        self.y -= rest
        self.master.move(self.view, 0, - rest)

        return

    def hide(self):
        """Fait disparaître un bouton tel qu'un 51, en le positionnant à sa coordonnée y actuelle + la hauteur du Canvas"""

        self.master.move(self.view, 0, self.master.height)
        self.y += self.master.height

        return

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### CREATION DES JOUEURS ###

class player(m.player):
    """Joueur avec les des propriétés et fonctions étendues en lien avec tkinter tk du joueur dans script m"""

    def __init__(self, x = None, y = None):
        """
        In :
          x = None : abscisse possible du joueur
          y = None : ordonnée possible du joueur
        """

        # si aucune donnée n'est fournie sur les coordonnées, script m prend des coordonnées logiques en fonction de sa liste levels_save
        # sinon (peu recommandé), le joueur est défini sur les coordonnées données
        if x == None or y == None:
            m.player.__init__(self)
        else:
            m.player.__init__(self, x, y)

        # le joueur ne prend pas toute une case, il a besoin de quatre coordonnées initiales
        t = self.get_coords()

        # création d'une liste obj_design du module graphics g d'objets can.create propres au joueur
        self.view = g.obj_design(can, - 1, t[0], t[1], t[2], t[3])

        return

    def get_coords(self):
        """Renvoie les coordonnées pour CAN d'un joueur à partir de son x et son y"""
        """
        Out :
          abscisse x1
          ordonnée y1
          abscisse x2
          ordonnée y2
        """
        
        return (self.x * r.rap + r.rap / 4, self.y * r.rap + r.rap / 4, (self.x + 1) * r.rap - r.rap/4, (self.y + 1) * r.rap - r.rap / 4)

    def move(self, event = None):
        """Actualise la position d'un joueur - extension de la fonction initiale"""
        """
        In :
          event = None : objet de tkinter tk lié à un bind avec ses propriétés
        """

        # réinitialisation de la position du joueur avec ses anciennes coordonnées
        t = self.get_coords()
        can.move(self.view, - t[0], - t[1])

        # changement des coordonnées et obtention de possibles éléments concernant les objets bougés stockés dans f
        f = super(player, self).move(event)

        # repositionnement du joueur avec ses nouvelles coordonnées (changées dans f)
        t = self.get_coords()
        can.move(self.view, t[0], t[1])

        # si f n'a changé la position d'une caisse, il contient des '- 1'
        # sinon, il contient les informations concernant les nouvelles coordonnées de la caisse bougée
        if not - 1 in f[1]:
            e = gateV[self.x][self.y]
            # repositionnement en deux étapes (réinitialisation et positionnement) de la caisse
            can.move(e, - self.x * r.rap, - self.y * r.rap)
            can.move(e, f[1][0] * r.rap, f[1][1] * r.rap)
            # changements dans gateV de la caisse
            gateV[f[1][0]][f[1][1]] = e
        
        gateV[self.x][self.y] = self.view

        return

    def move_all(cls, event = None):
        """Actualise la position de tous les joueurs et, parfois, des caisses"""
        """
        In :
          event = None : objet de tkinter tk lié à un bind avec ses propriétés
        """
        # tous les joueurs se déplacent alors avec la même direction, mais le programme respecte un ordre entre chaque joueur qui pose parfois problème lorsque deux sont côte à côte
        # l'ordre basique donne la priorité aux plus à gauche, et parmi ceux sur la même colonne, les plus bas
        # cela se produit donc lorsqu'on essaie d'avancer vers le bas ou la droite
        # le joueur du dessus essaie d'avancer sur celui du dessous mais ne peut pas ; or juste après celui du dessous peut, ce aurait laissé la possibilité de bouger à celui du dessus

        m.save_history()
        m.hist_allowed += 1

        # alors, on commence par récupérer dans quel sens tous les joueurs vont
        c_up = event.keycode == 38
        c_do = event.keycode == 40
        c_ri = event.keycode == 39
        c_le = event.keycode == 37

        tltl = cls.ALL
        l1 = [(tltl[k].x, tltl[k].y, k) for k in range(len(tltl))]
        l1 = sorted(l1)
        l2 = [tltl[k[2]] for k in l1]

        # puis, si ce sens est le bas ou la gauche, on analyse la liste en sens inverse
        if c_do or c_ri:
            ltl = list(reversed(l2))
        else:
            ltl = l2

        # si le niveau n'est pas fini
        if next_level:
            for k in ltl:
                # changement personnel pour chaque joueur de sa position avec l'objet event
                k.move(event)

        return

    move_all = classmethod(move_all)
            
    def new_view(self):
        """Génère la nouvelle valeur de self.view (après, souvent, sa destruction durant actualize())"""
        
        can.delete(self.view)

        # obtention des nouvelles coordonnées et création avec des nouveaux objets dans un obj_design de graphics g
        t = self.get_coords()
        self.view = g.obj_design(can, - 1, t[0], t[1], t[2], t[3])

        return

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### CREATION DU TIMER ###

class clock:
    """Génère un timer"""

    ALL = []

    # si le timer est activé
    activated = True

    def __init__(self, master):
        """
        In :
          master : surface dans laquelle se trouve le timer
        """

        clock.ALL.append(self)

        self.t = time.time()
        self.master = master

        self.view = g.obj_design(self.master, 75, 0, 0, self.master.width, self.master.height)

        return

    def refresh(self):
        """Réinitialise un timer, soit son début et sa représentation"""

        self.t = time.time()
        self.view.refresh_timer()

        return

    def actualize(self):
        """Actualise un timer"""

        # on stocke le temps écoulé
        t = time.time() - self.t
        # on calcule le périmètre du Canvas, qu'on divise par le temps total, puis multiplie par le temps écoulé pour savoir de combien réduire
        l = int((self.master.width + self.master.height) * 2 / r.max_t * t)

        if l < self.master.width:
            self.view.config_timer(0, l)
        
        elif l < self.master.width + self.master.height:
            self.view.config_timer(1, l - self.master.width)
        
        elif l < 2 * self.master.width + self.master.height:
            self.view.config_timer(2, l - self.master.width - self.master.height)
        
        else:
            self.view.config_timer(3, l - 2 * self.master.width - self.master.height)

        return

    def change_able(cls, event = None):
        """Active ou désactive le timer"""
        """
        In :
          event = None : objet de tkinter tk lié à un bind avec ses propriétés
        """

        if next_level:

            cls.activated = not cls.activated

            if cls.activated:
                for k in cls.ALL:
                    k.view = g.obj_design(k.master, 75, 0, 0, k.master.width, k.master.height)
                    #k.master.move(k.view, 0, -r.outscreen)
                    #k.view.y1 -= r.outscreen
                    #k.view.y2 -= r.outscreen
                    k.refresh()

            else:
                for k in cls.ALL:
                    k.master.delete(k.view)
                    #k.master.move(k.view, 0, r.outscreen)
                    #k.view.y1 += r.outscreen
                    #k.view.y2 += r.outscreen

            restart(r_timer = False)

        return

    change_able = classmethod(change_able)

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### CHANGEMENTS SUR LES GRILLES ###

def actualize(actu_gateVC = True):
    """Regénère les grilles"""
    """
    In :
      actu_gateVC = False : détermine si gateVC doit être actualisé
    """
    
    global gate, gateV, gateVC

    # actualisation du Canvas et de ses propriétés
    can.update()
    can.update_size()

    # on essaie de détruire chaque élément du Canvas pour le décharger
    for i in gateV:
        for j in i:
            try:
                can.delete(j)
            except Exception:
                # on ne fait rien s'il y a eu une erreur (normalement l'emplacement était vide)
                pass
    for i in gateVC:
        for j in i:
            try:
                can.delete(j)
            except Exception:
                pass

    # recréation des listes gate, gateV et gateVC et récupération intérieure à la fonction de gateC (tableau pour la position des croix)
    gate = m.gate()
    gateC = m.gateC()
    gateV = [[None for j in i] for i in gate]
    gateVC = [[None for j in i] for i in gate]

    # liste regroupant tous les objets obj_design du Canvas de chaque joueur, afin de les pop un par un plus tard lors de l'affichage
    p_t = [k.view for k in player.ALL]

    # on analyse chaque élément de gate (niveau actuel) pour créer sa représentation dans le Canvas
    for i in range(len(gate)):
        for j in range(len(gate[i])):
            # récupération et stockage dans e de l'élément
            e = gate[i][j]

            # si l'élément est un joueur, on associe son attribut player.view - on fait cela pour le dernier joueur de player.ALL, et poru éviter de créer deux joueurs, on pop l'élément de p_t
            # sinon, on créer un objet obj_design pour l'élément

            if e == - 1:

                gateV[i][j] = p_t.pop(0)

            elif e == 1:

                gateV[i][j] = g.obj_design(can, 1, i * r.rap, j * r.rap, (i+1) * r.rap, (j+1) * r.rap)

            elif e == 3:

                # afin de fusionner les coins si deux murs sont adjacents, on stocke si les éléments à côté sont aussi des murs dans les variables up (up - élément au-dessus), do (down - élément en-dessous), ri (right - élément à droite) et le (left - élément à gauche
                # pour up (up) et le (left), on vérifie ("i-1 > = 0" & "j-1 > = 0") que l'index fourni n'est pas -1 (ce qui renverrait au dernier élément de la liste, or l'analyse se contente des murs conjoints directement)
                # pour do (down) et ri (right), on rejoute un try au cas où le mur analysé se trouve sur un bord (bord bas ou droit), afin d'éviter, lors de l'analyse, un problème d'index (demande d'un index hors de la liste, soit supérieur ou égal à sa longueur)
                up = m.gate()[i][j - 1] == 3 and j - 1 >= 0
                try:
                    do = m.gate()[i][j + 1] == 3
                except Exception:
                    do = False
                try:
                    ri = m.gate()[i + 1][j] == 3
                except Exception:
                    ri = False
                le = m.gate()[i - 1][j] == 3 and i  -1 >= 0

                # avec les données obtenues précédemment (dans up, do, ri et le), on créé des nouvelles variables (voir le commentaire suivant) qui déterminent si un coin doit être rempli ou laissé arrondi
                #(c_ul : condition up-left, c_ur : condition up-right, c_dl : condition down-left, c_dr : condition down-right
                c_ul = up or le
                c_ur = up or ri
                c_dl = do or le
                c_dr = do or ri

                gateV[i][j] = g.obj_design(can, 3, i * r.rap, j * r.rap, (i + 1) * r.rap, (j + 1) * r.rap, c_ul = c_ul, c_ur = c_ur, c_dl = c_dl, c_dr = c_dr)

    # pour chacune des croix encore valides (aucune caisse dessus), on créé sa représentation dans le Canvas avec un obj_design
    for i in range(len(gateC)):
        for j in range(len(gateC[i])):
            if gateC[i][j][1]: # or (not actu_gateVC):
                gateVC[i][j] = g.obj_design(can, 2, i * r.rap, j * r.rap, (i + 1) * r.rap, (j + 1) * r.rap)

    # on recréé l'attribut player.view pour chaque joueur
    for k in player.ALL:
        k.new_view()

    # enfin, on remet au premier plan les boutons et le timer
    for k in new_button.ALL:
        k.refresh_view()
    if actu_gateVC and clock.activated:
        timer.refresh()
    can.lift(timer.view)

    return

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### FONCTION RESTART ###

def restart(event = None, r_timer = True):
    """Fait le niveau actuel recommencer en complément du module"""
    """
    In :
      event = None : objet de tkinter tk lié à un bind avec ses propriétés
    """

    # si le niveau n'est pas fini
    if next_level:

        if r_timer:
            timer.refresh()

        # on détruit chaque représentation de joueur sur le Canvas
        for k in player.ALL:
            can.delete(k.view)

        # script m s'occupe de quelques aspects logiques
        m.restart()

        # on ne sait jamais...
        for k in player.ALL:
            can.delete(k.view)

        # recréation de tous les joueurs, en fonction du nombre présent sur la grille
        cur = m.get_cur()
        levels = m.levels_save
        for i in levels[cur]:
            for j in i:
                if j == - 1:
                    player()

        # on trouve toutes les positions possibles pour les joueurs (tx1 et x1 pour x, tx2 et x2 pour y)

        tx1 = [[k] * levels[cur][k].count(- 1) for k in range(len(levels[cur])) if - 1 in levels[cur][k]]
        tx2 = []
        for i in levels[cur]:
            # t contient tous les indexs des -1 dans la colonne actuelle i
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

        # on change les coordonnées et regénère la représentation de chaque joueur
        for k in range(len(player.ALL)):
            player.ALL[k].repos(x1[k], x2[k])
            player.ALL[k].new_view()
                
        actualize()

    return

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### FONCTION UNDO ###

def undo(event = None):
    """Annule le dernier mouvement"""
    """
    In :
      event = None : objet de tkinter tk lié à un bind avec ses propriétés
    """

    if len(m.history) > 0 and next_level and m.hist_allowed > 0:

        pos = m.undo(prt = 1)

        for k in gateV:
            can.delete(k)

        # on change les coordonnées et regénère la représentation de chaque joueur
        for k in range(len(player.ALL)):
            player.ALL[k].repos(pos[0][k], pos[1][k])
            player.ALL[k].new_view()

        m.undo(prt = 2)

        for k in gateVC:
            can.delete(k)

        actualize(actu_gateVC = False)

        m.undo(prt = 3)

    return

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### FONCTION DE CONTINUITE APRES UN NIVEAU ###

def keep(event = None):
    """Permet de passer d'un niveau à un autre"""
    """
    In :
      event = None : objet de tkinter tk lié à un bind avec ses propriétés
    """

    global next_level

    if not next_level:
        next_level = True

    return

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### EXECUTION PRINCIPALE DU PROGRAMME ###

"""-----------------------------------------------------------------------"""
## initialisation ##

# on récupère le niveau actuel dans script m et on créé les listes pour le Canvas gateV (éléments non superposables) et gateVC (croix)
gate = m.gate()
gateV = [[]]
gateVC = [[]]

# on créé un joueur pour chaque -1 dans le niveau actuel, au cas où le niveau commence avec plusieurs joueurs
for i in range(len(m.levels_save[m.cur])):
    for j in range(len(m.levels_save[m.cur][i])):
        if m.levels_save[m.cur][i][j] == - 1:
            player(x = i, y = j)

# création du bouton restart
new_button(can, 50)
# création du bouton undo
new_button(can, 52)
# création du bouton next
next_b = new_button(can, 51, width = r.rap * 1.5, height = r.rap * 1.5)

# création du timer
timer = clock(can)

actualize()

"""-----------------------------------------------------------------------"""
## début ##

# association de quelques touches à des fonctions

win.bind('<Up>', player.move_all)
win.bind('<Down>', player.move_all)
win.bind('<Right>', player.move_all)
win.bind('<Left>', player.move_all)

win.bind('<r>', restart)
win.bind('<Control-z>', undo)
win.bind('<t>', clock.change_able)

win.bind('<n>', keep)

can.bind('<Button-1>', can.click)
can.bind('<Motion>', can.motion)
can.bind('<Button1-Motion>', can.motion)

# création des variables pour les boucles
end = False
next_level = True
end_between = False

while not end:

    # si la fenêtre est fermée durant l'éxecution du programme, le try empêche les erreurs
    try:
        win.update()
    except Exception:
        end = True
        try:
            win.destroy()
            break
        except Exception:
            break
    try:
        if clock.activated:
            timer.actualize()
    except Exception:
        pass

    if clock.activated and time.time() - timer.t > r.max_t:

        restart()
        timer.refresh()

    # si le niveau actuel est fini
    if m.check_end(want_ins = False):

        # on attend que le joueur valide pour passer au niveau suivant
        
        next_level = False
        next_b.show()

        while not next_level:
            try:
                win.update()
            except Exception:
                end = True
                # un break ne ferait que stopper la boucle actuelle, on a donc besoin d'un deuxième break, activé si celui-ci l'est, avec end_between
                end_between = True
                try:
                    win.destroy()
                except Exception:
                    break
        if end_between:
            break

        next_b.hide()

        # script m s'occupe de quelques points sur la création du nouveau niveau
        m.new_level()

        # on recréé chaque joueur
        cur = m.get_cur()
        levels = m.get_levels()
        for i in levels[cur]:
            for j in i:
                if j == - 1:
                    player()

        # on trouve toutes les positions possibles pour les joueurs (tx1 et x1 pour x, tx2 et x2 pour y)

        tx1 = [[k] * levels[cur][k].count(- 1) for k in range(len(levels[cur])) if - 1 in levels[cur][k]]
        tx2 = []
        for i in levels[cur]:
            # t contient tous les indexs des -1 dans la colonne actuelle i
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

        # on change les coordonnées et regénère la représentation de chaque joueur
        for k in range(len(player.ALL)):
            player.ALL[k].repos(x1[k], x2[k])
            player.ALL[k].new_view()
        
        actualize()
        r.max_t = len(m.levels[m.cur]) * len(m.levels[m.cur][0])

"""-----------------------------------------------------------------------"""
## fin ##

try:
    win.mainloop()
except Exception:
    pass
