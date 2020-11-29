# -*- coding: utf-8 -*-
'''
Questo pacchetto contiene tutte le classi necessarie al gioco.

INDICE:
    
    1) IMPORT
    
    2) COLORI
    
    3) FUNZIONI:
        -> _Wait
        -> _Void
        -> collisionDetection
        
    4) CLASSE GameInit:
        -> __init__
        -> MainLoop
        -> ReLoop
        -> MoveWindow
        -> OBJadd
        -> updateWindow
        -> __str__
        
    5) CLASSE Screen:
        -> __init__
        -> __str__
        
    6) CLASSE Window:
        -> __init__
        -> __str__
        
    7) CLASSE Personaggio:
        -> __init__
        -> __str__
        
    8) CLASSE Oggetto:
        -> __init__
        -> __str__

'''

'''
1) IMPORT
'''
import pygame
import sys
from itertools import chain


'''
2) COLORI
'''
# Possono essere estratti con il comando: GameToolKit.BLACK...
setattr(sys.modules[__name__], "BLACK", (0, 0, 0))
setattr(sys.modules[__name__], "GRAY", (128, 128, 128))
setattr(sys.modules[__name__], "WHITE", (255, 255, 255))
setattr(sys.modules[__name__], "RED", (255, 0, 0))
setattr(sys.modules[__name__], "GREEN", (0, 255, 0))
setattr(sys.modules[__name__], "BLUE", (0, 0, 255))
setattr(sys.modules[__name__], "YELLOW", (255, 255, 0))
setattr(sys.modules[__name__], "MAGENTA", (255, 0, 255))
setattr(sys.modules[__name__], "CYAN", (0, 255, 255))
setattr(sys.modules[__name__], "ORANGE", (255, 128, 0))
setattr(sys.modules[__name__], "DARK_ROSE", (255, 0, 128))
setattr(sys.modules[__name__], "LILAC", (200, 100, 160))
setattr(sys.modules[__name__], "ROSE", (255, 90, 90))
setattr(sys.modules[__name__], "SKIN_ROSE", (255, 130, 130))
setattr(sys.modules[__name__], "GREEN", (128, 255, 0))
setattr(sys.modules[__name__], "PURPLE", (160, 0, 255))
setattr(sys.modules[__name__], "SKY_BLUE", (0, 128, 255))


'''
3) FUNZIONI
'''
# Main Loop di default
def _Wait():
    '''Non fa nulla e non restituisce nessun valore.'''
    pass
# Funzione degli OBJ di default
def _Void(root = None, obj = None):
    '''Restituisce 'root' e 'obj' senza fare nulla.'''
    return root, obj

# Collision detection
def collisionDetection(root, collider, collided):
    xr = collider.x   # posizione in x del collider
    xd = collided.x   # posizione in x del collided
    yr = collider.y   # posizione in y del collider
    yd = collided.y   # posizione in y del collided
    wr = collider.w   # larghezza del collider
    wd = collided.w   # larghezza del collided
    hr = collider.h   # altezza del collider
    hd = collided.h   # alteza del collided
    # plr = collider.pl # penetrabilità laterale del collider
    pld = collided.pl # penetrabilità laterale del collided
    pvr = collider.pv # penetrabilità verticale del collider
    pvd = collided.pv # penetrabilità verticale del collided
    # posizione in x del collider precedente al movimento
    xrOLD = xr - (collider.xchange * collider.xspeed * root.dt)
    # posizione in y del collider precedente al movimento
    yrOLD = yr - (collider.ychange * collider.yspeed * root.dt)
    
    # output
    out = ""
    
    # Verifica la collisione:
    if (xr > xd - wr + pld) and (xr < xd + wd - pld) and (
            yrOLD < yd + hd - pvr) and (yrOLD > yd - hr + pvd):
        if collider.xchange < 0: # il collider viene da destra
            out = out + "1"      # caso 1
        if collider.xchange > 0: # il collider viene da sinistra
            out = out + "2"      # caso 2
    if (xrOLD > xd - wr + pld) and (xrOLD < xd + wd - pld) and (
            yr < yd + hd - pvr) and (yr > yd - hr + pvd):
        if collider.ychange < 0: # il personaggio viene da sotto
            out = out + "3"      # caso 3
        if collider.ychange > 0: # il personaggio viene da sopra
            out = out + "4"      # caso 4
    return out
