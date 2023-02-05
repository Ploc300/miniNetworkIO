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
    
        




class Jeu(arcade.View):
    
    def on_show(self):
        arcade.set_background_color((0, 0, 0))
        
        self.sprite_routeur = arcade.load_texture("./assets/sprites/routeur/1.png")
    
    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(500, 500, 50, 50, self.sprite_routeur)
    
    def on_update(self, delta_time: float):
        pass



window = FenetrePrincipale()
game = Jeu()

window.show_view(game)
arcade.run()