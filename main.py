import arcade

# créer un menu aussi

import os
os.chdir(os.path.dirname(__file__))


# import après le changement de place (pour pas faire planter le texure loader)
from sprites import Interface, Routeur, Switch, Cable

class FenetrePrincipale(arcade.Window):
    
    def __init__(self):
        super().__init__(1000, 650, "Jeu reseau", fullscreen=False)

        view_menu = None
        view_game = None
        view_help = None
        view_settings = None
        

    def setup(self, view_list:list):
        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Initialize Scene
        self.scene = arcade.Scene()
        
        self.view_menu, self.view_game, self.view_help, self.view_settings = view_list
    
    
    
    
        

class MenuJeu(arcade.View):
    
    
    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        
        arcade.set_background_color((255, 255, 255))
        
        # midle_x, midle_y, width, height, (r, g, b), nom, text, text_color
        self.buttons = [
            (window.width/2, window.height/5*4, 200, 50, (255, 0, 0), "bouton1", "Jouer", (0, 0, 0)),
            (window.width/2, window.height/5*3, 200, 50, (255, 0, 0), "bouton2", "Comment Jouer?", (0, 0, 0)),
            (window.width/2, window.height/5*2, 200, 50, (255, 0, 0), "bouton3", "Paramètres", (0, 0, 0)),
            (window.width/2, window.height/5  , 200, 50, (255, 0, 0), "bouton4", "Quitter", (0, 0, 0))
        ]
    
    def on_draw(self):
        self.clear()
        
        # dessiner les boutons
        for x, y, w, h, color, name, text, text_color in self.buttons:
            arcade.draw_rectangle_filled(x, y, w, h, color)
            arcade.draw_text(text, x, y, text_color, anchor_x="center", anchor_y="baseline")
            
    
    def on_update(self, delta_time: float):
        pass
    
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        
        # verifier si les boutons sont appuyés
        for x_but, y_but, w_but, h_but, _, name, _, _ in self.buttons:
            if x_but - (w_but/2) <= x <= x_but + (w_but/2) and y_but - (h_but/2) <= y <= y_but + (h_but/2):
                if button:
                    print(name)
                    self.button_press(name)
    
    def button_press(self, name:str) -> None:
        match name:
            case "bouton1":
                self.window.show_view(self.window.view_game)
            case "bouton2":
                self.window.show_view(self.window.view_help)
            case "bouton3":
                self.window.show_view(self.window.view_settings)
            case "bouton4":
                self.window.close()

class Help(arcade.View):
    
    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        
        arcade.set_background_color((255, 255, 255))
        
        # midle_x, midle_y, width, height, (r, g, b), nom, text, text_color
        self.buttons = [
            (window.width/2, window.height/5  , 200, 50, (255, 0, 0), "bouton1", "Retour", (0, 0, 0))
        ]

    def on_draw(self):
        self.clear()

        # dessiner les boutons
        for x, y, w, h, color, name, text, text_color in self.buttons:
            arcade.draw_rectangle_filled(x, y, w, h, color)
            arcade.draw_text(text, x, y, text_color, anchor_x="center", anchor_y="baseline")

    def on_update(self, delta_time: float):
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
            
        # verifier si les boutons sont appuyés
        for x_but, y_but, w_but, h_but, _, name, _, _ in self.buttons:
            if x_but - (w_but/2) <= x <= x_but + (w_but/2) and y_but - (h_but/2) <= y <= y_but + (h_but/2):
                if button:
                    print(name)
                    self.button_press(name)

    def button_press(self, name:str) -> None:
        match name:
            case "bouton1":
                self.window.show_view(self.window.view_menu)


class Settings(arcade.View):

    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        
        arcade.set_background_color((255, 255, 255))
        
        # midle_x, midle_y, width, height, (r, g, b), nom, text, text_color
        self.buttons = [
            (window.width/2, window.height/5  , 200, 50, (255, 0, 0), "bouton1", "Retour", (0, 0, 0))
        ]

    def on_draw(self):
        self.clear()

        # dessiner les boutons
        for x, y, w, h, color, name, text, text_color in self.buttons:
            arcade.draw_rectangle_filled(x, y, w, h, color)
            arcade.draw_text(text, x, y, text_color, anchor_x="center", anchor_y="baseline")

    def on_update(self, delta_time: float):
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
            
        # verifier si les boutons sont appuyés
        for x_but, y_but, w_but, h_but, _, name, _, _ in self.buttons:
            if x_but - (w_but/2) <= x <= x_but + (w_but/2) and y_but - (h_but/2) <= y <= y_but + (h_but/2):
                if button:
                    print(name)
                    self.button_press(name)

    def button_press(self, name:str) -> None:
        match name:
            case "bouton1":
                self.window.show_view(self.window.view_menu)



