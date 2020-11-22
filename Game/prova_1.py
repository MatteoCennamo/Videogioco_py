# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 18:16:11 2020

@author: mattc
"""

'''
IMPORT
'''
# Importa i pacchetti
import GameToolKit as gtk
import pygame

'''
FUNZIONI OBJ
'''
def nulla(root = None, obj = None):
    return root, obj

def collinionObstacles(root = None, obj = None):
    if obj.status:  # se è visibile
        out = gtk.collisionDetection(root, root.obj["personaggio"][0], obj)
        if len(out) > 0:   # c'è stata collisione
            done = False
            # Collided = True
            obj.collided = True
            if "1" in out: # collisione da destra
                root.obj["personaggio"][0].x = obj.x + obj.w - obj.pl
                done = True
            if "2" in out: # collisione da sinistra
                root.obj["personaggio"][0].x = (obj.x - 
                        root.obj["personaggio"][0].w + obj.pl)
                done = True
            if ("3" in out) and (not done): # collisione dal basso
                root.obj["personaggio"][0].y = (obj.y + obj.h -  
                        root.obj["personaggio"][0].pv)
            if ("4" in out) and (not done): # collisione dali'alto
                root.obj["personaggio"][0].y = (obj.y - 
                        root.obj["personaggio"][0].h + obj.pv)
        else:  # non c'è stata collisione
            obj.collided = False
    return root, obj

def collisionObjects(root = None, obj = None):
    if obj.status == True:
        x = root.obj["personaggio"][0].x
        y = root.obj["personaggio"][0].y
        w = root.obj["personaggio"][0].w
        h = root.obj["personaggio"][0].h
        pl = root.obj["personaggio"][0].pl
        pv = root.obj["personaggio"][0].pv
        
        if x + w - pl >= obj.x and x <= obj.x + obj.w - pl:
            if y + h - obj.pv >= obj.y and y <= obj.y + obj.h - pv:
                obj.collided = True
                obj.status = False
    return root, obj

'''
INIZIALIZZA IL GIOCO
'''
# Inizializza il gioco
root = gtk.GameInit(title = "Prova 1", screen_size = (1000, 500), 
                    window_size = (1200, 700), pos_wd = (0, 0), 
                    mainloop = lambda: prova())

'''
AGGIUNGI OGGETTI
'''
# Crea oggetto personaggio
player = gtk.Personaggio("./Sprites/SpriteWarrior.png", (410, 390, 390, 360), 
                         (350, 350), (100, 100), (0.2, 0.2), pl = 20, pv = 60)
# Aggiungi il personaggio a root
root.OBJadd("personaggio", player, nulla)

# Crea monete
for loc in [(600, 300), (0, 0), (1000, 100)]:
    coin = gtk.Oggetto("./Sprites/Coin.png", (335, 80, 450, 720), loc, 
                   (35, 58), "coin", pv = 15, pl = 0)
    root.OBJadd("oggetto", coin, collisionObjects)

# Aggiungi ostacoli
three = gtk.Oggetto("./Sprites/Alberi.png", (0, 0, 32, 32), (110, 200), 
                   (120, 150), "three", pv = 120, pl = 40)
root.OBJadd("ostacolo", three, collinionObstacles)
rock = gtk.Oggetto("./Sprites/Rocce.png", (2, 0, 36, 34), (800, 200), 
                   (130, 115), "rock", pv = 50, pl = 20)
root.OBJadd("ostacolo", rock, collinionObstacles)


'''
FUNZIONE DI MAINLOOP
'''
#####--- MAIN LOOP ---#####
def prova():
    global root
    # Pulisci la surface
    root.window.surface = pygame.Surface(root.window.size)
    root.window.surface.fill(gtk.GREEN)
    # Aggiorna la finestra
    root.updateWindow()


'''
MAINLOOP
'''
# Avvia il main loop
root.MainLoop()