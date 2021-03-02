# -*- coding: utf-8 -*-
'''
Questo pacchetto contiene tutte le classi necessarie al gioco.

INDICE:
    
    1) IMPORT
    
    2) COLORI
    
    3) FUNZIONI:
        -> _Wait
        -> _Void
        -> collisionDetection
        -> OBJactivete
        -> truncString2List
        -> multiQuest
        
    4) CLASSE GameInit:
        
    5) CLASSE Screen:
        
    6) CLASSE Window:
    
    7) CLASSE StatusBar:
        
    8) CLASSE Personaggio:
        
    9) CLASSE Oggetto:
    
    10) CLASSE GameString:
    
    11) CLASSE ResponceBox:

'''

'''
1) IMPORT
'''
import pygame                # Pacchetto standard per videogame in Python
import pygame.freetype       # Per il font delle scritte
import OBJfunctions as objf  # Per le funzioni degli obj e il Menu
#import GameDecorators as GD  # Per i decoratori del gioco
import sys                   # Per lavorare con i moduli e pacchetti


'''
2) COLORI
'''
# colors = (("BLACK", (0, 0, 0)), ("GRAY", (128, 128, 128)), ("WHITE", (255, 255, 255)), 
#           ("RED", (255, 0, 0)), ("BLUE", (0, 0, 255)), ("YELLOW", (255, 255, 0)), 
#           ("MAGENTA", (255, 0, 255)), ("CYAN", (0, 255, 255)), ("ORANGE", (255, 128, 0)), 
#           ("DARK_ROSE", (255, 0, 128)), ("LILAC", (200, 100, 160)), ("ROSE", (255, 90, 90)), 
#           ("SKIN_ROSE", (255, 130, 130)), ("PURPLE", (160, 0, 255)), ("SKY_BLUE", (0, 128, 255)))
#globals()['GREEN'] = (128, 255, 0)

# Possono essere estratti con il comando: GameToolKit.BLACK...
setattr(sys.modules[__name__], "BLACK", (0, 0, 0))
setattr(sys.modules[__name__], "GRAY", (128, 128, 128))
setattr(sys.modules[__name__], "WHITE", (255, 255, 255))
setattr(sys.modules[__name__], "RED", (255, 0, 0))
#setattr(sys.modules[__name__], "GREEN", (0, 255, 0))
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


'''
3) FUNZIONI
'''
# Main Loop di default
def _Wait():
    '''Non fa nulla e non restituisce nessun valore.'''
    pass
# Funzione degli OBJ di default
def _Void(root = None, obj = None):
    '''Restituisce 'root' e 'obj' senza fare nulla.'''
    return root, obj

# Collision detection
def collisionDetection(root, collider, collided):
    '''Stabilisce se 'collider' ha colliso con 'collided'. 'root' deve essere
    un oggetto 'GameInit', 'collider' e 'collided' devono essere oggetti 
    'Presonaggio' o 'Oggetto'. Casi possibili di 'out':
        -> "":   non c'è stata collisione
        -> "1":  collisione da destra
        -> "2":  collisione da sinistra
        -> "3":  collisione dal basso
        -> "4":  collisione dall'alto
        -> "13": collisione dal basso a destra
        -> "14": collisione dall'alto a destra
        -> "23": collisione dal basso a sinistra
        -> "24": collisione dall'alto a sinistra'''
    # xr, yr, wr, hr = collider.get_collision_rect()
    # xd, yd, wd, hd = collided.get_collision_rect()
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
    

# Lancia funzioone degli obj e rappresentali in 'Window'
def OBJactivete(obj, root):
    '''Lancia la funzione dell'obj se il menu è chiuso e renderizza l'obj in 
    'Window' se 'obj.status' = True. 'obj' è un oggetto 'Personaggio' o 'Oggetto'.
    'root' è un oggetto 'GameInit'.'''
    # Lancia la funzione associata all'obj (solo se il menu è chiuso)
    if root.obj["menu"][0].status == False:
        root, obj = obj.fun(root = root, obj = obj)
    # Solo se status = True
    if obj.status:
        # Rappresenta gli obj nella window
        obj.render(root.window.surface)

# Trasforma una stringa in una lista di stringhe
def truncString2List(s, limit):
    '''Trasforma una stringa in una lista di stringhe. Le stringhe sono troncate 
    dopo 'limit' numero di caratteri.'''
    l_txt = s.split('\n') if isinstance(s, str) else s.string.split('\n')
    list_txt = []
    def handleLimit(s, limit, main):
        '''Tronca una stringa al limite di caratteri, trasformandola in lista.'''
        list_txt = []   # Inizializza lista di output
        partial_s = ''  # Inizializza stringa parziale
        for w in s.split(' '): # Prendi parola per parola
            len_partial = len(partial_s) if isinstance(main, str) else \
                main.get_size(partial_s)[0]
            len_w = len(w) if isinstance(main, str) else main.get_size(w)[0]
            if len_partial + len_w  + 1 > limit: # Limite superato
                if not partial_s:   # se partial_s è vuoto
                    list_txt += [' ' + w]
                else: # limite superato, ma partial_s non è vuoto
                    list_txt += [partial_s]
                    partial_s = ' ' + w
            else: # Limite non superato
                partial_s += ' ' + w
        list_txt += [partial_s]
        return list_txt
    for i in l_txt:
        list_txt += handleLimit(i, limit, s)
    return [s[1:] for s in list_txt if len(s) > 0]

