from random import randrange

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""

class r:
    """Ensemble des constantes initiales"""

    # tailles

    rap = 50
    des = 20

    # couleurs

    fill_can      = 'lightgrey' # '#CC7070'
    fill_player   = '#7F2400' # '#5D72CC' # '#728AFF'
    ol_player     = '#661E00' # '#7EB2B2' # '#B2FFFF'
    fill_glass    = 'white'
    ol_glass      = 'black'
    fill_eye      = 'black'
    fill_pack     = 'gold' # '#CC865B' # '#FFAA72'
    ol_pack       = 'orange' # '#CCB55B' # '#FFE572'
    fill_cross    = 'black'
    fill_wall     = 'grey' # '#A55B5B'
    fill_brick    = 'lightgrey' # '#CC7070'
    fill_restart  = 'lightblue'
    ol_loop       = 'black'
    fill_next     = 'orange'
    fill_polynext = 'white'
    fill_undo     = '#FF5959' # 'red'
    ol_z          = 'black'
    fill_timer    = '#E5D75B' # 'lightyellow'

    fill_used_brick = 'darkgreen'

    fill_motion_restart = '#728AFF' # 'blue'
    fill_motion_next    = 'gold'
    fill_motion_undo    = '#AF3E3E' # 'darkred'

    # width

    width = 5

"""---------------------------------------------------------------------------------------------------------------------------------------------------"""

