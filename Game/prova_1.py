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
import GameBuilder as GB     # Per le funzioni di import di livello


'''
2) INIZIALIZZA IL GIOCO
'''
# Inizializza il gioco
root = gtk.GameInit(title = "Prova 1", screen_size = (1000, 600), 
                    window_size = (1200, 700), #pos_wd = (0, 0), 
                    mainloop = lambda: prova())

'''
3) AGGIUNGI OGGETTI
'''
# Crea oggetto personaggio
player = gtk.Personaggio("./Sprites/Personaggi_16x16.png", (48, 0, 16, 16), 
                         (910, 840), (75, 75), (0.2, 0.2), pl = 15, pv = 50)
# Aggiungi il personaggio a 'root'
root.OBJadd("personaggio", player, objf.playerAnimation)

# Importa il livello
level_df = GB.txt2DataFrame('./prova2.txt')
# Crea gli obj dal dataframe
GB.DataFrame2Map(level_df, root)

##########--- DEBUG ---##########--- DEBUG ---##########
print(root)

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