def multiQuest(root, domanda, *args, truncQuest = 100, 
               truncAns = 100, QuestBoxSize = None, AnsBoxSize = (94, 56), 
               QuestParams = None, AnsParams = None):
    '''Crea una barra dove viene rappresentata la 'domanda'. Si può rispondere 
    'sì' o 'no' alla domanda (default). Restituisce 0 se è stato risposto 'no', 
    1 se la risposta è 'sì' e così via se ci sono altre risposte. 'domanda' è 
    una stringa (puoi andare a capo con '\n'). 
    'truncQuest' è il limite di caratteri di 'domnda' prima di andare a capo. 
    'truncAns' è il numero di caratteri di 'args'. 
    'QuestBoxSize' è la tupla che contiene le dimensioni della finestra che 
    contiene la domada (di default, larghezza pari a quella dello schermo e una 
    altezza pari a 1/6 di quella dello schermo).
    'AnsBoxSize' è la tupla che contiene le dimensioni della finestra che 
    contiene le risposte. 
    'QuestParams' è un dizionario che contiene i parametri per il testo della 
    domanda, mentre 'AnsParams' è quello per la risposta. I parametri che possono 
    essere immessi sono quelli di dell'oggetto 'GameToolKit.ResponceBox'.'''
    # Scostamento dal bordo dello schermo
    OFFSETX = 10
    # Scostamento dalla box della domanda
    OFFSETY = 10
    if QuestParams == None:
        QuestParams = {}
    if AnsParams == None:
        AnsParams = {}
    # Crea la surface che verrà rappresentata
    if QuestBoxSize == None:
        surf_x, surf_y = root.screen.size[0], root.screen.size[1] / 6
    else:
        surf_x, surf_y = QuestBoxSize
    # Valori di default di 'QuestParams'
    DefQP = {'fontsize': 20, 'padx': 5, 'pady': 5, 'bg': (255, 255, 255), 
             'textcolor': (0, 0, 0), 'cursor': False}
    # Modifica QuestParams con i valori di default
    for k, v in DefQP.items():
        if k not in QuestParams:
            QuestParams[k] = v
    # Valori di default di 'AnsParams'
    AnsQP = {'fontsize': 28, 'padx': 5, 'pady': 10, 'bg': (255, 255, 255), 
             'textcolor': (0, 0, 0), 'cursor': True, 'current': 0}
    # Modifica AnsParams con i valori di default
    for k, v in AnsQP.items():
        if k not in AnsParams:
            AnsParams[k] = v
    
    surf = ResponceBox((surf_x, surf_y), truncString2List(domanda, truncQuest), 
                       **QuestParams)
    
    # Crea il box che contiene le risposte
    if len(args) == 0:
        args = ['No', 'Sì']
    txts = []
    for arg in args:
        if isinstance(arg, str):
            txts.append(truncString2List(arg, truncAns))
        else:
            txts.append(arg)
    ansBox = ResponceBox(AnsBoxSize, *txts, **AnsParams)
    
    # Entra nel loop
    while True:
        # Scansiono gli input dello user
        for e in pygame.event.get():
            # Pulsante spinto in basso
            if e.type == pygame.KEYDOWN:
                
                # Pigia pulsante a destra o sinistra
                if e.key == pygame.K_RIGHT:
                    # Modifica il cursore e il valore di ritorno
                    ansBox.cursorMove((1, 0))
                if e.key == pygame.K_LEFT:
                    # Modifica il cursore e il valore di ritorno
                    ansBox.cursorMove((-1, 0))
                if e.key == pygame.K_DOWN:
                    # Modifica il cursore e il valore di ritorno
                    ansBox.cursorMove((0, 1))
                if e.key == pygame.K_UP:
                    # Modifica il cursore e il valore di ritorno
                    ansBox.cursorMove((0, -1))
                # Se premi 'Invio'
                if e.key == pygame.K_RETURN:
                    return ansBox.get_responces()
                
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1: # pulsante sinistro del mouse
                    ansBox.mousePress((-root.screen.size[0] \
                  + ansBox.size[0] + OFFSETX + e.pos[0], -root.screen.size[1] \
                  + surf_y + ansBox.size[1] + OFFSETY + e.pos[1]), e.button)
        
        # Pulisci la surface di 'root.window'
        root.window.surface = pygame.Surface(root.window.size)
        # Colora la surface di 'root.window' di verde
        root.window.surface.fill(sys.modules[__name__].GREEN)
        
        # Aggiorna la finestra
        root.updateWindow()
        # Rappresenta la surface con la domanda nello schermo
        surf.render(root.window.surface, (-root.window.pos[0], -root.window.pos[1] \
                                        + root.screen.size[1] - surf_y + 1))
        # Rappresenta la surface con il box delle risposte nello schermo
        ansBox.render(root.window.surface, (-root.window.pos[0] + root.screen.size[0] \
                      - ansBox.size[0] - OFFSETX, -root.window.pos[1] + \
                      root.screen.size[1] - surf_y - ansBox.size[1] - OFFSETY))
        root.screen.set_mode.blit(root.window.surface, root.window.pos)
        root.status_bar.updateBar(root)
        pygame.display.update()

