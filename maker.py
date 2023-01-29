### IMPORTATION DES MODULES ###

import tkinter as tk
import graphics as g

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### CREATION DE LA FENETRE ###

win = tk.Tk()
win.title('Sokoban Maker')

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### CREATION DES CONSTANTES ###

class r:
    """Ensemble de constantes"""

    # taille
    
    rap = g.r.rap
    width,height = 13,13

    # couleurs

    fill_can = g.r.fill_can

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### CREATION DU CANVAS ###

class new_can(tk.Canvas):
    """Canvas"""
    
    def __init__(self):

        # création de la grille avec sa width et height
        self.width,self.height = r.width*r.rap,r.height*r.rap
        tk.Canvas.__init__(self,win,width=self.width,height=self.height,bg=r.fill_can)
        self.grid()

        return

    def move(self,obj,x,y):
        """Permet de bouger un objet OBJ_DESIGN dans le Canvas"""
        """
        In :
          obj : ensemble d'objets dans le Canvas à bouger des mêmes coordonnées
          x   : valeur de changement sur l'abscisse de obj
          y   : valeur de changement sur l'ordonnée de obj
        """

        # obj est une liste d'éléments de tk.Canvas.create créée comme obj_design dans graphics g, qu'il faut bouger tous ensemble avec les mêmes valeurs pour garder leur forme
        # on utilise la fonction initiale tk.Canvas.move() qu'on adapte à un objet obj_design de graphics g
        for k in obj:
            super(new_can,self).move(k,x,y)

        return

    def delete(self,obj):
        """Permet de détruire un objet OBJ_DESIGN dans le Canvas"""
        """
        In :
          obj : ensemble d'objets dans le Canvas à détruire
        """

        # obj est une liste d'éléments de tk.Canvas.create créée comme obj_design dans graphics g, qu'il faut bouger tous ensemble avec les mêmes valeurs pour garder leur forme
        # on utilise la fonction initiale tk.Canvas.move() qu'on adapte à un objet obj_design de graphics g
        for k in obj:
            super(new_can,self).delete(k)

can = new_can()

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### FONCTION DES COORDONNEES POUR LE JOUEUR ###

def get_coords(x,y):
        """Renvoie les coordonnées pour CAN d'un joueur"""
        """
        In :
          x : abscisse à adapter
          y : ordonnée à adapter
        Out :
          abscisse x1
          ordonnée y1
          abscisse x2
          ordonnée y2
        """
        
        return (x*r.rap+r.rap/4,y*r.rap+r.rap/4,(x+1)*r.rap-r.rap/4,(y+1)*r.rap-r.rap/4)

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### FONCTION DE CHANGEMENT ET PLACEMENT D'ITEM ###

def place(event=None):
    """Place un émélent en fonction de cur_item"""
    """
    In :
      event=None : objet de tkinter tk lié à un bind avec ses propriétés
    """

    # on stocke la position en abscisse et ordonnée du clique dans x et y
    x,y = event.x//r.rap,event.y//r.rap
    if x >= r.width:
        x = r.width-1
    if y >= r.height:
        y = r.height-1
    # l'élément cliqué est changé par l'item actuel
    gate[x][y] = cur_item

    # destruction de l'élément actuel
    # on utilise un try au cas où l'élément à supprimer n'existe pas (l'emplacement était déjà vide)
    try:
        can.delete(gateV[x][y])
    except Exception:
        pass

    # nx et ny (nouveau x et nouveau y) ont pour valeur la nouvelle position du futur élément (son coin supérieur gauche)
    nx,ny = x*r.rap,y*r.rap
    # on créé la représentation du nouvel élément, en fonction de l'item actuel
    if cur_item == -1:
        t = get_coords(x,y)
        gateV[x][y] = g.obj_design(can,cur_item,t[0],t[1],t[2],t[3])
    elif cur_item == 0:
        # puisqu'on ne doit rien changer ici, on créé simplement une liste vide (il faut que ce soit une liste pour coïncider avec un obj_design de graphics g avec l'éxecution de new_can.move() ou new_can.delete())
        gateV[x][y] = []
    elif cur_item == 1:
        gateV[x][y] = g.obj_design(can,cur_item,nx,ny,nx+r.rap,ny+r.rap)
    elif cur_item == 2:
        gateV[x][y] = g.obj_design(can,cur_item,nx,ny,nx+r.rap,ny+r.rap)
    elif cur_item == 3:
        gateV[x][y] = g.obj_design(can,cur_item,nx,ny,nx+r.rap,ny+r.rap)

    can.update()

    return

def change_item(event=None):
    """Fait l'item actuel changer en fonction de la touche pressée"""
    """
    In :
      event=None : objet de tkinter tk lié à un bind avec ses propriétés
    """

    global cur_item

    # un dictionnaire (item_cor) indique à quoi (-1, 0, 1, 2 ou 3) correspond chaque event.keycode
    
    if event.keycode in item_cor:
        
        cur_item = item_cor[event.keycode]

    return

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""
### PROGRAMME PRINCIPAL ###

"""-----------------------------------------------------------------------"""
## initialisation ##

# création
gate = [[0] * r.height for k in range(r.width)]
gateV = [[None] * r.height for k in range(r.width)]

# cur_item sert à savoir quel est l'élément actuel, item_cor sert à déterminer quelle valeur cur_item doit prendre avec un event.keycode
cur_item = 3
item_cor = {65:-1,90:0,69:1,82:2,84:3}

def stop(event=None):
    """Change END  pour faire finir le programme"""
    """
    In :
      event=None : objet de tkinter tk lié à un bind avec ses propriétés
    """
    
    global end

    end = True

    return

"""-----------------------------------------------------------------------"""
## début ##

end = False

# association de quelques touches
win.bind('<g>',stop)
win.bind('<a>',change_item)
win.bind('<z>',change_item)
win.bind('<e>',change_item)
win.bind('<r>',change_item)
win.bind('<t>',change_item)
can.bind('<Button1-Motion>',place)
can.bind('<Button-1>',place)

while not end:
    # afin d'éviter une erreur si la fenêtre est fermée pendant la création
    try:
        win.update()
    except Exception:
        try:
            win.destroy()
            break
        except Exception:
            break

end = True

# on demande quelle taille conserver de la grille gate
# si ce qui est donné n'est pas valide, on conserve la taille maximale
try:
    h,l = int(input('Hauteur :\n')),int(input('Largeur :\n'))
except Exception:
    h,l = r.height,r.width

# changement de la grille en string et modification de la syntaxe pour une meilleure lisibilité dans lvls
sh = [k[:h] for k in gate[:l]]
t = str(sh).replace(' ','').replace(',[',',\n     [')
print(f'Grille générée :\n     {t}')

try:
    win.mainloop()
except Exception:
    pass
