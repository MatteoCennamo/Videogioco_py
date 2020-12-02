# -*- coding: utf-8 -*-
"""
Prova di utilizzo del 'ReLoop'.
"""

'''
IMPORT
'''
# Importa i pacchetti
import GameToolKit as gtk
import OBJfunctions as objf  # Funzioni degli OBJ
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
player = gtk.Personaggio("./Sprites/Personaggi_16x16.png", (48, 0, 16, 16), 
                         (350, 350), (75, 75), (0.2, 0.2), pl = 15, pv = 50)
# Aggiungi il personaggio a root
root.OBJadd("personaggio", player, objf.playerAnimation)

'''
FUNZIONI DI MAINLOOP
'''
#####--- PRIMA FUNZIONE DEL MAIN LOOP ---#####
def prova():
    global root, ite
    ite += 1
    # Pulisci la surface
    root.window.surface = pygame.Surface(root.window.size)
    # Crea rettangolo arancione
    pygame.draw.rect(root.window.surface, gtk.ORANGE, 
                     (100, 100, 20, 20))
    
    # Aggiorna la finestra
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
    # Pulisci la surface
    root.window.surface = pygame.Surface(root.window.size)
    # Crea rettangolo giallo
    pygame.draw.rect(root.window.surface, gtk.YELLOW, 
                     (100, 100, 20, 20))
    # Aggiorna la finestra
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
