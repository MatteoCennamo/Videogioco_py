# -*- coding: utf-8 -*-
"""
Prova del gioco.

INDICE:
    
    1) IMPORT
    2) INIZIALIZZA GIOCO
    3) AGGIUNGI OGGETTI
    4) FUNZIONE DI MAINLOOP
    5) MAINLOOP

"""

'''
1) IMPORT
'''
# Importa i pacchetti
import GameToolKit as gtk    # Classi del gioco
import OBJfunctions as objf  # Funzioni degli OBJ
import pygame                # Pacchetto standard per videogame in Python


'''
2) INIZIALIZZA IL GIOCO
'''
# Inizializza il gioco
root = gtk.GameInit(title = "Prova 1", screen_size = (1000, 500), 
                    window_size = (1200, 700), #pos_wd = (0, 0), 
                    mainloop = lambda: prova())

'''
3) AGGIUNGI OGGETTI
'''
# Crea oggetto personaggio
player = gtk.Personaggio("./Sprites/Personaggi_16x16.png", (48, 0, 16, 16), 
                         (350, 350), (75, 75), (0.2, 0.2), pl = 15, pv = 50)
# Aggiungi il personaggio a 'root'
root.OBJadd("personaggio", player, objf.playerAnimation)

# Crea monete
for loc in [(600, 300), (0, 0), (135, 315), (1000, 100)]:
    coin = gtk.Oggetto("./Sprites/Oggetti.png", (0, 0, 12, 12), loc, 
                   (58, 58), "coin", pv = 15, pl = 0, nFrames = 5)
    # Aggiungi monete a 'root'
    root.OBJadd("oggetto", coin, objf.collisionCoins)

# Crea gli alberi
for loc in [(110, 200), (130, 310), (1020, 115)]:
    three = gtk.Oggetto("./Sprites/Alberi.png", (0, 0, 32, 32), loc, 
                       (120, 150), "three", pv = 120, pl = 40)
    # Aggiungi gli alberi a 'root'
    root.OBJadd("ostacolo", three, objf.collinionObstacles)

# Crea le rocce
rock = gtk.Oggetto("./Sprites/Rocce.png", (2, 0, 36, 34), (800, 200), 
                   (130, 115), "rock", pv = 50, pl = 20)
# Aggiungi le rocce a 'root'
root.OBJadd("ostacolo", rock, objf.collinionObstacles)


'''
4) FUNZIONE DI MAINLOOP
'''
#####--- MAIN LOOP ---#####
def prova():
    global root
    # Pulisci la surface di 'root.window'
    root.window.surface = pygame.Surface(root.window.size)
    # Colora la surface di 'root.window' di verde
    root.window.surface.fill(gtk.GREEN)
    # Aggiorna la finestra
    root.updateWindow()


'''
5) MAINLOOP
'''
# Avvia il main loop
root.MainLoop()