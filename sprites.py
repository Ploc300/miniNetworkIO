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
    
    def __init__(self, x:int, y:int, nom:str, ip=None, masque=None) -> None:
        self.center_x = x
        self.center_y = y
        self.nom = nom
        self.ip = ip
        self.masque = masque
    
    def get_name(self):
        return self.nom
    
    def get_coords(self):
        return (self.center_x, self.center_y)

    def get_ip(self):
        return self.ip
    
    def set_ip(self, ip:str, masque:str):
        self.ip = ip
        self.masque = masque
    
    def get_masque(self):
        return self.masque



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
        
        # si on est en mode config
        self.config = False
        
        # l'interface actuel dans la console
        self.interfaces_actuel = None
        
        # table de routage
        self.table_routage = []
        
    
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
    
    def get_prompt(self):
        mode = ""
        if self.config:
            if self.interfaces_actuel is not None:
                mode = "(config-if)"
            else:
                mode = "(config)"
        
        return f"{self.nom}{mode}#"
    
    def executer(self, commande):
        self.contenu_console.append(self.get_prompt()+commande)
        
        # interprétation
        contenu_commande = commande.split(" ")
        if len(contenu_commande) > 0:
            # si on entre en mode config
            if contenu_commande[0].startswith("conf"):
                
                if len(contenu_commande) > 1:
                    if contenu_commande[1].startswith("t"):
                        self.config = True
                    else:
                        self.contenu_console.append("Argument non valide")
                else:
                    self.contenu_console.append("Il manque un argument")
            
            # si commande int
            elif contenu_commande[0].startswith("int"):
                if len(contenu_commande) > 1:
                    if self.config:
                        interface = self.get_interface(contenu_commande[1])
                        if interface is not None:
                            self.interfaces_actuel = interface
                        else:
                            self.contenu_console.append("L'interface n'est pas valide")
                    else:
                        self.contenu_console.append("Vous devez etre en mode config")
                else:   
                    self.contenu_console.append("Nom de l'interface manquante")
            
            # si commande exit
            elif contenu_commande[0].startswith("exit"):
                if self.interfaces_actuel is not None:
                    self.interfaces_actuel = None
                else:
                    self.config = False
            
            # si commande ip
            elif contenu_commande[0].startswith("ip"):
                if len(contenu_commande) > 1:
                    if self.config:
                        # si commande ip addr
                        if contenu_commande[1].startswith("addr"):
                            if self.interfaces_actuel is not None:
                                if len(contenu_commande) == 4:
                                    # faire la verif de validité
                                    if self.ip_valide(contenu_commande[2], contenu_commande[3]):
                                        self.interfaces_actuel.set_ip(contenu_commande[2], contenu_commande[3])
                                        self.table_routage.append([f"{contenu_commande[2]}/{contenu_commande[3]}", "-", self.interfaces_actuel.get_name()])
                                    
                                else:
                                    self.contenu_console.append("Il faut préciser l'ip et le masque")
                            else:
                                self.contenu_console.append("Aucune interface n'es selectionné")
                        # si commande ip route
                        elif contenu_commande[1].startswith("route"):
                            if len(contenu_commande) == 5:
                                # verifier l'ip
                                if self.ip_valide(contenu_commande[2], contenu_commande[3]):
                                    # si l'ip et le masque sont valides
                                    # on verifie la passerelle
                                    passerelle = self.passerelle_valide(contenu_commande[4])
                                    if passerelle is not None:
                                        self.table_routage.append([f"{contenu_commande[2]}/{contenu_commande[3]}", contenu_commande[4], passerelle[2]])
                                    else:
                                        self.contenu_console.append("La passerelle n'est pas valide")

                                    
                            else:
                                self.contenu_console.append("Pas assez d'arguments (ip, masque et passerelle)")
                        else:
                            self.contenu_console.append("Argument invalide")
                    else:
                        self.contenu_console.append("Il faut etre en mode config")
                else:
                    self.contenu_console.append("Il n'y a pas assez d'argument")
            
            # si c'est une commande en do
            elif contenu_commande[0].startswith("do"):
                if self.config:
                    if len(contenu_commande) > 1:
                        if contenu_commande[1].startswith("sh"):
                            if len(contenu_commande) > 2:
                                if contenu_commande[2].startswith("ip"):
                                    if len(contenu_commande) > 3:
                                        if contenu_commande[3].startswith("int"):
                                            for interface in self.interfaces:
                                                self.contenu_console.append(f"{interface.get_name()}:{interface.get_ip()}/{interface.get_masque()}")
                                        elif contenu_commande[3].startswith("route"):
                                            for route in self.table_routage:
                                                self.contenu_console.append("   ".join(route))
                                        else:
                                            self.contenu_console.append("Argument inconnu")
                                    else:
                                        self.contenu_console.append("Il n'y a pas assez d'argument")
                                else:
                                    self.contenu_console.append("Argument inconnu")
                            else:
                                self.contenu_console.append("Il n'y a pas assez d'argument")
                        else:
                            self.contenu_console.append("Argument inconnu")
                    else:
                        self.contenu_console.append("Il n'y a pas assez d'argument")
                else:
                    self.contenu_console.append("Il ne faut pas utiliser do en dehors du mode config")
            
            
            elif contenu_commande[0].startswith("sh"):
                if not self.config:
                    if len(contenu_commande) > 1:
                        if contenu_commande[1].startswith("ip"):
                            if len(contenu_commande) > 2:
                                if contenu_commande[2].startswith("int"):
                                    for interface in self.interfaces:
                                        self.contenu_console.append(f"{interface.get_name()}:{interface.get_ip()}/{interface.get_masque()}")
                                elif contenu_commande[2].startswith("route"):
                                    for route in self.table_routage:
                                        self.contenu_console.append("   ".join(route))
                                else:
                                    self.contenu_console.append("Argument inconnu")
                            else:
                                self.contenu_console.append("Il n'y a pas assez d'argument")
                        else:
                            self.contenu_console.append("Argument inconnu")
                    else:
                        self.contenu_console.append("Il n'y a pas assez d'argument")
                else:
                    self.contenu_console.append("Il faut utiliser do devant les comande show en mode config")
                    
                    
            # si la commande n'est pas comprise
            else:
                self.contenu_console.append("La commande n'a pas été comprise")
    
    def ip_valide(self, ip, masque):
        ip_splitted = ip.split(".")
        masque_splited = masque.split(".")
        
        ip_valide = True
        masque_valide = True
        # verifier l'ip
        if len(ip_splitted) == 4:
            for p in ip_splitted:
                if not 0 <= int(p) <= 255:
                    ip_valide = False
        else:
            ip_valide = False
            self.contenu_console.append("L'ip n'est pas valide, exemple d'ip : 10.0.0.1")
            
        
        if ip_valide:
            # verifier le massque    
            if len(masque_splited) == 4:
                for p in masque_splited:
                    if not 0 <= int(p) <= 255:
                        masque_valide = False
            else:
                masque_valide = False
                self.contenu_console.append("Le masque n'est pas valide, exemple d'ip : 255.0.0.0")
        else:
            self.contenu_console.append("Les nombres de l'ip doivent etre compris entre 0 et 255")
        
        if not masque_valide:
            self.contenu_console.append("Les nombres du masque doivent etre compris entre 0 et 255")

        masque_binaire = ["".join([bin(int(i)).replace("0b", "") for i in masque_splited])]
        
        que_des_zero = False
        for char in masque_binaire:
            if char == "0":
                que_des_zero = True
            if que_des_zero and char == "1":
                masque_valide = False
        
        if not masque_valide:
            self.contenu_console.append("Le maque n'est pas valide")
        
        # verif que le masque englobe tout le réseau
        englobe_reseau = True
        for i in range(len(ip_splitted)):
            if int(ip_splitted[i]) & ~int(masque_splited[i]):
                print(int(ip_splitted[i]) & ~int(masque_splited[i]))
                englobe_reseau = False

        if not englobe_reseau:
            self.contenu_console.append("Le maque n'englobe pas tout le reseau")
            
        
        return masque_valide and ip_valide and englobe_reseau

    def passerelle_valide(self, passerelle):
        # calcule des réseaux a coté
        for res in self.table_routage:
            if res[1] == "-":
                temp_passerelle = [int(val) for val in passerelle.split(".")]
                
                ip, masque = res[0].split("/")
                ip = [int(val) for val in ip.split(".")]
                masque = [int(val) for val in masque.split(".")]
                
                # opération bit a bit de masquage
                for i in range(len(temp_passerelle)):
                    temp_passerelle[i] = temp_passerelle[i] & masque[i]
                
                if temp_passerelle == ip:
                    return res
        
        return None
    
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
