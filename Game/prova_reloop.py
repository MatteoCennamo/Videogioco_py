# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:59:20 2020

@author: mattc
"""

'''
IMPORT
'''
# Importa i pacchetti
import GameToolKit as gtk
import pygame


'''
INIZIALIZZA IL GIOCO
'''
# Crea variabile che conta il numero di iterazioni nel main loop
ite = 0

# Inizializza il gioco
root = gtk.GameInit(title = "ARANCIONE", screen_size = (1000, 500), 
                    window_size = (1090, 550), pos_wd = (0, 0), 
                    mainloop = lambda: prova())

'''
AGGIUNGI OGGETTI
'''
# Crea oggetto personaggio
player = gtk.Personaggio("./Sprites/SpriteWarrior.png", (410, 400, 390, 350), 
                         (0, 0), (100, 100), (0.2, 0.2))
# Aggiungi il personaggio a root
root.OBJadd("personaggio", player)

'''
FUNZIONI DI MAINLOOP
'''
#####--- PRIMA FUNZIONE DEL MAIN LOOP ---#####
def prova():
    global root, ite
    ite += 1
    dt = root.clock.tick(60)
    # Pulisci la surface
    root.window.surface = pygame.Surface(root.window.size)
    # Crea rettangolo arancione
    pygame.draw.rect(root.window.surface, gtk.ORANGE, 
                     (100, 100, 20, 20))
    
    # Muovi la finestra
    root.MoveWindow((-0.02*dt, -0.02*dt))
    root.updateWindow()
    
    # Rimpristina nuovo main loop
    if ite > 200:
        # Rinomina il titolo della finestra
        root.screen.title = pygame.display.set_caption("GIALLO")
        ite = 0
        # Fai sparire il personaggio
        root.obj["personaggio"][0].status = False
        root.ReLoop(mainloop = lambda: prova_reloop())

#####--- SECONDA FUNZIONE DEL MAIN LOOP ---#####
def prova_reloop():
    global root, ite
    ite += 1
    dt = root.clock.tick(60)
    # Pulisci la surface
    root.window.surface = pygame.Surface(root.window.size)
    # Crea rettangolo giallo
    pygame.draw.rect(root.window.surface, gtk.YELLOW, 
                     (100, 100, 20, 20))
    # root.screen.set_mode.blit(root.window.surface, root.window.pos)
    # Muovi la finestra
    root.MoveWindow((0.02*dt, 0.02*dt))
    root.updateWindow()
    
    # Rimpristina nuovo main loop
    if ite > 100:
        # Rinomina il titolo della finestra
        root.screen.title = pygame.display.set_caption("ARANCIONE")
        ite = 0
        # Fai riapparire il personaggio
        root.obj["personaggio"][0].status = True
        root.ReLoop(mainloop = lambda: prova())

'''
MAINLOOP
'''
# Avvia il main loop
root.MainLoop()
