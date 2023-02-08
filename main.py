import arcade
from sprites import Interface, Routeur, Switch

# créer un menu aussi

import os
os.chdir(os.path.dirname(__file__))

class FenetrePrincipale(arcade.Window):
    
    def __init__(self):
        super().__init__(1000, 650, "Jeu reseau", fullscreen=False)
        
        view_menu = None
        view_game = None
        
        
    
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
        
        self.sprite_routeur = arcade.load_texture("./assets/sprites/routeur/1.png")
        
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
        
        self.sprite_routeur = arcade.load_texture("./assets/sprites/routeur/1.png")
        
        # x, y, w, h, nom, niveau
        self.routeurs = [(500, 500, 50, 50, "coeur de reseau", 1)]
        
        #self.switch
        
        # nom machine 1, nom machine 2, type(0 = droit ou 1=croisé) ? , niveau
        self.cables = []
    
    def on_draw(self):
        self.clear()
        
        arcade.draw_lrwh_rectangle_textured(500, 500, 50, 50, self.sprite_routeur)
    
    def on_update(self, delta_time: float):
        pass
    




window = FenetrePrincipale()

view_menu = MenuJeu(window=window)
view_game = Jeu(window=window)

window.setup([view_menu, view_game])

window.show_view(view_menu)

arcade.run()
