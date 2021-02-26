# -*- coding: utf-8 -*-
"""
Qui sono contenuti tutti i decoratori.

INDICE:
    
    1) IMPORT
    
    2) PER FUNZIONI

"""
'''
1) IMPORT
'''
import pygame
import functools
import GameToolKit as gtk


'''
2) PER FUNZIONI
'''
def actBoxes(fun = None, *, updaterFUN = None, arrows = {}):
    DefaulArrows = {'right': True, 'left': True, 'up': True, 'down': True}
    # Aggiungi ad 'arrows' le chiavi mancanti da 'DefaultArrows'
    for k, v in DefaulArrows.items():
        if k not in arrows.keys():
            arrows[k] = v
    def decorator_actBox(fun):
        @functools.wraps(fun)
        def wrapper_actBox(*args, **kargs):
            # Entra nel loop
            while True:
                # Scansiono gli input dello user
                for e in pygame.event.get():
                    # Pulsante spinto in basso
                    if e.type == pygame.KEYDOWN:
                        # Pigia pulsante a destra o sinistra
                        if arrows['right'] and e.key == pygame.K_RIGHT:
                            fun('right')
                        if arrows['left'] and e.key == pygame.K_LEFT:
                            fun('left')
                        if arrows['down'] and e.key == pygame.K_DOWN:
                            fun('down')
                        if arrows['up'] and e.key == pygame.K_UP:
                            fun('up')
                        # Se premi 'Invio'
                        if e.key == pygame.K_RETURN:
#                            fun('return')
                            return fun('return')
                updaterFUN()
        return wrapper_actBox
    if fun:
        return decorator_actBox(fun)
    return decorator_actBox
