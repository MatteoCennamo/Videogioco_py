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
import threading


'''
2) PER FUNZIONI
'''
class ClickerCursor(threading.Thread):
    '''Oggetto < Thread > responsabile dell'animazione del pulsante quando 
    viene cliccato.'''
    def __init__(self, button = None, sleep = .2):
        super().__init__()
        # Oggetto 'GameButton'
        self.button = button
        # Il Lock serve per non interferire con altri processi
        self.lock = threading.Lock()
        # Tempo di attesa prima cambiare il background del pulsante
        self.sleep = sleep  # in secondi
    def run(self):
        '''Esegue l'animazione del pulsante.'''
        with self.lock:
            self.button.cursor = True
            self.button.pady += 2
        time.sleep(self.sleep)
        with self.lock:
            self.button.cursor = False
            self.button.pady -= 2

def buttonCommand(fun = None, *, button):
    '''Animazione del pulsante quando viene cliccato.'''
    def decorator_buttonCommand(fun):
        @functools.wraps(fun)
        def wrapper_buttonCommand(*args, **kargs):
            clicker = ClickerCursor(button)
            clicker.start()  # thread per l'animazione del pulsante
            value = fun(*args, **kargs)  # esegue funzione associata al pulsante
            return value
        return wrapper_buttonCommand
    if fun:
        return decorator_buttonCommand(fun)
    return decorator_buttonCommand