'''
4) CLASSE GAMEINIT
'''
# Creo il root che contiene la finestra
# title    -> titolo della finestra
# size     -> tupla che contiene la grandezza della finestra (x, y).
# pos_wd   -> posizione iniziale della finestra, di default pari a (0, 0)
# mainloop -> funzione che contiene i comandi da ripetere a ogni ciclo while.
class GameInit():
    '''Inizializza il gioco.'''
    def __init__(self, title = "Default title", screen_size = (1000, 700), 
                 window_size = (1000, 700), pos_wd = (0, 0), mainloop = _Wait, 
                 tkinterObject = None, builderMode = False):
        # Integrare a tkinter. 'tkinterObject' è un 'tkinter.Tk'
        if tkinterObject == None:
            self.tkinterObject = None
        else:
            self.tkinterObject = tkinterObject
        
        # Verifica se si trova in Builder Mode
        if builderMode:
            self.builderMode = True
        else:
            self.builderMode = False
        
        # Inizializza 'pygame'
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
        
        # Crea la barra di stato
        self.status_bar = StatusBar([self.screen.size[0], 25])
        
        # Crea il menu
        menu = Oggetto("./Sprites/Menu.png", (0, 0, 186, 134), (0, 0), 
                       (372, 268), "menu", status = False)
        
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
        
        # Crea attributo '._freeze' che congela lo schermo se è True
        self._freeze = False
        
        # Crea la variabile che mantiene il mainloop
        self.mainloop = lambda: mainloop()
        
        # Crea un dizionario di oggetti.
        # vuoto di default:
        self.obj = {"personaggio": [], "oggetto": [], "ostacolo": [], 
                    "volante": [], "pavimento": [], "menu": []}
        
        # Aggiungi il Menu agli obj
        self.OBJadd("menu", menu, objf.menuOpen)
        # Crea il puntatore
        puntatore = Oggetto("./Sprites/Menu.png", (0, 0, 1, 1), (self.obj["menu"][0].x, 
                            self.obj["menu"][0].y), (self.obj["menu"][0].w, int(
                                    self.obj["menu"][0].h / 4)), "puntatore", 
                                status = False)
        puntatore.image.set_alpha(100)
        # Aggiungi il puntatore del Menu
        self.OBJadd("menu", puntatore, _Void)
    
    # Crea il main loop e lo avvia
    def MainLoop(self):
        '''Crea il main loop del gioco e avvia la funzione associata all'attributo
        '.mainloop' dell'oggetto 'GameInit'. Stabilisce i rapporti con la 
        tastiera.'''
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
                        # Apre il Menu
                        if e.key == pygame.K_m and not self.builderMode:
                            # Blocca il movimento del personaggio
                            self.obj["personaggio"][0].xchange = 0
                            self.obj["personaggio"][0].ychange = 0
                            # Apri la funzione del menu
                            objf.menuOpen(self)
                        # Se premi 'Invio'
                        if e.key == pygame.K_RETURN and self.builderMode:
                            # Aggiungi l'obj corrente alla lista del tkinter object
                            old_obj = self.obj["personaggio"][0]
                            self.tkinterObject.obj += \
                            [{'CLASS': self.tkinterObject.main_frame.combo_class.get(),
                              'CAT': self.tkinterObject.main_frame.combo_cat.get(), 
                              'X': old_obj.ritaglio[0], 'Y': old_obj.ritaglio[1],
                              'W': old_obj.ritaglio[2], 'H': old_obj.ritaglio[3],
                              'PATH': old_obj.path, 'xPOS': int(old_obj.x), 
                              'yPOS': int(old_obj.y), 'zPOS': int(old_obj.z),
                              'WIDTH': old_obj.w, 'HEIGHT': old_obj.h, 
                              'xSPEED': self.tkinterObject.main_frame.xspeed.get(), 
                              'ySPEED': self.tkinterObject.main_frame.yspeed.get(), 
                              'FUN': self.tkinterObject.main_frame.combo_fun.get(), 
                              'TYPE': self.tkinterObject.main_frame.type.get(), 
                              'PL': self.tkinterObject.main_frame.pl.get(), 
                              'PV': self.tkinterObject.main_frame.pv.get(), 
                              'nFRAMES': self.tkinterObject.main_frame.nFrames.get()}]
                            print(self.tkinterObject.obj[-1])
                            new_obj = Oggetto(old_obj.path, old_obj.ritaglio, 
                                              (old_obj.x, old_obj.y, old_obj.z), (old_obj.w, 
                                              old_obj.h), self.tkinterObject.main_frame.type)
                            self.OBJadd(self.tkinterObject.main_frame.combo_cat.get(), 
                                        new_obj)
                
                # Prendi il dizionario delle chiavi (valcono 1 se pressate)
                keys = pygame.key.get_pressed()
                # Verifica gli spostamenti orizzontali e verticali
                if keys[pygame.K_LEFT]:
                    self.obj["personaggio"][0].xchange = -1
                if keys[pygame.K_RIGHT]:
                    self.obj["personaggio"][0].xchange = 1
                if keys[pygame.K_UP]:
                    self.obj["personaggio"][0].ychange = -1
                if keys[pygame.K_DOWN]:
                    self.obj["personaggio"][0].ychange = 1
                # Se non vengono pigiati, metti a 0 la velocità
                if not any([keys[pygame.K_LEFT], keys[pygame.K_RIGHT]]) or \
                    all([keys[pygame.K_LEFT], keys[pygame.K_RIGHT]]):
                    self.obj["personaggio"][0].xchange = 0
                if not any([keys[pygame.K_UP], keys[pygame.K_DOWN]]) or \
                    all([keys[pygame.K_UP], keys[pygame.K_DOWN]]):
                    self.obj["personaggio"][0].ychange = 0
                # Se sia la velocità in x che in y sono diverse da 0, diminuiscile
                if all([self.obj["personaggio"][0].xchange, 
                        self.obj["personaggio"][0].ychange]):
                    self.obj["personaggio"][0].xchange /= 1.414
                    self.obj["personaggio"][0].ychange /= 1.414
                
                # Prendi il tempo
                self.dt = self.clock.tick(60)  # 60
                
                # Modifica la posizione del personaggio
                self.obj["personaggio"][0].x += self.obj[
                        "personaggio"][0].xchange * self.obj[
                                "personaggio"][0].xspeed * self.dt
                self.obj["personaggio"][0].y += self.obj[
                        "personaggio"][0].ychange * self.obj[
                                "personaggio"][0].yspeed * self.dt
                
                # Collision con i bordi della window
                if not self.builderMode:
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
                    if self.obj["personaggio"][0].y < 0: #self.status_bar.size[1]:
                        self.obj["personaggio"][0].y = 0 #self.status_bar.size[1]
                
                # Avvia il main loop
                self.mainloop()
                
                # Aggiorna le finestre
                if self.tkinterObject != None:
                    # Se la finestra pygame è stata chiusa
                    if self.run == False:
                        # Chiudi anche la finestra tkinter
                        self.tkinterObject.destroy()
                        pygame.display.update()
                    else:
                        try:
                            self.tkinterObject.update()
                        except:
                            # Il tkinter object è stato distrutto
                            self.run = False # chiudi anche la finestra pygame
                        finally:
                            pygame.display.flip()
                else:
                    pygame.display.update()
        
        # Quado esci dal main loop
        pygame.quit()
    
    # Rappresenta il Menu in Window
    # Avvia un nuovo main loop
    def ReLoop(self, mainloop = _Wait):
        '''Esce dal main loop e rientra con un nuovo 'GameInit.mainloop'.'''
        # Esce dal main loop
        self.run = False
        
        # Modifica il mainloop con quello nuovo
        self.mainloop = lambda: mainloop()
        
        # Rientra nel nuovo main loop
        self._reloop = True
    
    # Aggiorna la finestra
    def updateWindow(self):
        '''Sposta la finestra 'Window' a seconda della posizione dell'oggetto 
        'Personaggio'. Rappresenta gli oggetti che hanno l'attributo '.status' = 
        True nella '.surface' di 'Window'. Rappresenta la barra di stato
        'GameInit.status_bar'. Renderizza 'Window.surface' in 
        'GameInit.screen.set_mode.'''
        # Scansiona gli obj 'pavimento'.
        # I pavimenti sono rappresentati in ordine di apparizione in 
        # 'self.obj['pavimento']'.
        for e in self.obj['pavimento']:
            # Lancia la funzione e renderizza l'obj
            OBJactivete(e, self)
        
        # Crea una lista di tutti gli oggetti (tranne 'volante', 'pavimento' e 'menu')
        OBJlist = []
        for k, v in self.obj.items():
            if k not in ('volante', 'pavimento', 'menu'):
                OBJlist += v
        
        # Ordina gli oggetti per y+h (in ordine crescente)
        OBJlist.sort(key = lambda obj: obj.y + obj.h)
        
        # Scansiona gli obj
        for e in OBJlist:
            # Lancia la funzione e renderizza l'obj
            OBJactivete(e, self)
        
        # Crea la lista dei valori ordinati per y+h dei 'volante'
        OBJvolante = self.obj['volante']
        OBJvolante.sort(key = lambda obj: obj.y + obj.h)
        
        # Scansiona gli obj 'volante'
        for e in OBJvolante:
            # Lancia la funzione e renderizza l'obj
            OBJactivete(e, self)
        
        # Scansiona menu
        for e in self.obj["menu"]:
            # Solo se status = True
            if e.status:
                # Rappresenta gli obj nella window
                e.render(self.window.surface)
        
        # Sposta la finestra insieme al personaggio
        dx = [self.obj["personaggio"][0].x - self.screen.size[0] / 2 + 
              self.window.pos[0] + self.obj["personaggio"][0].w / 2]
        dy = [self.obj["personaggio"][0].y - self.screen.size[1] / 2 + 
              self.window.pos[1] + self.obj["personaggio"][0].h / 2]
        
        # Sposta la finestra
        self.window.MoveWindow((-dx[0], -dy[0]), self.screen.size, 
                               self.status_bar.size)
        # Aggiungi surface rossa
        if self.builderMode:
            if self.obj["personaggio"][0].w - 2 * self.obj["personaggio"][0].pl < 0:
                w = 0
            else:
                w = self.obj["personaggio"][0].w - 2 * self.obj["personaggio"][0].pl
            if self.obj["personaggio"][0].h - self.obj["personaggio"][0].pv < 0:
                h = 0
            else:
                h = self.obj["personaggio"][0].h - self.obj["personaggio"][0].pv
            redSurf = pygame.Surface((w, h))
            redSurf.fill(sys.modules[__name__].RED)
            redSurf.set_alpha(128)
            self.window.surface.blit(redSurf, (self.obj["personaggio"][0].x + 
                                               self.obj["personaggio"][0].pl, 
                                               self.obj["personaggio"][0].y + 
                                               self.obj["personaggio"][0].pv))
        # Rappresenta la finestra nella nuova posizione
        self.window.render(self.screen)
        # Aggiungi riga di stato in alto
        self.status_bar.updateBar(self)
    
    
    # Aggiung oggetti a .obj
    def OBJadd(self, objType, obj, fun = _Void):
        '''Aggiunge un oggetto al dizionario 'GameInit.obj'. 'objType' è la 
        chiave del dizionario, 'obj' è il valore corrispondente che si vuole 
        aggiungere (deve essere di tipo 'Oggetto' o 'Personaggio'). 'fun' è 
        la funzione che si vuole associare all'oggetto.'''
        
        # Aggiungi funzione all'oggetto
        obj.fun = fun
        # Aggiungi elemento alla lista
        self.obj[objType.lower()] = self.obj[objType.lower()] + [obj]
    
    # Cosa restituisce quando usi la funzione 'str'
    def __str__(self):
        a = ["<class 'GameToolKit.GameInit'>:\r\n\r\n" + 
             ".screen     -> {}".format(str(self.screen)) + 
             ".window     -> {}".format(str(self.window)) + 
             ".status_bar -> {}".format(str(self.status_bar)) + 
             ".clock      -> pygame.time.Clock\r\n" + 
             ".dt         -> time frame: {}\r\n".format(str(self.dt)) + 
             ".run        -> logical: {}\r\n".format(self.run) + 
             "._reloop    -> logical: {}\r\n".format(self._reloop) + 
             ".mainloop   -> function\r\n" + 
             ".obj        -> dictionary of {}:\r\n".format(len(self.obj)) + 
             "    [personaggio] -> list of {}\r\n".format(len(self.obj["personaggio"])) + 
             "    [oggetto]     -> list of {}\r\n".format(len(self.obj["oggetto"])) + 
             "    [ostacolo]    -> list of {}\r\n".format(len(self.obj["ostacolo"])) + 
             "    [volante]     -> list of {}\r\n".format(len(self.obj["volante"])) + 
             "    [pavimento]   -> list of {}\r\n".format(len(self.obj["pavimento"])) + 
             "    [menu]        -> list of {}\r\n".format(len(self.obj["menu"]))]
        return a[0]