class Jeu(arcade.View):
    
    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        
        arcade.set_background_color((255, 255, 255))
        
        # machine qui est atuelement selectionné
        self.actuelement_selectionne = None
        
        # cooldown entre chaque anim
        self.animation_cooldown = 30
        
        # x, y, w, h, nom, niveau
        self.routeurs = [Routeur(500, 500, 50, 50, "coeur de reseau", 1),
                        Routeur(200, 200, 50, 50, "R1", 1)
                        ]
        
        
        #self.switch
        self.switchs = []
        
        # nom machine 1, nom machine 2, type(0 = droit ou 1=croisé) ? , niveau
        self.cables = [Cable(self.routeurs[0].get_interface("eth0"), self.routeurs[1].get_interface("eth0"), 1)]
        
        # lance le render des sprites
        self.ajouter_sprites()
    
    def on_draw(self):
        
        # dessiner le stage
        self.clear()
        self.window.camera.use()
        self.window.scene.draw()
        
        # dessiner le carré de paramètres
        arcade.draw_lrtb_rectangle_filled(self.window.width*2/3, self.window.width, self.window.height, 0, (223, 223, 222))
        
        # dessiner le contenu du carré de paramètres
        if self.actuelement_selectionne is not None:
            arcade.draw_text(f"Nom : {self.actuelement_selectionne.nom}", self.window.width*5/6,
                            self.window.height*19/20, (0, 0, 0), anchor_x="center", anchor_y="baseline")
            arcade.draw_text(f"Niveau : {self.actuelement_selectionne.niveau}", self.window.width*5/6,
                            self.window.height*18/20, (0, 0, 0), anchor_x="center", anchor_y="baseline")
            arcade.draw_text(f"Nombre d'interfaces : {self.actuelement_selectionne.stats_actuel['interfaces']}", self.window.width*5/6,
                            self.window.height*17/20, (0, 0, 0), anchor_x="center", anchor_y="baseline")
            arcade.draw_text(f"Vitesse : {self.actuelement_selectionne.stats_actuel['packet_par_s']}", self.window.width*5/6,
                            self.window.height*16/20, (0, 0, 0), anchor_x="center", anchor_y="baseline")
        
        # dessin carré console
        if self.actuelement_selectionne is not None:
            arcade.draw_lrtb_rectangle_filled(self.window.width*2/3, self.window.width, self.window.height/2, 0, (0, 0, 0))
            
        
        # update les sprites
        self.animation_cooldown -= 1
        if self.animation_cooldown <= 0:
            self.update_sprites()
            self.animation_cooldown = 30
            
        # dessiner les noms
        self.dessiner_noms()
        
        # dessiner les cables
        for cable in self.cables:
            cable.dessiner()
            
        
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        
        # gérer si un routeur est cliqué
        
        for routeur in self.routeurs:
            if routeur.collides_with_point((x, y)):
                self.actuelement_selectionne = routeur
        
        
    
    def on_update(self, delta_time: float):
        pass
    
    def ajouter_sprites(self):
        """Fonction qui va ajouter a la scene tout les sprites qui n'y sont pas encore"""
        
        for routeur in self.routeurs:
            if not routeur.in_game:
                routeur.in_game = True
                self.window.scene.add_sprite(routeur.nom, routeur)
    
    
    def update_sprites(self):
        """Fonction qui fait avancer les animations de tout les sprites"""
        
        # update les sprites
        for routeur in self.routeurs:
            routeur.animer()
    
    
    def dessiner_noms(self):
        
        for routeur in self.routeurs:
            arcade.draw_text(routeur.nom, routeur.center_x, routeur.center_y + routeur.height/2 + 10, 
                            (255, 0, 0), anchor_x="center", anchor_y="baseline")
            
        
    




window = FenetrePrincipale()

view_menu = MenuJeu(window=window)
view_game = Jeu(window=window)
view_help = Help(window=window)
view_settings = Settings(window=window)

window.setup([view_menu, view_game, view_help, view_settings])

window.show_view(view_menu)

arcade.run()
