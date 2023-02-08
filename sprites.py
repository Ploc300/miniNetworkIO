import arcade
import json

with open("./conf.json", 'r') as f:
    
    content = json.load(f)
    STAT_ROUTEUR = content["conf"]["routeur"]
    
    STAT_CABLE = content["conf"]["cable"]



class Interface:
    
    def __init__(self, x:int, y:int, nom:str) -> None:
        self.pos_x = x
        self.pos_y = y
        self.nom = nom
    
    def get_name(self):
        return self.nom
    
    def get_coords(self):
        return (self.pos_x, self.pos_y)



class Routeur(arcade.Sprite):
    
    def __init__(self, x:int, y:int, w:int, h:int, nom:str, niveau:int) -> None:
        super().__init__()
        
        self.pos_x = x
        self.pos_y = y
        self.width = w
        self.height = h
        self.nom = nom
        self.niveau = niveau
        
        # récuperer les stats du routeur
        self.stats = STAT_ROUTEUR
        self.stats_actuel = STAT_ROUTEUR[f"nv{self.niveau}"]
        
        # créer les interfaces
        self.interfaces = self.gen_interfaces()
        
        self.sprites = [arcade.load_texture("./assets/sprites/routeur/1.png")]
        self.sprite_actuel = 0
    
    def gen_interfaces(self) -> list:
        """Calcul l'endroit ou doivent se trouver les interfaces"""
        
        nb_interfaces = self.stats_actuel["interfaces"]
        interfaces = []
        
        if nb_interfaces >= 2:
            interfaces.append(Interface(self.pos_x, self.pos_y + (self.height/2), "eth0"))
            interfaces.append(Interface(self.pos_x + self.width, self.pos_y + (self.height/2), "eth1"))
        
        if nb_interfaces >= 3:
            interfaces.append(Interface(self.pos_x + (self.width/2), self.pos_y + self.height, "eth2"))
        
        if nb_interfaces >= 4:
            interfaces.append(Interface(self.pos_x + (self.width/2), self.pos_y, "eth3"))
        
        return interfaces

    def update_animation(self):
        
        self.sprite_actuel += 1
        
        if self.sprite_actuel >= len(self.sprites):
            self.sprite_actuel = 0
        
        return self.sprites[self.sprite_actuel]
            
    
    def level_up(self, n=1):
        self.niveau += n
        self.stats_actuel = STAT_ROUTEUR[self.niveau]
        
        self.interfaces = self.gen_interfaces()

        

class Cables(arcade.Sprite):
    
    def __init__(self, interface1:Interface, interface2:Interface, niveau) -> None:
        super().__init__()
        
        self.niveau = niveau
        self.interface1 = interface1
        self.interface2 = interface2
        
        self.stats = STAT_CABLE
        self.stats_actuel = STAT_CABLE[f"nv{self.niveau}"]
    


class Switch(arcade.Sprite):
    
    def __init__(self, x:int, y:int, w:int, h:int, nom:str, niveau:int) -> None:
        super().__init__()
        
        self.pos_x = x
        self.pos_y = y
        self.width = w
        self.height = h
        self.nom = nom
        self.niveau = niveau