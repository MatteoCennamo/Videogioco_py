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
    '''< Thread > object which performs a request (.start method) with the 
    provided '.url'. Then it stores the data in '.data' attribute.'''
    def __init__(self, button = None):
        super().__init__()
        # GameButton object
        self.button = button
        # Il Lock serve per non interferire con altri processi
        self.lock = threading.Lock()
    def run(self):
        '''Makes the URL request and stores the data in '.data' attribute.'''
        with self.lock:
            self.button.cursor = True
            self.button.pady += 2
        time.sleep(0.2)
        with self.lock:
            self.button.cursor = False
            self.button.pady -= 2

def buttonCommand(fun = None, *, button):
    '''Animazione del pulsante quando viene cliccato.'''
    def decorator_buttonCommand(fun):
        @functools.wraps(fun)
        def wrapper_buttonCommand(*args, **kargs):
            clicker = ClickerCursor(button)
            clicker.start()
            value = fun(*args, **kargs)
            return value
        return wrapper_buttonCommand
    if fun:
        return decorator_buttonCommand(fun)
    return decorator_buttonCommand
