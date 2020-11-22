# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:45:18 2020

@author: mattc
"""

'''
Questo pacchetto contiene tutte le classi necessarie al gioco.
'''

import pygame
import sys

'''
COLORI
'''
# possono essere estratti con il comando: GameToolKit.WHITE
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

# Main Loop di default
def _Wait():
    pass
def nulla(root = None, obj = None):
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
OGGETTO GAME INIT
'''
# Creo il root che contiene la finestra
# title    -> titolo della finestra
# size     -> tupla che contiene la grandezza della finestra (x, y).
# pos_wd   -> posizione iniziale della finestra, di default pari a (0, 0)
# mainloop -> funzione che contiene i comandi da ripetere a ogni ciclo while.
class GameInit():
    def __init__(self, title = "Default title", screen_size = (800, 600), 
                 window_size = (800, 600), pos_wd = 
                 (0, 0), mainloop = _Wait):
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
        self.obj = {"personaggio": [], "oggetto": [], "ostacolo": []}
        
        ##########--- DEBUG ---##########--- DEBUG ---##########
#        print(str(self))
    
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
        
        # Collisione con gli oggetti
#        self.OBJcollision()
        
        # Collisione con ostacoli
#        for e in self.obj["ostacolo"]:
#            out = collisionDetection(self, self.obj["personaggio"][0], e)
#            if len(out) > 0:   # c'è stata collisione
#                e.collided = True
#                done = False
#                if "1" in out: # collisione da destra
#                    self.obj["personaggio"][0].x = e.x + e.w - e.pl
#                    done = True
#                if "2" in out: # collisione da sinistra
#                    self.obj["personaggio"][0].x = (e.x - 
#                            self.obj["personaggio"][0].w + e.pl)
#                    done = True
#                if ("3" in out) and (not done): # collisione dal basso
#                    self.obj["personaggio"][0].y = (e.y + e.h -  
#                            self.obj["personaggio"][0].pv)
#                if ("4" in out) and (not done): # collisione dali'alto
#                    self.obj["personaggio"][0].y = (e.y - 
#                            self.obj["personaggio"][0].h + e.pv)
#            else:  # non c'è stata collisione
#                e.collided = False
        
        # Scansiona gli obj
        OBJkey = [x for x in self.obj.keys() if x not in ["personaggio"]]
        for o in OBJkey:
            for e in self.obj[o]:
                # Lancia la funzione associata all'obj
                self, e = e.fun(root = self, obj = e)
#                print(str(e))
                # Solo se status = True e che si trovano in alto
                if e.status and (e.y + e.h < self.obj["personaggio"][0].y + 
                                 self.obj["personaggio"][0].h):
                    # Rappresenta gli obj nella window
                     self.window.surface.blit(e.image, (e.x, e.y))
                
        # Rappresenta il personaggio
        # Lancia la funzione associata all'obj
        self, self.obj["personaggio"][0] = self.obj["personaggio"][0].fun(
                root = self, obj = self.obj["personaggio"][0])
        self.window.surface.blit(self.obj["personaggio"][0].image, (
                self.obj["personaggio"][0].x, self.obj["personaggio"][0].y))
        
        # Rappresnta quello che sta davanti al personaggio
        for o in OBJkey:
            for e in self.obj[o]:
                # Lancia la funzione associata all'obj
                self, e = e.fun(root = self, obj = e)
                
                # Solo se status = True e che si trovano in basso
                if e.status and (e.y + e.h >= self.obj["personaggio"][0].y + 
                                 self.obj["personaggio"][0].h):
                     self.window.surface.blit(e.image, (e.x, e.y))
        
        # Rappresenta la finestra nella nuova posizione
        self.screen.set_mode.blit(self.window.surface, self.window.pos)
    
    # Collisione con gli oggetti
    def OBJcollision(self):
        x = self.obj["personaggio"][0].x
        y = self.obj["personaggio"][0].y
        w = self.obj["personaggio"][0].w
        h = self.obj["personaggio"][0].h
        pl = self.obj["personaggio"][0].pl
        pv = self.obj["personaggio"][0].pv
        
        # Verifica la collisione
        for e in self.obj["oggetto"]: # Scansiona tutti gli oggetti
            if e.status:              # Considera solo quelli con status = True
                if x + w - pl >= e.x and x <= e.x + e.w - pl:
                    if y + h - e.pv >= e.y and y <= e.y + e.h - pv:
                        e.status = False
    
    # Cosa restituisce quando usi la funzione 'str'
    def __str__(self):
        a = ["<class 'GameToolKit.GameInit object'>:\r\n\r\n" + 
             ".screen   -> {}".format(str(self.screen)) + 
             ".window   -> {}".format(str(self.window)) + 
             "    .pos     -> list of 2: posx = {}; posy = {}\r\n".format(
                     self.window.pos[0], self.window.pos[1])]
        b = [".clock    -> pygame.time.Clock\r\n" + 
             ".dt       -> time frame: {}\r\n".format(str(self.dt)) + 
             ".run      -> logical: {}\r\n".format(self.run) + 
             "._reloop  -> logical: {}\r\n".format(self._reloop) + 
             ".mainloop -> function\r\n" + 
             ".obj      -> dictionary of {}\r\n".format(len(self.obj))]
        return a[0] + b[0]

'''
OGGETTO SCREEN
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
             "    .size     -> list of 2: width = {}; height = {}\r\n".format(
                     self.size[0], self.size[1]) + 
                     "    .title    -> pygame.display.set_caption\r\n"]
        return a[0]

'''
OGGETTO WINDOW
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
             "    .size    -> list of 2: width = {}; height = {}\r\n".format(
                     self.size[0], self.size[1])]
        return a[0]

'''
OBJ -> PERSONAGGIO
'''
class Personaggio():
    def __init__(self, path, ritaglio, pos, size, speed, pl = 20, 
                 pv = 40):
        # Inizializza tutti gli attributi dell'oggetto 'Personaggio'
        self.status = True        # True = rappresenta in window
        self.path = path          # path della sprite
        self.chrono = 0           # conta il numero di loop trascorsi
        self.fun = lambda: nulla()# funzione associata al personaggio
        self.ritaglio = ritaglio  # (x, y, w, h) del ritaglio di 'image'
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
        self.image = pygame.image.load(path)
        
        #Ritaglia l'immagine
        self.image = self.image.subsurface(ritaglio)
        
        # Ridimensiona l'immagine
        self.image = pygame.transform.scale(self.image, size)
    
    def __str__(self):
        a = ["<class 'GameToolKit.Personaggio'>:\r\n\r\n" + 
             ".status   -> logical: {}\r\n".format(self.status) + 
             ".image    -> pygame.Surface\r\n" +
             '.path     -> {}: "{}"\r\n'.format(type(self.path), self.path) + 
             ".chrono   -> {}: {}\r\n".format(type(self.chrono), self.chrono) + 
             ".fun      -> funzione\r\n" + 
             ".ritaglio -> list of 4:\r\n" + 
             "    [0] x -> {}\r\n".format(self.ritaglio[0]) + 
             "    [1] y -> {}\r\n".format(self.ritaglio[1]) + 
             "    [2] w -> {}\r\n".format(self.ritaglio[2]) + 
             "    [3] h -> {}\r\n".format(self.ritaglio[3]) + 
             ".x        -> {}: {}\r\n".format(type(self.x), str(self.x)) + 
             ".y        -> {}: {}\r\n".format(type(self.y), str(self.y)) + 
             ".w        -> {}: {}\r\n".format(type(self.w), str(self.w)) + 
             ".h        -> {}: {}\r\n".format(type(self.h), str(self.h)) + 
             ".xchange  -> {}: {}\r\n".format(type(self.xchange), 
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
OBJ -> OGGETTO
'''
class Oggetto():
    def __init__(self, path, ritaglio, pos, size, tipo, pl = 0, 
                 pv = 0):
        # Inizializza tutti gli attributi dell'oggetto 'Oggetto'
        self.status = True        # True = rappresenta in window
        self.collided = False     # True = l'oggetto è stato colpito
        self.path = path          # path della sprite
        self.fun = lambda: nulla()# funzione associata all'oggetto
        self.chrono = 0           # conta il numero di loop trascorsi
        self.type = tipo          # tipo di oggetto (es. coin, arma, ...)
        self.ritaglio = ritaglio  # (x, y, w, h) del ritaglio di 'image'
        self.pl = pl              # penetrabilità laterale (in pixel)
        self.pv = pv              # penetrabilità verticale (in pixel)
        self.w = size[0]          # larghezza
        self.h = size[1]          # altezza
        self.x = pos[0]           # posizione x in window
        self.y = pos[1]           # posizione y in window
        
        # Crea l'immagine che viene rappresentata nalla window
        self.image = pygame.image.load(path)
        
        #Ritaglia l'immagine
        self.image = self.image.subsurface(ritaglio)
        
        # Ridimensiona l'immagine
        self.image = pygame.transform.scale(self.image, size)
    
    def __str__(self):
        a = ["<class 'GameToolKit.Oggetto'>:\r\n\r\n" + 
             ".status   -> logical: {}\r\n".format(self.status) + 
             ".collided -> logical: {}\r\n".format(self.collided) + 
             '.type     -> "{}"\r\n'.format(self.type) + 
             ".image    -> pygame.Surface\r\n" +
             '.path     -> {}: "{}"\r\n'.format(type(self.path), self.path) + 
             ".chrono   -> {}: {}\r\n".format(type(self.chrono), self.chrono) + 
             ".fun      -> funzione: {}\r\n".format(str(self.fun)) + 
             ".ritaglio -> list of 4:\r\n" + 
             "    [0] x -> {}\r\n".format(self.ritaglio[0]) + 
             "    [1] y -> {}\r\n".format(self.ritaglio[1]) + 
             "    [2] w -> {}\r\n".format(self.ritaglio[2]) + 
             "    [3] h -> {}\r\n".format(self.ritaglio[3]) + 
             ".x        -> {}: {}\r\n".format(type(self.x), str(self.x)) + 
             ".y        -> {}: {}\r\n".format(type(self.y), str(self.y)) + 
             ".w        -> {}: {}\r\n".format(type(self.w), str(self.w)) + 
             ".h        -> {}: {}\r\n".format(type(self.h), str(self.h)) + 
             ".pl       -> {}: {}\r\n".format(type(self.pl), str(self.pl)) + 
             ".pv       -> {}: {}\r\n".format(type(self.pv), str(self.pv))]
        return a[0]