# casi possibili di 'out':
#    -> "":   non c'è stata collisione
#    -> "1":  collisione da destra
#    -> "2":  collisione da sinistra
#    -> "3":  collisione dal basso
#    -> "4":  collisione dall'alto
#    -> "13": collisione dal basso a destra
#    -> "14": collisione dall'alto a destra
#    -> "23": collisione dal basso a sinistra
#    -> "24": collisione dall'alto a sinistra


'''
4) CLASSE GAMEINIT
'''
# Creo il root che contiene la finestra
# title    -> titolo della finestra
# size     -> tupla che contiene la grandezza della finestra (x, y).
# pos_wd   -> posizione iniziale della finestra, di default pari a (0, 0)
# mainloop -> funzione che contiene i comandi da ripetere a ogni ciclo while.
class GameInit():
    def __init__(self, title = "Default title", screen_size = (1000, 700), 
                 window_size = (1000, 700), pos_wd = (0, 0), mainloop = _Wait):
        pygame.init()
        
        # Crea la schermata
        self.screen = Screen(title, screen_size)
        
        # Fai i controlli della finestra (window deve essere > screen)
        for i in [0, 1]: # -> 0 = X; 1 = Y
            if window_size[i] < screen_size[i]:
                window_size = list(window_size)
                window_size[i] = screen_size[i]
                print("\r\n\r\nWindow non può essere più piccola di Screen.")
                print("Window è stata ridimensionata.\r\n")
        
        # Fai i controlli della posizione della finestra
        for i in [0, 1]: # -> 0 = X; 1 = Y
            if pos_wd[i] > 0:
                pos_wd = list(pos_wd)
                pos_wd[i] = 0
                print("\r\nWindow non può partire da una posizione maggiore" + 
                      "di 0.")
                print("Window è stata riposizionata.\r\n")
        for i in [0, 1]: # -> 0 = X; 1 = Y
            if pos_wd[i] < screen_size[i] - window_size[i]:
                pos_wd = list(pos_wd)
                pos_wd[i] = screen_size[i] - window_size[i]
                print("\r\nWindow non può partire da una posizione minore di" + 
                      " 'grandezza schermo - grandezza finestra'.")
                print("Window è stata riposizionata.\r\n")
        
        # Crea la finestra
        self.window = Window(window_size, (pos_wd))
        
        # Riempi la schermata con la Surface 'window'
        self.screen.set_mode.blit(self.window.surface, self.window.pos)
        
        # Crea l'orologio
        self.clock = pygame.time.Clock()
        
        # Prendi il time frame
        self.dt = self.clock.tick()
        
        # Crea variablile 'run'
        # run = True  -> rimani nel main loop
        # run = False -> esci dal main loop
        self.run = True
        
        # Creo la variabile '_reloop'
        # _reloop = True  -> manda un nuovo main loop
        # _reloop = False -> esci dal main loop
        self._reloop = True # Di default, entra nel main loop
        
        # Crea la variabile che mantiene il mainloop
        self.mainloop = lambda: mainloop()
        
        # Crea un dizionario di oggetti.
        # vuoto di default:
        self.obj = {"personaggio": [], "oggetto": [], "ostacolo": [], 
                    "volante": []}
        
        ##########--- DEBUG ---##########--- DEBUG ---##########
        print(str(self))
    
    # Crea il main loop e lo avvia
    def MainLoop(self):
        while self._reloop == True:
            # Cambia il valore di _reloop in 'False' -> di default non 
            # ricomincia nuovi loop quando esce dal main loop.
            self._reloop = False
            self.run = True
            
            # Incomincia il main loop
            while self.run == True:
                # Scansiono gli input dello user
                for e in pygame.event.get():
                    # Quit
                    if e.type == pygame.QUIT:
                        self.run = False
                    
                    # Pulsante spinto in basso
                    if e.type == pygame.KEYDOWN:
                        # Quit
                        if e.key == pygame.K_q:
                            self.run = False
                        
                        if e.key == pygame.K_RIGHT:
                            self.obj["personaggio"][0].xchange = 1
                        
                        if e.key == pygame.K_LEFT:
                            self.obj["personaggio"][0].xchange = -1
                        
                        if e.key == pygame.K_DOWN:
                            self.obj["personaggio"][0].ychange = 1
                        
                        if e.key == pygame.K_UP:
                            self.obj["personaggio"][0].ychange = -1
                    
                    # Pulsante spinto in alto
                    if e.type == pygame.KEYUP:
                        if e.key == pygame.K_RIGHT or e.key == pygame.K_LEFT:
                            self.obj["personaggio"][0].xchange = 0
                        
                        if e.key == pygame.K_DOWN or e.key == pygame.K_UP:
                            self.obj["personaggio"][0].ychange = 0
                    
                # Take the time
                self.dt = self.clock.tick(60)
                
                # Modifica la posizione del personaggio
                self.obj["personaggio"][0].x += self.obj[
                        "personaggio"][0].xchange * self.obj[
                                "personaggio"][0].xspeed * self.dt
                self.obj["personaggio"][0].y += self.obj[
                        "personaggio"][0].ychange * self.obj[
                                "personaggio"][0].yspeed * self.dt
                
                # Collision con i bordi della window
                if self.obj["personaggio"][0].x > self.window.size[
                        0] - self.obj["personaggio"][0].w:
                    self.obj["personaggio"][0].x = self.window.size[0
                            ] - self.obj["personaggio"][0].w
                if self.obj["personaggio"][0].x < 0:
                    self.obj["personaggio"][0].x = 0
                if self.obj["personaggio"][0].y > self.window.size[1
                           ] - self.obj["personaggio"][0].h:
                    self.obj["personaggio"][0].y = self.window.size[1
                            ] - self.obj["personaggio"][0].h
                if self.obj["personaggio"][0].y < 0:
                    self.obj["personaggio"][0].y = 0
                
                # Avvia il main loop
                self.mainloop()
                pygame.display.update()
        
        # Quado esci dal main loop
        pygame.quit()
    
    # Avvia un nuovo main loop
    def ReLoop(self, mainloop = _Wait):
        # Esce dal main loop
        self.run = False
        
        # Modifica il mainloop con quello nuovo
        self.mainloop = lambda: mainloop()
        
        # Rientra nel nuovo main loop
        self._reloop = True
    
    # Muovi finestra
    def MoveWindow(self, delta_pos):
        # 'delta_pos' -> tupla che contiene lo spostamento in x e y
        
        # Pulisci lo schermo (necessario solo se le dimensioni della 
        # finestra sono più piccole di quello dello schermo)
        # self.screen.set_mode.fill(sys.modules[__name__].GRAY)
        # Aggiorna i valori della posizione della finestra
        self.window.pos[0] += delta_pos[0]
        self.window.pos[1] += delta_pos[1]
        
        # Fai i controlli della posizione della finestra:
        for i in [0, 1]: # -> 0 = X; 1 = Y
            # X/Y > 0
            if self.window.pos[i] > 0:
                self.window.pos[i] = 0
            # X/Y < di tot
            if self.window.pos[i] < self.screen.size[i] - self.window.size[i]:
                self.window.pos[i] = self.screen.size[i] - self.window.size[i]
        
        # Rappresenta la finestra nella nuova posizione
        # self.screen.set_mode.blit(self.window.surface, self.window.pos)
    
    # Aggiung oggetti a .obj
    def OBJadd(self, objType, obj, fun):
        # objType -> stringa che contiene il tipo di object
        # obj     -> l'oggetto da inserire
        
        # Aggiungi funzione all'oggetto
        obj.fun = fun
        # Aggiungi elemento alla lista
        self.obj[objType.lower()] = self.obj[objType.lower()] + [obj]
    
    # Aggiorna la finestra
    def updateWindow(self):
        # Sposta la finestra insieme al personaggio
        dx = [self.obj["personaggio"][0].x - self.screen.size[0] / 2 + 
              self.window.pos[0] + self.obj["personaggio"][0].w / 2]
        dy = [self.obj["personaggio"][0].y - self.screen.size[1] / 2 + 
              self.window.pos[1] + self.obj["personaggio"][0].h / 2]
        
        # Sporta la finestra
        self.MoveWindow((-dx[0], -dy[0]))
        
        # Crea una lista di tutti gli oggetti
        OBJlist = list(chain.from_iterable(self.obj.values()))
        
        # Ordina gli oggetti per y+h (in ordine crescente)
        OBJlist.sort(key = lambda obj: obj.y + obj.h)
        
        # Scansiona gli obj
        for e in OBJlist:
            # Lancia la funzione associata all'obj
            self, e = e.fun(root = self, obj = e)
            
            # Solo se status = True e non si trova in 'volante'
            if e.status and e not in self.obj["volante"]:
                # Rappresenta gli obj nella window
                 self.window.surface.blit(e.image, (e.x, e.y))
        # Scansiona gli obj 'volante'
        for e in OBJlist:
            # Solo se status = True e si trova in 'volante'
            if e.status and e in self.obj["volante"]:
                # Rappresenta gli obj nella window
                 self.window.surface.blit(e.image, (e.x, e.y))

        # Rappresenta la finestra nella nuova posizione
        self.screen.set_mode.blit(self.window.surface, self.window.pos)
    
    # Cosa restituisce quando usi la funzione 'str'
    def __str__(self):
        a = ["<class 'GameToolKit.GameInit object'>:\r\n\r\n" + 
             ".screen   -> {}".format(str(self.screen)) + 
             ".window   -> {}".format(str(self.window)) + 
             ".clock    -> pygame.time.Clock\r\n" + 
             ".dt       -> time frame: {}\r\n".format(str(self.dt)) + 
             ".run      -> logical: {}\r\n".format(self.run) + 
             "._reloop  -> logical: {}\r\n".format(self._reloop) + 
             ".mainloop -> function\r\n" + 
             ".obj      -> dictionary of {}:\r\n".format(len(self.obj)) + 
             "    [personaggio] -> list of {}\r\n".format(len(self.obj["personaggio"])) + 
             "    [oggetto]     -> list of {}\r\n".format(len(self.obj["oggetto"])) + 
             "    [ostacolo]    -> list of {}\r\n".format(len(self.obj["ostacolo"])) + 
             "    [volante]     -> list of {}\r\n".format(len(self.obj["volante"]))]
        return a[0]