'''
5) CLASSE SCREEN
'''
class Screen():
    '''Crea l'oggetto 'Screen' che contiene il titolo della finestra di gioco 
    e la surface principale dove renderizzare 'Window' ('.set_mode').'''
    def __init__(self, title, size):
        self.set_mode = pygame.display.set_mode(size)  # creazione della finestra
        self.set_mode.fill(sys.modules[__name__].GRAY) # background di default
        self.size = list(size)                         # dimansioni della finestra
        self.title = pygame.display.set_caption(title) # titolo della finestra
    
    # Cosa restituisce quando usi la funzione 'str'
    def __str__(self):
        a = ["<class 'GameToolKit.Screen'>:\r\n" + 
             "    .set_mode -> pygame.display.set_mode\r\n" + 
             "    .title    -> pygame.display.set_caption\r\n" + 
             "    .size     -> list of 2:\r\n" + 
             "        [0] width  -> {}\r\n".format(self.size[0]) + 
             "        [1] height -> {}\r\n".format(self.size[1])]
        return a[0]


'''
6) CLASSE WINDOW
'''
class Window():
    '''In 'Window.surface' verranno incollati tutti gli oggetti prima di essere
    renderizzati in 'GameInit.updateWindow()'.'''
    def __init__(self, size, pos):
        self.surface = pygame.Surface(size)  # Surface
        self.size = list(size)               # dimenzioni della mappa
        self.pos = list(pos)                 # posizione rispetto a 'Screen'
    
    # Muovi finestra
    def MoveWindow(self, delta_pos, screen_size, status_bar_size):
        '''Modifica la posizione relativa dell'oggetto 'Window' rispetto 
        all'oggetto 'Screen' (che sta fisso). 'screen_size' è una tupla che 
        contiene le dimensioni dell'oggetto 'Screen'.'''
        # 'delta_pos' -> tupla che contiene lo spostamento in x e y
        
        # Pulisci lo schermo (necessario solo se le dimensioni della 
        # finestra sono più piccole di quello dello schermo)
        # self.screen.set_mode.fill(sys.modules[__name__].GRAY)
        # Aggiorna i valori della posizione della finestra
        self.pos[0] += delta_pos[0]
        self.pos[1] += delta_pos[1]
        
        # Fai i controlli della posizione della finestra:
        for i in [0, 1]: # -> 0 = X; 1 = Y
            # X/Y > 0
            if self.pos[i] > i * status_bar_size[1]:  # self.pos[i] > 0
                self.pos[i] = i * status_bar_size[1]  # self.pos[i] = 0
            # X/Y < di tot
            if self.pos[i] < screen_size[i] - self.size[i]:
                self.pos[i] = screen_size[i] - self.size[i]
    
    def render(self, screen):
        '''Renderizza 'Window' in 'Screen'.'''
        screen.set_mode.blit(self.surface, self.pos)
    
    # Cosa restituisce quando usi la funzione 'str'
    def __str__(self):
        a = ["<class 'GameToolKit.Window'>:\r\n" + 
             "    .surface -> pygame.Surface\r\n" + 
             "    .size    -> list of 2:\r\n" + 
             "        [0] width  -> {}\r\n".format(self.size[0]) + 
             "        [1] height -> {}\r\n".format(self.size[1]) + 
             "    .pos     -> list of 2:\r\n" + 
             "        [0] posx -> {}\r\n".format(self.pos[0]) + 
             "        [1] posy -> {}\r\n".format(self.pos[1])]
        return a[0]


'''
7) CLASSE STATUSBAR
'''
class StatusBar():
    def __init__(self, size, pos = (0, 0)):
        '''Root deve essere un oggetto 'GameInit'. .size[0] dipende dalla 
        dimensione dello schermo 'root.screen.size[0]'. 'BarStatus' viene 
        rappresentato in 'Window.surface' dalla funzione 'GameInit.updateWindow', 
        che richiama 'BarStatus.updateBar'. La barra di stato viene rappresentata
        in alto.'''
        # Posizione della barra di stato in 'Window':
        self.pos = list(pos)        # posizione nella window [X, Y]
        self.size = list(size)      # dimensione della barra
        self.surface = pygame.Surface(size)  # Surface
        self.string = "Monete: %d"  # cosa viene scritto nella barra
        self.bg = (0, 0, 0)         # colore di background (NERO)
        self.text = GameString(     # scritta
                self.string, pos = [20, 5], bg = self.bg)
    
    def updateBar(self, root):
        '''Prende come argomento un oggetto 'GameInit' e rappresenta la 
        barra di stato nella finestra.'''
        # Pulisci la surface
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.bg)
        # Reimposta il valore della stringa con il numero di monete prese
        self.text.set_string(self.string % root.obj["personaggio"][0].coins)
        self.text.render(self.surface)  # renderizza la scritta
        # Rappresenta la barra nella finestra
        root.screen.set_mode.blit(self.surface, self.pos)
    
    def __str__(self):
         a = ["<class 'GameToolKit.StatusBar'>:\r\n" + 
             "    .surface -> pygame.Surface\r\n" + 
             "    .size    -> list of 2:\r\n" + 
             "        [0] width  -> {}\r\n".format(self.size[0]) + 
             "        [1] height -> {}\r\n".format(self.size[1]) + 
             "    .pos     -> list of 2:\r\n" + 
             "        [0] posx -> {}\r\n".format(self.pos[0]) + 
             "        [1] posy -> {}\r\n".format(self.pos[1]) + 
             "    .text    -> {}".format(str(self.text)) + 
             "    .string  -> {}\r\n".format(self.string) + 
             "    .bg      -> {}\r\n".format(self.bg)]
         return a[0]


