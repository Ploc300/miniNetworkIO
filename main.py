import arcade

# créer un menu aussi

import os
os.chdir(os.path.dirname(__file__))


# import après le changement de place (pour pas faire planter le texure loader)
from sprites import Interface, Routeur, Switch

class FenetrePrincipale(arcade.Window):
    
    def __init__(self):
        super().__init__(1000, 650, "Jeu reseau", fullscreen=False)
        
        self.view_menu = None
        self.view_game = None
        
        
    
    def setup(self, view_list:list):
        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Initialize Scene
        self.scene = arcade.Scene()
        
        self.view_menu, self.view_game = view_list
    
    
    
    
        

class MenuJeu(arcade.View):
    
    
    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        
        arcade.set_background_color((255, 255, 255))
        
        # midle_x, midle_y, width, height, (r, g, b), nom, text, text_color
        self.buttons = [
            (500, 500, 200, 50, (255, 0, 0), "bouton1", "Jouer", (0, 0, 0)),
            (500, 400, 200, 50, (255, 0, 0), "bouton2", "haha2", (0, 0, 0)),
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
                if button == 1:
                    print(name)
                    self.button_press(name)
    
    def button_press(self, name:str) -> None:
        if name == "bouton1":
            self.window.show_view(self.window.view_game)
            




class Jeu(arcade.View):
    
    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        
        arcade.set_background_color((255, 255, 255))
        
        # cooldown entre chaque anim
        self.animation_cooldown = 30
        
        # x, y, w, h, nom, niveau
        self.routeurs = [Routeur(500, 500, 50, 50, "coeur de reseau", 1),
                        Routeur(200, 200, 50, 50, "coeur de reseau", 1)
                        ]
        
        
        #self.switch
        
        # nom machine 1, nom machine 2, type(0 = droit ou 1=croisé) ? , niveau
        self.cables = []
        
        # lance le render des sprites
        self.ajouter_sprites()
    
    def on_draw(self):
        
        # dessiner le stage
        self.clear()
        self.window.camera.use()
        self.window.scene.draw()
        
        # update les sprites
        self.animation_cooldown -= 1
        if self.animation_cooldown <= 0:
            self.update_sprites()
            self.animation_cooldown = 30
        
        
    
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
        
        for routeur in self.routeurs:
            routeur.animer()
        
    




window = FenetrePrincipale()

view_menu = MenuJeu(window=window)
view_game = Jeu(window=window)

window.setup([view_menu, view_game])

window.show_view(view_menu)

arcade.run()
