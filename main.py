import arcade

# créer un menu aussi

import os
os.chdir(os.path.dirname(__file__))

class FenetrePrincipale(arcade.Window):
    
    def __init__(self):
        super().__init__(1000, 650, "Jeu reseau", fullscreen=False)
    
    def setup(self):
        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Initialize Scene
        self.scene = arcade.Scene()
    
        

class Menu(arcade.View):
    
    def on_show(self):
        arcade.set_background_color((0, 0, 0))
        
        self.sprite_routeur = arcade.load_texture("./assets/sprites/routeur/1.png")
        
        # midle_x, midle_y, width, height, (r, g, b), nom, text, text_color
        self.buttons = [
            (500, 500, 200, 50, (255, 255, 255), "bouton1", "haha", (0, 0, 0)),
            (500, 400, 200, 50, (255, 255, 255), "bouton2", "haha2", (0, 0, 0)),
        ]
    
    def on_draw(self):
        
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


class Jeu(arcade.View):
    
    def on_show(self):
        arcade.set_background_color((0, 0, 0))
        
        self.sprite_routeur = arcade.load_texture("./assets/sprites/routeur/1.png")
    
    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(500, 500, 50, 50, self.sprite_routeur)
    
    def on_update(self, delta_time: float):
        pass



window = FenetrePrincipale()
menu = Menu()
game = Jeu()

window.show_view(menu)
arcade.run()