'''
8) CLASSE PERSONAGGIO
'''
class Personaggio():
    '''Questa è la classe per il Personaggio giocabile. Viene aggiunto a 
    'GameInit' con la funzione 'GameInit.OBJadd()'. Il personaggio viene 
    rappresentato sullo schermo se '.status' = True (opzione di default).'''
    def __init__(self, path, ritaglio, pos, size, speed, pl = 20, 
                 pv = 40, tipo = ''):
        # Inizializza tutti gli attributi dell'oggetto 'Personaggio'
        self.status = True        # True = rappresenta in window
        self.type = tipo          # tipo di personaggio
        self.coins = 0            # Numero di monete raccolte
        self.path = path          # path della sprite
        self.chrono = 0           # conta il numero di loop trascorsi
        self.fun = lambda: _Void()# funzione associata al personaggio
        self.ritaglio = list(ritaglio)  # (x, y, w, h) del ritaglio di 'image'
                                        # solo dell'immagine in alto a sinistra.
        self.pl = pl              # penetrabilità laterale (in pixel)
        self.pv = pv              # penetrabilità verticale (in pixel)
        self.__w = size[0]        # larghezza
        self.__h = size[1]        # altezza
        self.x = pos[0]           # posizione x in window
        self.y = pos[1]           # posizione y in window
        if len(pos) > 2:
            self.z = pos[2]       # posizione in z
        else:
            self.z = 0
        self.xchange = 0          # spostamento lungo x (moltiplica con xspeed)
        self.ychange = 0          # spostamento lungo y (moltiplica con yspeed)
        self.xspeed = speed[0]    # velocità lungo x
        self.yspeed = speed[1]    # velocità lungo y
        
        # Crea l'immagine che viene rappresentata nalla window
        imageAll = pygame.image.load(path).convert_alpha()
        
        # Inizializza image_list
        self.image_dict = {"down": [], "left": [], "right": [], "up": []}
        
        row = 0
        # Ritaglia l'immagine
        for i in self.image_dict.keys():
            col_list = []
            for col in range(3):
                w = self.ritaglio[2]
                x = self.ritaglio[0] + w * col
                h = self.ritaglio[3]
                y = self.ritaglio[1] + h * row
                new_image = imageAll.subsurface(x, y, w, h)
                new_image = pygame.transform.scale(new_image, size)
                col_list.append(new_image)
            new_image = imageAll.subsurface(x - w, y, w, h)
            new_image = pygame.transform.scale(new_image, size)
            col_list.append(new_image)
            self.image_dict[i] = col_list # aggiorna il dizionario con la nuova riga
            row += 1 # passa alla prossima riga
        
        # Prendi l'immagine di default
        self.image = self.image_dict["down"][1]  # frontale
        # Ridimensiona l'immagine
        # self.image = pygame.transform.scale(self.image, size)
        self.OLDdirection = "down"
    
    @property
    def w(self):
        '''Largezza dell''oggetto da renderizzare.'''
        return self.__w
    @w.setter
    def w(self, new):
        '''Mantiene le proporzioni con self.__h.'''
        prop = self.__h / self.__w
        self.__w = new
        self.__h = new * prop
    
    @property
    def h(self):
        '''Altezza dell''oggetto da renderizzare.'''
        return self.__h
    @h.setter
    def h(self, new):
        '''Mantiene le proporzioni con self.__w.'''
        prop = self.__w / self.__h
        self.__h = new
        self.__w = new * prop
    
    def get_render_rect(self):
        '''Restituisce il pygame.Rect dell'oggetto da renderizzare. Usa invece 
        il  metodo '.get_collision_rect' per verificare le collisioni.'''
        return pygame.Rect([self.x, self.y - self.z], [self.w, self.h])
    
    def get_collision_rect(self):
        '''Restituisce il pygame.Rect dell'oggetto per le collisioni. Usa invece 
        il  metodo '.get_render_rect' per la renderizzazione dell'icona.'''
        return pygame.Rect([self.x + self.pl, self.y - self.pv], 
                           [self.w - 2 * self.pl, self.h - self.pv])
    
    def resize(self, w = None, h = None):
        '''Modifica le proporzioni della surface.'''
        if w == None:
            w = self.w
        if h == None:
            h = self.h
        fun = self.fun
        self.__init__(self.path, self.ritaglio, (self.x, self.y), (w, h), 
                      (self.xspeed, self.yspeed), pl = self.pl, pv = self.pv, 
                      tipo = self.type)
        self.fun = fun
    
    def render(self, surf, pos = None):
        '''Renderizza il 'Personaggio' in una 'Surface'.'''
        if pos == None:
            pos = self.get_render_rect()#(self.x, self.y)
        surf.blit(self.image, pos)
    
    def __str__(self):
        a = ["<class 'GameToolKit.Personaggio'>:\r\n\r\n" + 
             ".status       -> logical: {}\r\n".format(self.status) + 
             ".type         -> {}: {}\r\n".format(type(self.type), self.type) + 
             ".chrono       -> {}: {}\r\n".format(type(self.chrono), self.chrono) + 
             ".fun          -> funzione\r\n" + 
             ".image        -> pygame.Surface\r\n" + 
             ".image_dict   -> dictionary of 4:\r\n" + 
             "    [down]  -> list of 3 pygame.Surface\r\n" + 
             "    [left]  -> list of 3 pygame.Surface\r\n" + 
             "    [right] -> list of 3 pygame.Surface\r\n" + 
             "    [up]    -> list of 3 pygame.Surface\r\n" + 
             ".OLDdirection -> string: {}\r\n".format(self.OLDdirection) +
             '.path         -> {}: "{}"\r\n'.format(type(self.path), self.path) + 
             ".ritaglio     -> list of 4:\r\n" + 
             "    [0] x -> {}\r\n".format(self.ritaglio[0]) + 
             "    [1] y -> {}\r\n".format(self.ritaglio[1]) + 
             "    [2] w -> {}\r\n".format(self.ritaglio[2]) + 
             "    [3] h -> {}\r\n".format(self.ritaglio[3]) + 
             ".x            -> {}: {}\r\n".format(type(self.x), str(self.x)) + 
             ".y            -> {}: {}\r\n".format(type(self.y), str(self.y)) + 
             ".z            -> {}: {}\r\n".format(type(self.z), str(self.z)) + 
             ".w            -> {}: {}\r\n".format(type(self.w), str(self.w)) + 
             ".h            -> {}: {}\r\n".format(type(self.h), str(self.h)) + 
             ".xchange      -> {}: {}\r\n".format(type(self.xchange), 
                           str(self.xchange)) + 
                           ".ychange      -> {}: {}\r\n".format(type(self.ychange), 
                                         str(self.ychange))]
        b = [".xspeed       -> {}: {}\r\n".format(type(self.xspeed), 
             str(self.xspeed)) + 
            ".yspeed       -> {}: {}\r\n".format(type(self.yspeed), 
                          str(self.yspeed)) + 
             ".pl           -> {}: {}\r\n".format(type(self.pl), str(self.pl)) + 
             ".pv           -> {}: {}\r\n".format(type(self.pv), str(self.pv))]
        return a[0] + b[0]