class obj_design(list):
    """Permet la partie design du projet ; éléments d'un objet rentrés dans self, une liste"""

    def __init__(self, can, nb, x1, y1, x2, y2, c_ul=False, c_ur=False, c_dr=False, c_dl=False):

        list.__init__(self)
        self.nb, self.can = nb, can
        self.to_fill = []

        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

        if nb == -1: # personnage
            
            self.extend([
                can.create_oval(          x1-r.des/4, y1-r.des/4,         x2+r.des/4,           y2+r.des/4,         fill=r.fill_player, outline=r.ol_player, width=3), 
                can.create_oval(x1+r.des*0.8-r.des/4, y1+r.des/1.5,       x1+r.des*0.8+r.des/4, y1+r.des/4,         outline=r.ol_glass, width=r.width), 
                can.create_oval(x2-r.des*0.8-r.des/4, y1+r.des/1.5,       x2-r.des*0.8+r.des/4, y1+r.des/4,         outline=r.ol_glass, width=r.width), 
                can.create_rectangle(   x1+r.des*0.8, y1+r.des/1.5,       x2-r.des*0.8,         y1+r.des/4,         outline=r.ol_glass, width=r.width), 
                can.create_oval(x1+r.des*0.8-r.des/4, y1+r.des/1.5,       x1+r.des*0.8+r.des/4, y1+r.des/4,         fill=r.fill_glass, width=0), 
                can.create_oval(x2-r.des*0.8-r.des/4, y1+r.des/1.5,       x2-r.des*0.8+r.des/4, y1+r.des/4,         fill=r.fill_glass, width=0), 
                can.create_rectangle(   x1+r.des*0.8, y1+r.des/1.5,       x2-r.des*0.8,         y1+r.des/4,         fill=r.fill_glass, width=0), 
                can.create_oval(    x1+r.des*0.8+0.3, y1+r.des*11/24-0.4, x1+r.des*0.8+0.3,     y1+r.des*11/24-0.3, fill=r.fill_eye, width=3), 
                can.create_oval(        x2-r.des*0.8, y1+r.des*11/24-0.4, x2-r.des*0.8,         y1+r.des*11/24-0.3, fill=r.fill_eye, width=3)
                ])

        elif nb == 1: # caisse
            
            self.extend([
                can.create_rectangle(       x1+r.des/3, y1+r.des/3,       x2-r.des/3,           y2-r.des/3,         fill=r.fill_pack, outline=r.ol_pack, width=r.width), 
                can.create_line(            x1+r.des/3, (y1+y2)/2,        x2-r.des/3,           (y1+y2)/2,          fill=r.ol_pack, width=r.width), 
                can.create_line(             (x1+x2)/2, y1+r.des/3,       (x1+x2)/2,            y2-r.des/3,         fill=r.ol_pack, width=r.width)
                ])

        elif nb == 2: # croix
            
            self.extend([
                can.create_line(            x1+r.rap/3, y1+r.rap/3,       x2-r.rap/3,           y2-r.rap/3,         fill=r.fill_cross, width=r.width), 
                can.create_line(            x2-r.rap/3, y1+r.rap/3,       x1+r.rap/3,           y2-r.rap/3,         fill=r.fill_cross, width=r.width)
                ])

        elif nb == 3: # mur
            
            if c_ul:
                self.extend([
                    can.create_rectangle(           x1, y1,               x1+r.des,             y1+r.des,           fill=r.fill_wall, width=0)
                    ])
            if c_ur:
                self.extend([
                    can.create_rectangle(           x2, y1,               x2-r.des,             y1+r.des,           fill=r.fill_wall, width=0)
                    ])
            if c_dl:
                self.extend([
                    can.create_rectangle(           x1, y2,               x1+r.des,             y2-r.des,           fill=r.fill_wall, width=0)
                    ])
            if c_dr:
                self.extend([
                    can.create_rectangle(           x2, y2,               x2-r.des,             y2-r.des,           fill=r.fill_wall, width=0)
                    ])
            
            self.extend([
                
                can.create_rectangle(         x1+r.des, y1,               x2-r.des,             y2,                 fill=r.fill_wall, width=0), 
                can.create_rectangle(               x1, y1+r.des,         x2,                   y2-r.des,           fill=r.fill_wall, width=0), 
                can.create_oval(                    x1, y1,               x1+r.des*2,           y1+r.des*2,         fill=r.fill_wall, width=0), 
                can.create_oval(                    x2, y1,               x2-r.des*2,           y1+r.des*2,         fill=r.fill_wall, width=0), 
                can.create_oval(                    x1, y2,               x1+r.des*2,           y2-r.des*2,         fill=r.fill_wall, width=0), 
                can.create_oval(                    x2, y2,               x2-r.des*2,           y2-r.des*2,         fill=r.fill_wall, width=0), 
                
                can.create_line(                    x1, y1+r.rap/4,       x2,                   y1+r.rap/4,         fill=r.fill_brick, width=r.width), 
                can.create_line(                    x1, y1+r.rap/2,       x2,                   y2-r.rap/2,         fill=r.fill_brick, width=r.width), 
                can.create_line(                    x1, y2-r.rap/4,       x2,                   y2-r.rap/4,         fill=r.fill_brick, width=r.width), 
                
                can.create_line(            x1+r.rap/3, y1,               x1+r.rap/3,           y1+r.rap/4,         fill=r.fill_brick, width=r.width), 
                can.create_line(          x1+r.rap/1.5, y1,               x1+r.rap/1.5,         y1+r.rap/4,         fill=r.fill_brick, width=r.width), 
                
                can.create_line(            x1+r.rap/6, y1+r.rap/4,       x1+r.rap/6,           y1+r.rap/2,         fill=r.fill_brick, width=r.width), 
                can.create_line(            x2-r.rap/6, y1+r.rap/4,       x2-r.rap/6,           y1+r.rap/2,         fill=r.fill_brick, width=r.width), 
                
                can.create_line(            x1+r.rap/3, y2-r.rap/2,       x1+r.rap/3,           y2-r.rap/4,         fill=r.fill_brick, width=r.width), 
                can.create_line(          x1+r.rap/1.5, y2-r.rap/2,       x1+r.rap/1.5,         y2-r.rap/4,         fill=r.fill_brick, width=r.width), 

                can.create_line(            x1+r.rap/6, y2-r.rap/4,       x1+r.rap/6,           y2,                 fill=r.fill_brick, width=r.width), 
                can.create_line(            x2-r.rap/6, y2-r.rap/4,       x2-r.rap/6,           y2,                 fill=r.fill_brick, width=r.width)

                ])
            
            if c_ul or c_ur:
                self.extend([
                    can.create_line(                x1, y1,               x2,                   y1,                 fill=r.fill_brick, width=r.width)
                    ])
            if c_dl or c_dr:
                self.extend([
                    can.create_line(                x1, y2,               x2,                   y2,                 fill=r.fill_brick, width=r.width)
                    ])

        elif nb == 50: # bouton restart

            poly_points = [((x1+x2+r.des/2)/2, y1+r.des/4), ((x1+x2+r.des/2)/2, y1+r.des*0.75), ((x1+x2-r.des/2)/2, y1+r.des/2)]
            
            self.extend([
                can.create_rectangle(         x1+r.des, y1,               x2-r.des,             y2,                 fill=r.fill_restart, width=0), 
                can.create_rectangle(               x1, y1+r.des,         x2,                   y2-r.des,           fill=r.fill_restart, width=0), 
                can.create_oval(                    x1, y1,               x1+r.des*2,           y1+r.des*2,         fill=r.fill_restart, width=0), 
                can.create_oval(                    x2, y1,               x2-r.des*2,           y1+r.des*2,         fill=r.fill_restart, width=0), 
                can.create_oval(                    x1, y2,               x1+r.des*2,           y2-r.des*2,         fill=r.fill_restart, width=0), 
                can.create_oval(                    x2, y2,               x2-r.des*2,           y2-r.des*2,         fill=r.fill_restart, width=0), 
                can.create_oval(            x1+r.des/2, y1+r.des/2,       x2-r.des/2,           y2-r.des/2,         outline=r.ol_loop, width=r.width), 
                can.create_rectangle(     x1+r.des/2.5, y1+r.des/2.5,     (x1+x2)/2,            (y1+y2)/2,          fill=r.fill_restart, width=0), 
                can.create_polygon(                                                                    poly_points, fill=r.ol_loop, width=r.width)
                ])

            self.to_fill += self[:6]
            self.to_fill.append(self[7])

        elif nb == 51: # bouton next

            poly_points = [(x1+r.des, y1+r.des), (x1+r.des, y2-r.des), (x2-r.des, (y1+y2)/2)]

            self.extend([
                can.create_rectangle(         x1+r.des, y1,               x2-r.des,             y2,                 fill=r.fill_next, width=0), 
                can.create_rectangle(               x1, y1+r.des,         x2,                   y2-r.des,           fill=r.fill_next, width=0), 
                can.create_oval(                    x1, y1,               x1+r.des*2,           y1+r.des*2,         fill=r.fill_next, width=0), 
                can.create_oval(                    x2, y1,               x2-r.des*2,           y1+r.des*2,         fill=r.fill_next, width=0), 
                can.create_oval(                    x1, y2,               x1+r.des*2,           y2-r.des*2,         fill=r.fill_next, width=0), 
                can.create_oval(                    x2, y2,               x2-r.des*2,           y2-r.des*2,         fill=r.fill_next, width=0), 
                can.create_polygon(                                                                    poly_points, fill=r.fill_polynext, width=0)
                ])

            self.to_fill += self[:6]

        elif nb == 52: # bouton undo

            self.extend([
                can.create_rectangle(         x1+r.des, y1,               x2-r.des,             y2,                 fill=r.fill_undo, width=0), 
                can.create_rectangle(               x1, y1+r.des,         x2,                   y2-r.des,           fill=r.fill_undo, width=0), 
                can.create_oval(                    x1, y1,               x1+r.des*2,           y1+r.des*2,         fill=r.fill_undo, width=0), 
                can.create_oval(                    x2, y1,               x2-r.des*2,           y1+r.des*2,         fill=r.fill_undo, width=0), 
                can.create_oval(                    x1, y2,               x1+r.des*2,           y2-r.des*2,         fill=r.fill_undo, width=0), 
                can.create_oval(                    x2, y2,               x2-r.des*2,           y2-r.des*2,         fill=r.fill_undo, width=0), 
                can.create_line(          x1+r.des/1.5, y1+r.des/1.5,     x2-r.des/1.5,         y1+r.des/1.5,       fill=r.ol_z, width=r.width), 
                can.create_line(          x1+r.des/1.5, y2-r.des/1.5,     x2-r.des/1.5,         y2-r.des/1.5,       fill=r.ol_z, width=r.width), 
                can.create_line(          x2-r.des/1.5, y1+r.des/1.5,     x1+r.des/1.5,         y2-r.des/1.5,       fill=r.ol_z, width=r.width)
                ])

            self.to_fill += self[:6]

        elif nb == 75: # timer

            self.extend([
                can.create_line(x1, y1, x2, y1, fill=r.fill_timer, width=r.width*2),
                can.create_line(x2, y1, x2, y2, fill=r.fill_timer, width=r.width*2),
                can.create_line(x2, y2, x1, y2, fill=r.fill_timer, width=r.width*2),
                can.create_line(x1, y2, x1, y1, fill=r.fill_timer, width=r.width*2)
                ])

            self.x1 += r.width/2
            self.y1 += r.width/2

        elif nb == 76: # étoile

            self.extend([
                can.create_oval(x1, y1, x2, y2, fill='yellow')
                ])

        return

    def color_motion(self):
        """Change la couleur d'un bouton lorsque la souris passe dessus"""

        fill = {50:r.fill_motion_restart, 51:r.fill_motion_next, 52:r.fill_motion_undo}
        if self.nb in fill:
            for k in self.to_fill:
                self.can.itemconfig(k, fill=fill[self.nb])

        return

    def usual_color(self):
        """Remet la couleur initiale d'un bouton"""

        fill = {50:r.fill_restart, 51:r.fill_next, 52:r.fill_undo}

        if self.nb in fill:
            for k in self.to_fill:
                self.can.itemconfig(k, fill=fill[self.nb])

        return

    def config_timer(self, line_nb, l):
        """Configurer le timer"""
        """
        In :
          line_nb : le numéro de la ligne à configurer
          l       : la longueur à retirer sur la ligne
        """

        if line_nb == 0:
            self.can.coords(self[line_nb], self.x1+l, self.y1, self.x2, self.y1)
        
        elif line_nb == 1:
            self.can.coords(self[line_nb], self.x2, self.y1+l, self.x2, self.y2)

        elif line_nb == 2:
            self.can.coords(self[line_nb], self.x2-l, self.y2, self.x1, self.y2)

        elif line_nb == 3:
            self.can.coords(self[line_nb], self.x1, self.y2-l, self.x1, self.y1)

        return

    def refresh_timer(self):
        """Reset le timer"""

        self.x2, self.y2 = self.can.width, self.can.height

        self.can.coords(self[0], self.x1, self.y1, self.x2, self.y1)
        self.can.coords(self[1], self.x2, self.y1, self.x2, self.y2)
        self.can.coords(self[2], self.x2, self.y2, self.x1, self.y2)
        self.can.coords(self[3], self.x1, self.y2, self.x1, self.y1)

        return