'''
5) CLASSE SCREEN
'''
class Screen():
    def __init__(self, title, size):
        self.set_mode = pygame.display.set_mode(size)
        self.set_mode.fill(sys.modules[__name__].GRAY)
        self.size = list(size)
        self.title = pygame.display.set_caption(title)
    
    # Cosa restituisce quando usi la funzione 'str'
    def __str__(self):
        a = ["<class 'GameToolKit.Screen'>:\r\n" + 
             "    .set_mode -> pygame.display.set_mode\r\n" + 
             "    .title    -> pygame.display.set_caption\r\n" + 
             "    .size     -> list of 2:\r\n" + 
             "        [0] width  -> {}\r\n".format(self.size[0]) + 
             "        [1] height -> {}\r\n".format(self.size[1])]
        return a[0]


'''
6) CLASSE WINDOW
'''
class Window():
    def __init__(self, size, pos):
        self.surface = pygame.Surface(size)
        self.size = list(size)
        self.pos = list(pos)
    
    # Cosa restituisce quando usi la funzione 'str'
    def __str__(self):
        a = ["<class 'GameToolKit.Window'>:\r\n" + 
             "    .surface -> pygame.Surface\r\n" + 
             "    .size    -> list of 2:\r\n" + 
             "        [0] width  -> {}\r\n".format(self.size[0]) + 
             "        [1] height -> {}\r\n".format(self.size[1]) + 
             "    .pos     -> list of 2:\r\n" + 
             "        [0] posx -> {}\r\n".format(self.pos[0]) + 
             "        [1] posy -> {}\r\n".format(self.pos[1])]
        return a[0]