'''
9) CLASSE OGGETTO
'''
class Oggetto():
    '''Crea un Oggetto che può essere aggiunto all'oggetto 'GameInit' con 
    'GameInit.OBJadd()'. L'oggetto sarà rappresentato nello schermo se avrà 
    l'attributo '.status' = True (opzione di default).'''
    def __init__(self, path, ritaglio, pos, size, tipo, status = True, pl = 0, 
                 pv = 0, nFrames = 1, z = 0):
        # Inizializza tutti gli attributi dell'oggetto 'Oggetto'
        self.status = status       # True = rappresenta in window
        self.collided = False      # True = l'oggetto è stato colpito
        self.path = path           # path della sprite
        self.fun = lambda: _Void() # funzione associata all'oggetto
        self.chrono = 0            # conta il numero di loop trascorsi
        self.type = tipo           # tipo di oggetto (es. coin, arma, ...)
        self.ritaglio = ritaglio   # (x, y, w, h) del ritaglio di 'image'
        self.pl = pl               # penetrabilità laterale (in pixel)
        self.pv = pv               # penetrabilità verticale (in pixel)
        self.__w = size[0]         # larghezza
        self.__h = size[1]         # altezza
        self.x = pos[0]            # posizione x in window
        self.y = pos[1]            # posizione y in window
        if len(pos) > 2:
            self.z = pos[2]        # posizione in z
        else:
            self.z = 0
        self.image_list = []       # contiene la lista dei frame dell'oggetto
        
        # Crea l'immagine che viene rappresentata nalla window
        self.image = self.cutImage(nFrames)  # contiene l'immagine rappresentata
                                             # in window.
    
    # Ritaglia le immagini per l'animazione di oggetti.
    # Crea una lista di immagini.
    def cutImage(self, nFrames):
        '''Ritaglia le immagini per l'animazione di oggetti. Crea una lista di 
        immagini che andranno a comporre l'attributo '.image_list'.'''
        # Crea l'immagine che viene rappresentata nalla window
        imageAll = pygame.image.load(self.path).convert_alpha()
        
        # Inizializza image_list
        self.image_list = []
        
        for col in range(nFrames):
            w = self.ritaglio[2]
            x = self.ritaglio[0] + w * col
            h = self.ritaglio[3]
            y = self.ritaglio[1]
            # ritaglia l'immagine
            new_image = imageAll.subsurface(x, y, w, h)
            # ridimrnsiona l'immagine
            new_image = pygame.transform.scale(new_image, (int(self.w), int(self.h)))
            # aggiorna la lista con la nuova immagine
            self.image_list.append(new_image)
        
        # Prendi l'immagine di default
        return self.image_list[0]  # la prima
    
    @property
    def w(self):
        '''Largezza dell''oggetto da renderizzare.'''
        return self.__w
    @w.setter
    def w(self, new):
        '''Mantiene le proporzioni con self.__h.'''
        prop = self.__h / self.__w
        self.__w = new
        self.__h = new * prop
        self.updateImages((self.__w, self.__h))
    
    @property
    def h(self):
        '''Altezza dell''oggetto da renderizzare.'''
        return self.__h
    @h.setter
    def h(self, new):
        '''Mantiene le proporzioni con self.__w.'''
        prop = self.__w / self.__h
        self.__h = new
        self.__w = new * prop
        self.updateImages((self.__w, self.__h))
    
    def updateImages(self, size):
        for i in self.image_list:
            i = pygame.transform.scale(i, (int(self.w), int(self.h)))
        self.image = pygame.transform.scale(self.image, (int(self.w), int(self.h)))
    
    def get_render_rect(self):
        '''Restituisce il pygame.Rect dell'oggetto da renderizzare. Usa invece 
        il  metodo '.get_collision_rect' per verificare le collisioni.'''
        return pygame.Rect([self.x, self.y - self.z], [self.w, self.h])
    
    def get_collision_rect(self):
        '''Restituisce il pygame.Rect dell'oggetto per le collisioni. Usa invece 
        il  metodo '.get_render_rect' per la renderizzazione dell'icona.'''
        return pygame.Rect([self.x + self.pl, self.y - self.pv], 
                           [self.w - 2 * self.pl, self.h - self.pv])
    
    def render(self, surf, pos = None):
        '''Renderizza l'Oggetto in una 'Surface'.'''
        if pos == None:
            pos = self.get_render_rect()#(self.x, self.y)
        surf.blit(self.image, pos)
    
    def __str__(self):
        a = ["<class 'GameToolKit.Oggetto'>:\r\n\r\n" + 
             "    .status     -> logical: {}\r\n".format(self.status) + 
             "    .collided   -> logical: {}\r\n".format(self.collided) + 
             '    .type       -> "{}"\r\n'.format(self.type) + 
             "    .chrono     -> {}: {}\r\n".format(type(self.chrono), self.chrono) + 
             "    .fun        -> funzione: {}\r\n".format(str(self.fun)) + 
             "    .image      -> pygame.Surface\r\n" + 
             "    .image_list -> list of {} pygame.Surface\r\n".format(len(
                     self.image_list)) + 
             '    .path       -> {}: "{}"\r\n'.format(type(self.path), self.path) + 
             "    .ritaglio   -> list of 4:\r\n" + 
             "        [0] x -> {}\r\n".format(self.ritaglio[0]) + 
             "        [1] y -> {}\r\n".format(self.ritaglio[1]) + 
             "        [2] w -> {}\r\n".format(self.ritaglio[2]) + 
             "        [3] h -> {}\r\n".format(self.ritaglio[3]) + 
             "    .x          -> {}: {}\r\n".format(type(self.x), str(self.x)) + 
             "    .y          -> {}: {}\r\n".format(type(self.y), str(self.y)) + 
             "    .z          -> {}: {}\r\n".format(type(self.z), str(self.z)) + 
             "    .w          -> {}: {}\r\n".format(type(self.w), str(self.w)) + 
             "    .h          -> {}: {}\r\n".format(type(self.h), str(self.h)) + 
             "    .pl         -> {}: {}\r\n".format(type(self.pl), str(self.pl)) + 
             "    .pv         -> {}: {}\r\n".format(type(self.pv), str(self.pv))]
        return a[0]


'''
10) CLASSE GAMESTRING
'''
class GameString():
    '''Crea un oggetto 'testo' facile da modificare e renderizzare. Bisogna 
    passare la 'stringa' che contiene il testo da proiettare.'''
    def __init__(self, string, pos = [0, 0], bg = (128, 128, 128), 
                 textcolor = (255, 255, 255), fontname = 'Comic Sans MS', 
                 fontsize = 16, rotation = 0):
        self.string = string     # contiene il testo
        self.pos = list(pos)     # posizione in '.master' del testo
        self.bg = list(bg)       # colore di background
        self.rotation = rotation # rotazione della scritta
        self.textcolor = list(textcolor)  # colore del testo
        self.set_font(fontname = 'Comic Sans MS', fontsize = fontsize, 
                      color = self.textcolor)
    
    def set_font(self, fontname = 'Comic Sans MS', fontsize = 16, 
                 color = (255, 255, 255)):
        '''Modifica il font della scritta dell'oggetto 'GameString'. Imposta:
            -> GameString._font (font della scritta)
            -> GameString.textcolor (colore della scritta)'''
        self._font = pygame.freetype.SysFont(fontname, fontsize)
        self.textcolor = color
    
    def set_string(self, string):
        '''Modifica la stringa che viene rappresentata nella casella di testo.'''
        self.string = string
    
    def get_size(self, string = None):
        '''Prende le dimensioni del testo quando viene renderizzato. Usa il metodo 
        '.size' dei pygame.font.Font. Se viene passata una stringa in 'string', 
        ritorna le dimensioni della stringa di testo con la formattazione attuale.'''
        if string == None:
            string = self.string 
        return self._font.get_rect(string)[2:4]
    
    def get_rect(self):
        '''Ricava un oggetto pygame.Rect dal GameString.'''
        return pygame.Rect(self.pos, self.get_size)
    
    def render(self, surf, pos = None, rect = None):
        '''Renderizza la scritta nella Surface 'surf'.'''
        if pos == None:
            pos = self.pos
        if rect == None:
            rect = pygame.Rect(pos, self.get_size())
        # Renderizza il font in '.master'
        self._font.render_to(surf, rect, self.string, self.textcolor, 
                             rotation = self.rotation, bgcolor = self.bg)
    
    def move(self, deltax, deltay):
        '''Modifica la posizione della scritta all'interno della Surface 
        '.master' aggiungendo a '.pos' il delta-x e delta-y.'''
        self.pos[0] += deltax  # Aggiunge delta-x alla posizione
        self.pos[1] += deltay  # Aggiunge delta-y alla posizione
    
    def __str__(self):
        a = ["<class 'GameInit.GameString'>:\r\n" + 
             "        .string    -> {}\r\n".format(self.string) + 
             "        .pos       -> list of 2:\r\n" + 
             "            [0] x -> {}\r\n".format(self.pos[0]) + 
             "            [0] y -> {}\r\n".format(self.pos[1]) + 
             "        .bg        -> {}\r\n".format(self.bg) + 
             "        .textcolor -> {}\r\n".format(self.textcolor) + 
             "        .rotation  -> {}\r\n".format(self.rotation) + 
             "        ._font     -> {}\r\n".format(type(self._font))]
        return a[0]

