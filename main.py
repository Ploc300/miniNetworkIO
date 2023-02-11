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
            (window.width/2, window.height/8  , 200, 50, (255, 0, 0), "bouton1", "Retour", (0, 0, 0))
        ]

        # midle_x, midle_y, width, height, text, text_color, size, anchor_x, anchor_y
        self.textes = [
            (window.width/4,   window.height/5*4, window.width/2.5, window.height/4, "Zone 1", (0, 0, 0), 20, "center", "baseline"),
            (window.width/4*3, window.height/5*4, window.width/2.5, window.height/4, "Zone 2", (0, 0, 0), 20, "center", "baseline"),
            (window.width/4,   window.height/5*2, window.width/2.5, window.height/4, "Zone 3", (0, 0, 0), 20, "center", "baseline"),
            (window.width/4*3, window.height/5*2, window.width/2.5, window.height/4, "Zone 4", (0, 0, 0), 20, "center", "baseline"),
        ]

    def on_draw(self):
        self.clear()

        # dessiner les boutons
        for x, y, w, h, color, name, text, text_color in self.buttons:
            arcade.draw_rectangle_filled(x, y, w, h, color)
            arcade.draw_text(text, x, y, text_color, anchor_x="center", anchor_y="baseline")

        # dessiner les textes
        for x, y, w, h, text, text_color, size, anchor_x, anchor_y in self.textes:
            arcade.draw_rectangle_filled(x, y, w, h, color)
            arcade.draw_text(text, x, y, text_color, size, anchor_x=anchor_x, anchor_y=anchor_y)

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
            (window.width/2, window.height/5  , 200, 50, (255, 0, 0), "bouton1", "Retour", (0, 0, 0)),
            (window.width/2, window.height/5*2, 200, 50, (255, 0, 0), "bouton2", "Langue", (0, 0, 0)),
            (window.width/2, window.height/5*3, 200, 50, (255, 0, 0), "bouton3", "Volume", (0, 0, 0)),
            (window.width/2, window.height/5*4, 200, 50, (255, 0, 0), "bouton4", f"light_mode mode" , (0, 0, 0))
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
            case "bouton2":
                # changer la langue
                print("changement de langue a implementer")
            case "bouton3":
                # changer le volume
                print("changement de volume a implementer")
            case "bouton4":
                # changer dark/light mode
                print("changement de dark/light mode a implementer")




class Jeu(arcade.View):
    
    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        
        arcade.set_background_color((255, 255, 255))
        
        # x, y, w, h, nom, niveau
        self.routeurs = [Routeur(500, 500, 50, 50, "coeur de reseau", 1)]
        
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
view_help = Help(window=window)
view_settings = Settings(window=window)

window.setup([view_menu, view_game, view_help, view_settings])

window.show_view(view_menu)

arcade.run()