'''
7) CLASSE PERSONAGGIO
'''
class Personaggio():
    def __init__(self, path, ritaglio, pos, size, speed, pl = 20, 
                 pv = 40):
        # Inizializza tutti gli attributi dell'oggetto 'Personaggio'
        self.status = True        # True = rappresenta in window
        self.path = path          # path della sprite
        self.chrono = 0           # conta il numero di loop trascorsi
        self.fun = lambda: _Void()# funzione associata al personaggio
        self.ritaglio = list(ritaglio)  # (x, y, w, h) del ritaglio di 'image'
                                        # solo dell'immagine in alto a sinistra.
        self.pl = pl              # penetrabilità laterale (in pixel)
        self.pv = pv              # penetrabilità verticale (in pixel)
        self.w = size[0]          # larghezza
        self.h = size[1]          # altezza
        self.x = pos[0]           # posizione x in window
        self.y = pos[1]           # posizione y in window
        self.xchange = 0          # spostamento lungo x (moltiplica con xspeed)
        self.ychange = 0          # spostamento lungo y (moltiplica con yspeed)
        self.xspeed = speed[0]    # velocità lungo x
        self.yspeed = speed[1]    # velocità lungo y
        
        # Crea l'immagine che viene rappresentata nalla window
        imageAll = pygame.image.load(path)
        
        # Inizializza image_list
        self.image_dict = {"down": [], "left": [], "right": [], "up": []}
        
        row = 0
        # Ritaglia l'immagine
        for i in self.image_dict.keys():
            col_list = []
            for col in range(3):
                w = self.ritaglio[2]
                x = self.ritaglio[0] + w * col
                h = self.ritaglio[3]
                y = self.ritaglio[1] + h * row
                new_image = imageAll.subsurface(x, y, w, h)
                new_image = pygame.transform.scale(new_image, size)
                col_list.append(new_image)
            new_image = imageAll.subsurface(x - w, y, w, h)
            new_image = pygame.transform.scale(new_image, size)
            col_list.append(new_image)
            self.image_dict[i] = col_list # aggiorna il dizionario con la nuova riga
            row += 1 # passa alla prossima riga
        
        # Prendi l'immagine di default
        self.image = self.image_dict["down"][1]  # frontale
        # Ridimensiona l'immagine
        # self.image = pygame.transform.scale(self.image, size)
        self.OLDdirection = "down"
    
    def __str__(self):
        a = ["<class 'GameToolKit.Personaggio'>:\r\n\r\n" + 
             ".status     -> logical: {}\r\n".format(self.status) + 
             ".chrono     -> {}: {}\r\n".format(type(self.chrono), self.chrono) + 
             ".fun        -> funzione\r\n" + 
             ".image      -> pygame.Surface\r\n" + 
             ".image_dict -> dictionary of 4:\r\n" + 
             "    [down]  -> list of 3 pygame.Surface\r\n" + 
             "    [left]  -> list of 3 pygame.Surface\r\n" + 
             "    [right] -> list of 3 pygame.Surface\r\n" + 
             "    [up]    -> list of 3 pygame.Surface\r\n" + 
             '.path       -> {}: "{}"\r\n'.format(type(self.path), self.path) + 
             ".ritaglio   -> list of 4:\r\n" + 
             "    [0] x -> {}\r\n".format(self.ritaglio[0]) + 
             "    [1] y -> {}\r\n".format(self.ritaglio[1]) + 
             "    [2] w -> {}\r\n".format(self.ritaglio[2]) + 
             "    [3] h -> {}\r\n".format(self.ritaglio[3]) + 
             ".x          -> {}: {}\r\n".format(type(self.x), str(self.x)) + 
             ".y          -> {}: {}\r\n".format(type(self.y), str(self.y)) + 
             ".w          -> {}: {}\r\n".format(type(self.w), str(self.w)) + 
             ".h          -> {}: {}\r\n".format(type(self.h), str(self.h)) + 
             ".xchange    -> {}: {}\r\n".format(type(self.xchange), 
                           str(self.xchange)) + 
                           ".ychange  -> {}: {}\r\n".format(type(self.ychange), 
                                         str(self.ychange))]
        b = [".xspeed   -> {}: {}\r\n".format(type(self.xspeed), 
             str(self.xspeed)) + 
            ".yspeed   -> {}: {}\r\n".format(type(self.yspeed), 
                          str(self.yspeed)) + 
             ".pl       -> {}: {}\r\n".format(type(self.pl), str(self.pl)) + 
             ".pv       -> {}: {}\r\n".format(type(self.pv), str(self.pv))]
        return a[0] + b[0]