'''
11) CLASSE RESPONCEBOX
'''
class ResponceBox():
    '''Crea una finestra che contiene una sequenza di risposte. Il puntatore 
    può muoversi dalla prima risposta (quando '.current' = 0) alla seconda 
    (quando '.current' = 1), e così via. Gli elementi di 'args' devono essere 
    delle liste del tipo di quelle create con 'GameToolKit.truncString2List', 
    che contengono stringhe, oppure oggetti GameToolKit.Personaggio, 
    GameToolkit.Oggetto, GameToolkit.ResponceBox, GameToolKit.GameString o 
    pygame.Surface.
    
    NOTA: gli 'args' vanno passati con la seguente struttura:
        cella1[riga1[oggetto], riga2[oggetto], ...], cella2[[], [], ...]
    'GameToolKit.truncString2List' formatta una stringa per trasformarla in cella.
    Se si vuole passare un'icona con un testo, passare una cosa del tipo:
        cella[riga[GameToolkit.ResponceBox]]
    oppure:
        cella[riga1[GameToolkit.Oggetto], riga2[GameToolKit.GameString]]
    
    ALTRI PARAMETRI:
    'size' è una tupla che contiene la dimensione del box (x, y).
    'bg' è il colore di background (di default, bianco).
    'textcolor' è una tupla di interi da 0 a 255 che rappresenta il colore (RBG) 
    del testo.
    'cursor' = True se si vuole rappresentare il cursore sul testo.
    'fontsize' è un intero che rappresenta la dimansione del font del testo. 
    'fontname' è il nome del font (vedi pygame.freetype.SysFont).
    'padx' e 'pady' sono distanza (in pixel) del testo dai bordi del box.
    'edgeWidth' è lo spessore in pixel della cornice del box.
    'edgeColor' è il colore della cornice del box (nero di default).
    'cursorColor' è il colore del cursore (nero di default).
    'inline' è l'interlinea da lasciare tra una riga di testo e un'altra (di 
    default, viene calcolata del 'fontsize').
    'disposition' indica se le celle di testo devono essere disposte verticalmente 
    (default, 'v'), orizzontalmente ('h') o a matrice ('nxm') [vedi '.dispose'].
    'mode' stabilisce come si deve comportare la ResponceBox quando riceve un 
    comando dal mouse. I valori ammessi sono:
        active -> (default) il cursore è sempre visibile;
        sleep  -> il cursore viene disattivato se il mouse viene cliccato fuori 
                  dal box;
        static -> il corsore non viene mai visualizzato.'''
    def __init__(self, size, *args, current = 0, bg = (255, 255, 255), 
                 textcolor = (0, 0, 0), cursor = True, fontsize = 16, 
                 fontname = 'Comic Sans MS', padx = 5, pady = 5, edgeWidth = 5, 
                 edgeColor = (0, 0, 0), cursorColor = (0, 0, 0), inline = None, 
                 singleCursor = False, disposition = 'vertical', mode = 'active'):
        self.__ans = args           # lista delle celle di testo
        self.__size = size          # dimensioni del box
        self.__current = current    # valore scelto
        self.__mode = mode          # comportamento del cursore in risposta ai click
        self.bg = bg                # colore di background
        self.textcolor = textcolor  # colore del testo
        self.fontsize = fontsize    # dimensioni del font
        self.fontname = fontname    # tipo di font
        self.edgeWidth = edgeWidth  # spessore del bordo
        self.edgeColor = edgeColor  # colore del bordo
        self.cursorColor = cursorColor # colore del cursore
        if inline == None:
            inline = fontsize + 2
        self.inline = inline        # interlinea
        self.padx = padx            # spaziatura da sinistra
        self.pady = pady            # spaziatura dall'alto
        self.__cursor = cursor      # 'True' se il cursore viene rappresentato
        self.__disp = disposition   # disposizione delle celle di testo
        
        # Surface del cursore
        self.cursor_surface = self.updateCursor()
        # Crea la surface principale del box
        self.surface = self.updateSurface()
        # Disponi le celle di testo
        self.dispose()
    
    @property
    def ans(self):
        '''Lista dove ogni elemento è una lista che contiene i testi delle celle.'''
        return self.__ans
    @ans.setter
    def ans(self, new):
        self.__ans = new
        self.updateAll()
    
    @property
    def size(self):
        '''Dimensioni della finestra (x, y).'''
        return self.__size
    @size.setter
    def size(self, new):
        self.__size = new
        self.updateAll()
    
    @property
    def disp(self):
        '''Disposizione delle caselle di testo ('vertical', 'horizontal' or 'nxm').'''
        return self.__disp
    @disp.setter
    def disp(self, new):
        self.__disp = new
        self.updateAll()
    
    @property
    def cursor(self):
        '''Logical che vale True se il cursore deve essere rappresentato, altrimenti 
        vale False.'''
        return self.__cursor
    @cursor.setter
    def cursor(self, logic):
        self.__cursor = True if logic else False
        self.updateCursor()
    
    @property
    def current(self):
        '''Cella attualmente selezionata.'''
        return self.__current
    @current.setter
    def current(self, new):
        self.__current = new
        self.updateAll()
    
    @property
    def mode(self):
        '''Comportamento del cursore in risposta ai click del mouse. Può avere 
        i seguenti valori: 'active' (default, il cursore è sempre visualizzato); 
        'sleep' (il cursore è visualizzato solo se si clicca all'interno del box);
        'static' (il cursore non viene mai visualizzato).'''
        return self.__mode
    @mode.setter
    def mode(self, new):
        accepted_values = ('active', 'sleep', 'static')
        if new in accepted_values:
            self.__mode = new
            self.updateCursor()
        else:
            raise ValueError(f'"mode" deve essere uno dei seguenti: {accepted_values}')
    
    @property
    def n_ans(self):
        '''Numero di risposte.'''
        return len(self.ans)
    
    @property
    def cellSize(self):
        '''Prende le dimensioni della singla cella di testo. Questo è anche la 
        dimensione del cursore.'''
        x, y = self.cellNumber
        return ((self.size[0] - 2 * (self.edgeWidth)) / x,     # width
                    (self.size[1] - 2 * (self.edgeWidth)) / y) # height
    
    @property
    def cellNumber(self):
        '''Restituisce una tupla con il numero di celle ti testo (x, y).'''
        if self.disp in ('h', 'horizontal'):
            x = self.n_ans
            y = 1
        elif self.disp in ('v', 'vertical'):
            x = 1
            y = self.n_ans
        else:
            x, y = self.disp.split('x')
        return int(x), int(y)
    
    def updateSurface(self):
        '''Aggiorna la surface se vengono apportate modifiche ai testi o alla 
        disposizione.'''
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.edgeColor)
        self.surface.fill(self.bg, rect = (self.edgeWidth, self.edgeWidth, \
             self.size[0] - 2 * self.edgeWidth, self.size[1] - 2 * self.edgeWidth))
        self.dispose()
        return self.surface
    
    def updateCursor(self):
        '''Aggiorna la surface del cursore se il numero di celle o la loro 
        dimensione viene modificata.'''
        # Surface del cursore
        self.cursor_surface = pygame.Surface(self.cellSize)
        self.cursor_surface.fill(self.cursorColor)
        # Crea trasparenza del cursore
        if self.cursor and self.mode != 'static':
            self.cursor_surface.set_alpha(100)
        else:
            self.cursor_surface.set_alpha(0) # Trasparente
        return self.cursor_surface
    
    def updateAll(self):
        '''Aggiorna la sia la surface che il cursore.'''
        self.updateSurface()
        self.updateCursor()
    
    def dispose(self):
        '''Imposta la disposizione delle celle di testo e li renderizza nella 
        surface. I valori di 'self.disp' concessi sono: 
            vertical | v   -> disposizione verticale (default)
            horizontal | h -> disposizione orizzontale
            nxm            -> n: numero di righe; m: numero di colonne
        NOTA: prende il valore da 'self.disp'.'''
        # Numero di celle di testo in x e in y
        x, y = self.cellNumber
        idx_ans = 0  # indice in 'self.ans'
        for i in range(y):      # colonne della matrice di celle di testo
            for j in range(x):  # righe della matrice di celle di testo
                if idx_ans < self.n_ans:
                    cellSurface = pygame.Surface((int(self.cellSize[0] - self.padx), 
                                                  int(self.cellSize[1] - self.pady)))
                    cellSurface.fill(self.bg)
                    cellPos = [self.edgeWidth + self.padx + j * self.cellSize[0], 
                               self.edgeWidth + self.pady + i * self.cellSize[1]]
                    # Scrivi linea per linea
                    if isinstance(self.ans[idx_ans], list):
                        for line, t in enumerate(self.ans[idx_ans]):
                            pos = [0, line * self.inline]
                            if isinstance(t, str):
                                txt = GameString(t, pos = pos, bg = self.bg, \
                                        textcolor = self.textcolor, fontsize = \
                                        self.fontsize, fontname = self.fontname)
                                txt.render(cellSurface)
                            elif isinstance(t, pygame.Surface):
                                cellSurface.blit(t, pos)
                            elif isinstance(t, (ResponceBox, GameString, Personaggio, 
                                                Oggetto)):
                                t.render(cellSurface, pos)
                    self.surface.blit(cellSurface, cellPos)
                idx_ans += 1 # vai alla prossima cella di testo
    
    def render(self, surf, pos):
        '''Renderizza il box nella 'pygame.Surface' ('surf') nella posizione in 
        'pos' (x, y).'''
        # Renderizza la surface
        surf.blit(self.surface, pos)
        # Renderizza il cursore
        if self.mode != 'static':
            surf.blit(self.cursor_surface, [pos[0] + self.cursor_pos[0], pos[1] + 
                                            self.cursor_pos[1]])
    
    def get_rect(self, pos = (0, 0)):
        '''Restituisce il pygame.Rect. Di default, la posizione viene posta a 
        (0, 0), ma può essere cambiata con l'argomento 'pos'.'''
        return pygame.Rect(pos, self.size)
    
    def get_responces(self):
        '''Restituisce una lista nidificata che contiene tutti i valori di 
        .current per se stessa e per le ResponceBox più interne.
        NOTA:il primo valore è la risposta selezionata nella ResonceBox più 
        esterna, mentre quelle a mano a mano più interne sono scansionate per 
        celle, da sinistra verso destra e dall'alto verso il basso.
        
        ESEMPIO di risultato:
            [0]  -> se unica ResponceBox
            
            [9, [0], [1, [3]]] -> se nidificata'''
        out = [self.current]
        def recursion(ans, counter):
            if isinstance(ans, (list, tuple)):
                for a in ans:
                    counter = recursion(a, counter)
            if isinstance(ans, ResponceBox):
                counter += [ans.get_responces()]
            return counter
        for ans in self.ans:
            out = recursion(ans, out)
        return out
    
    def cursorMove(self, direction):
        '''Modifica 'self.current' e la posizione del cursore a seconda del valore 
        di 'direction' (è una tupla che indica di quanto ti sposti in x e y nella 
        matrice delle celle di testo). Se la disposizione delle celle è verticale 
        o orizzontale, basta passare un intero.'''
        # Numero di celle i x e y
        nX, nY = self.cellNumber
        # Posizione del cursore
        posx, posy = (self.current % nX, self.current // nX)
        if isinstance(direction, (tuple, list)):
            if direction[0]: # spostamento in x
                posx += direction[0]
                posx %= nX
            if direction[1]: # spostamento in y
                posy += direction[1]
                posy %= nY
        if isinstance(direction, (int, float)):
            if nX == 1:
                posx += int(direction)
                posx %= nX
            if nY == 1:
                posy += int(direction)
                posy %= nY
        # Aggiusta il valore corrente
        self.current = posy * nX + posx
    
    @property
    def cursor_pos(self):
        '''Posizione del cursore nella box (x, y). Calcolato con 'self.current' 
        e 'self.disp'.'''
        # Numero di celle i x e y
        nX,nY = self.cellNumber
        return (self.edgeWidth + (self.current % nX) * self.cellSize[0], 
                self.edgeWidth + ((self.current // nX) % nY) * self.cellSize[1])
    
    def mousePress(self, pos, button):
        '''Prende come input la posizione relativa del mouse ('pos') e il pulsante 
        premuto (vedi pygame.MOUSEBUTTONDOWN). Modifica '.current' in base a dove 
        ho premuto il mouse.'''
        if button == 1: # pulsante sinistro del mouse
            nX, nY = self.cellNumber
            cellW, cellH = self.cellSize
            # Togli il bordo per rendere i calcoli successivi più facili
            posx, posy = [pos[0] - self.edgeWidth, pos[1] - self.edgeWidth]
            if (posx < 0 or posx > cellW * nX) or (posy < 0 or posy > cellH * nY):
                # Fuori dei bordi
                if self.mode == 'sleep':
                    self.current = -1
                    self.cursor = False
                # parsa tutte le celle
                for i, ans in enumerate(self.ans):
                    # Se nella cella selezionata l'oggetto è ResponceBox, lancia il 
                    # mousePress della cella
                    if i < self.n_ans:
                        def checkResponceBox(item, parent, current, numLine):
                            if isinstance(item, list):
                                for numLine, i in enumerate(item):
                                    checkResponceBox(i, parent, current, numLine)
                            elif isinstance(item, ResponceBox):
                                #item.cursor = True
                                item.mousePress([-1, -1], 1)
                        checkResponceBox(ans, self, i, 0)
            else:
                self.cursor = True
                # Modifica '.current'
                currentx = min([posx // cellW, nX - 1])
                currenty = min([posy // cellH, nY - 1])
                # Aggiusta il valore corrente
                self.current = int(currenty * nX + currentx)
                # parsa tutte le celle
                for i, ans in enumerate(self.ans):
                    # Se nella cella selezionata l'oggetto è ResponceBox, lancia il 
                    # mousePress della cella
                    if i < self.n_ans:
                        def checkResponceBox(item, parent, current, numLine):
                            if isinstance(item, list):
                                for numLine, i in enumerate(item):
                                    checkResponceBox(i, parent, current, numLine)
                            elif isinstance(item, ResponceBox):
                                item.mousePress(\
                                        [posx - cellW * (current % nX) - parent.padx, 
                                         posy - cellH * ((current // nX) % nY) - 
                                         parent.pady - parent.inline * numLine], 1)
                        checkResponceBox(ans, self, i, 0)
            self.updateAll()

'''
CLASSE GAMEBUTTON
'''
class GameButton(ResponceBox):
    '''Una ResponceBox che attiva direttamente la funzione associata in 'command' 
    quando selezionato con il mouse. In 'arg' può essere passata una lista di 
    argomenti da passare a 'command',  mentre in 'karg' puoi passare un dizionario 
    con i keyword arguments.
    NOTA: per funzionare correttamente, deve essere renderizzato in un'altra 
    ResponceBox con .mousePress() abilitato. Altrimenti bisogna passare alla 
    funzione esplicitamente la posizione relativa del mouse dopo il click.'''
    def __init__(self, size, *args, master = None, command = None, arg = None, 
                 karg = None, **kargs):
        super().__init__(size, *args, **kargs)
        self.__mode = 'active'     # il cursore deve essere abilitato
        self.__cursor = False      # il cursore deve essere invisibile
        # funzione che lancia il pulsante
        if command:
            self.command = lambda: command(*arg, **karg)
        else:
            self.command = lambda: print('click!')
        self.__result = None       # risultato della funzione lanciata
    
    @property
    def result(self):
        '''Memorizza eventuali risultati della funzione '.command'.'''
        return self.__result
    
    def mousePress(self, pos, button):
        if button == 1: # pulsante sinistro del mouse
            nX, nY = self.cellNumber
            cellW, cellH = self.cellSize
            # Togli il bordo per rendere i calcoli successivi più facili
            posx, posy = [pos[0] - self.edgeWidth, pos[1] - self.edgeWidth]
            if (posx < 0 or posx > cellW * nX) or (posy < 0 or posy > cellH * nY):
                # Fuori dei bordi
                pass
            else:
                # Lancia la funzione e memorizza il risultato
                self.__result = self.command()
    
    def render(self, surf, pos):
        '''Renderizza il box nella 'pygame.Surface' ('surf') nella posizione in 
        'pos' (x, y).'''
        # Renderizza la surface
        surf.blit(self.surface, pos)
        # Renderizza il cursore
        if self.cursor:
            surf.blit(self.cursor_surface, [pos[0] + self.cursor_pos[0], pos[1] + 
                                            self.cursor_pos[1]])
