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
import time
import functools
import GameToolKit as gtk


'''
2) PER FUNZIONI
'''
def buttonCommand(fun = None, *, button = None, master = None, surf = None, pos = None):
    '''Stabilisci la ResponceBox principale la sua posizione. Se il pulsante 
    non ha una ResponceBox principale, passare la posizione del pulsante con 
    'master_pos' e in 'master' passa il pulsante.'''
    def decorator_buttonCommand(fun):
        @functools.wraps(fun)
        def wrapper_buttonCommand(*args, **kargs):
            if not master:
                button.cursor = True
                button.render(surf, pos)
                value = fun()
                time.sleep(0.2)
                button.cursor = False
                button.render(surf, pos)
            else:
                button.cursor = True
                master.updateSurface()
                time.sleep(0.2)
                button.cursor = False
                master.updateSurface()
            return value
        return wrapper_buttonCommand
    if fun:
        return decorator_buttonCommand(fun)
    return decorator_buttonCommand