'''
8) CLASSE OGGETTO
'''
class Oggetto():
    def __init__(self, path, ritaglio, pos, size, tipo, pl = 0, 
                 pv = 0, nFrames = 1):
        # Inizializza tutti gli attributi dell'oggetto 'Oggetto'
        self.status = True        # True = rappresenta in window
        self.collided = False     # True = l'oggetto è stato colpito
        self.path = path          # path della sprite
        self.fun = lambda: _Void()# funzione associata all'oggetto
        self.chrono = 0           # conta il numero di loop trascorsi
        self.type = tipo          # tipo di oggetto (es. coin, arma, ...)
        self.ritaglio = ritaglio  # (x, y, w, h) del ritaglio di 'image'
        self.pl = pl              # penetrabilità laterale (in pixel)
        self.pv = pv              # penetrabilità verticale (in pixel)
        self.w = size[0]          # larghezza
        self.h = size[1]          # altezza
        self.x = pos[0]           # posizione x in window
        self.y = pos[1]           # posizione y in window
        self.image_list = []      # contiene la lista dei frame dell'oggetto
        
        # Crea l'immagine che viene rappresentata nalla window
        self.image = self.cutImage(nFrames)  # contiene l'immagine rappresentata
                                             # in window.
        print(str(self))
    
    # Ritaglia le immagini per l'animazione di oggetti.
    # Crea una lista di immagini.
    def cutImage(self, nFrames):
        # Crea l'immagine che viene rappresentata nalla window
        imageAll = pygame.image.load(self.path)
        
        # Inizializza image_list
        self.image_list = []
        
        for col in range(nFrames):
            w = self.ritaglio[2]
            x = self.ritaglio[0] + w * col
            h = self.ritaglio[3]
            y = self.ritaglio[1]
            # ritaglia l'immagine
            new_image = imageAll.subsurface(x, y, w, h)
            # ridimrnsiona l'immagine
            new_image = pygame.transform.scale(new_image, (self.w, self.h))
            # aggiorna la lista con la nuova immagine
            self.image_list.append(new_image)
        
        # Prendi l'immagine di default
        return self.image_list[0]  # la prima
    
    def __str__(self):
        a = ["<class 'GameToolKit.Oggetto'>:\r\n\r\n" + 
             ".status     -> logical: {}\r\n".format(self.status) + 
             ".collided   -> logical: {}\r\n".format(self.collided) + 
             '.type       -> "{}"\r\n'.format(self.type) + 
             ".chrono     -> {}: {}\r\n".format(type(self.chrono), self.chrono) + 
             ".fun        -> funzione: {}\r\n".format(str(self.fun)) + 
             ".image      -> pygame.Surface\r\n" + 
             ".image_list -> list of {} pygame.Surface\r\n".format(len(self.image_list)) + 
             '.path       -> {}: "{}"\r\n'.format(type(self.path), self.path) + 
             ".ritaglio   -> list of 4:\r\n" + 
             "    [0] x -> {}\r\n".format(self.ritaglio[0]) + 
             "    [1] y -> {}\r\n".format(self.ritaglio[1]) + 
             "    [2] w -> {}\r\n".format(self.ritaglio[2]) + 
             "    [3] h -> {}\r\n".format(self.ritaglio[3]) + 
             ".x          -> {}: {}\r\n".format(type(self.x), str(self.x)) + 
             ".y          -> {}: {}\r\n".format(type(self.y), str(self.y)) + 
             ".w          -> {}: {}\r\n".format(type(self.w), str(self.w)) + 
             ".h          -> {}: {}\r\n".format(type(self.h), str(self.h)) + 
             ".pl         -> {}: {}\r\n".format(type(self.pl), str(self.pl)) + 
             ".pv         -> {}: {}\r\n".format(type(self.pv), str(self.pv))]
        return a[0]
