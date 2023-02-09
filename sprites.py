import arcade
import json
import os

with open("./conf.json", 'r') as f:
    
    content = json.load(f)
    STAT_ROUTEUR = content["conf"]["routeur"]
    
    STAT_CABLE = content["conf"]["cable"]


# chargement des sprites (pour les charger qu'une fois)
TEXTURES_SPRITES = {}
for type_texture in os.listdir("./assets/sprites/"):
    TEXTURES_SPRITES[type_texture] = []
    for texture in os.listdir(f"./assets/sprites/{type_texture}/"):
        TEXTURES_SPRITES[type_texture].append(arcade.load_texture(f"./assets/sprites/{type_texture}/{texture}"))


class Interface:
    
    def __init__(self, x:int, y:int, nom:str) -> None:
        self.center_x = x
        self.center_y = y
        self.nom = nom
    
    def get_name(self):
        return self.nom
    
    def get_coords(self):
        return (self.center_x, self.center_y)



class Routeur(arcade.Sprite):
    
    def __init__(self, x:int, y:int, w:int, h:int, nom:str, niveau:int) -> None:
        super().__init__()
        
        self.center_x = x
        self.center_y = y
        self.width = w
        self.height = h
        self.nom = nom
        self.niveau = niveau
        
        # si le sprite a deja ete ajouté a la game
        self.in_game = False
        
        # récuperer les stats du routeur
        self.stats = STAT_ROUTEUR
        self.stats_actuel = STAT_ROUTEUR[f"nv{self.niveau}"]
        
        # récupérer les textures (faire une fonction plus tard)
        self.texture_actuel = 0
        self.textures_sprite = TEXTURES_SPRITES["routeur"]
        self.texture = self.textures_sprite[self.texture_actuel]
                
        # créer les interfaces
        self.interfaces = self.gen_interfaces()
        
        # contenu console
        self.contenu_console = [f"Bienvenu dans la console de la machine {self.nom}"]
        
    
    def gen_interfaces(self) -> list:
        """Calcul l'endroit ou doivent se trouver les interfaces"""
        
        nb_interfaces = self.stats_actuel["interfaces"]
        interfaces = []
        
        if nb_interfaces >= 2:
            interfaces.append(Interface(self.center_x, self.center_y + (self.height/2), "eth0"))
            interfaces.append(Interface(self.center_x + self.width, self.center_y + (self.height/2), "eth1"))
        
        if nb_interfaces >= 3:
            interfaces.append(Interface(self.center_x + (self.width/2), self.center_y + self.height, "eth2"))
        
        if nb_interfaces >= 4:
            interfaces.append(Interface(self.center_x + (self.width/2), self.center_y, "eth3"))
        
        return interfaces
            
    
    def level_up(self, n=1):
        self.niveau += n
        self.stats_actuel = STAT_ROUTEUR[self.niveau]
        
        self.interfaces = self.gen_interfaces()

        
    def animer(self):
        self.texture_actuel += 1
        
        if self.texture_actuel >= len(self.textures_sprite):
            self.texture_actuel = 0
        
        self.texture = self.textures_sprite[self.texture_actuel]
    
    def get_interface(self, nom):
        
        for interface in self.interfaces:
            if nom == interface.get_name():
                return interface
    
    def executer(self, commande):
        self.contenu_console.append(f"{self.nom}#{commande}")
        
        # interprétation
        
        self.contenu_console.append("interpretation pas encore activé")
    
    def get_output_lines(self, nb:int, car_par_ligne:int, nb_start=-1):
        """Renvoi les nb ligne aec un maximum de nb_char_par_ligne
        sur chaque ligne, par défaut le fetch commence par la fin"""
        liste_fin = []
        
        i = 0
        nb_lignes = 0
        while nb_lignes < nb and i < len(self.contenu_console):
            
            nb_lignes += 1 + len(self.contenu_console[nb_start - i])//car_par_ligne
            
            if nb_lignes <= nb:
                liste_fin.append(self.contenu_console[nb_start - i])
            
            i += 1
        
        return liste_fin[::-1]
        

class Cable:
    
    def __init__(self, interface1:Interface, interface2:Interface, niveau) -> None:
        
        
        self.niveau = niveau
        self.interface1 = interface1
        self.interface2 = interface2
        
        self.stats = STAT_CABLE
        self.stats_actuel = STAT_CABLE[f"nv{self.niveau}"]
    
    def dessiner(self):
        arcade.draw_line(self.interface1.center_x, self.interface1.center_y,
                        self.interface2.center_x, self.interface2.center_y, (0, 0, 0))
    


class Switch(arcade.Sprite):
    
    def __init__(self, x:int, y:int, w:int, h:int, nom:str, niveau:int) -> None:
        super().__init__()
        
        self.center_x = x
        self.center_y = y
        self.width = w
        self.height = h
        self.nom = nom
        self.niveau = niveau
        
        # si le sprite a deja ete ajouté a la game
        self.in_game = False
