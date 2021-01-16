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
        -> questYesNo
        
    4) CLASSE GameInit:
        -> __init__
        -> MainLoop
        -> ReLoop
        -> OBJadd
        -> updateWindow
        -> __str__
        
    5) CLASSE Screen:
        -> __init__
        -> __str__
        
    6) CLASSE Window:
        -> __init__
        -> MoveWindow
        -> render
        -> __str__
    
    7) CLASSE StatusBar:
        -> __init__
        -> updateBar
        -> __str__
        
    8) CLASSE Personaggio:
        -> __init__
        -> render
        -> __str__
        
    9) CLASSE Oggetto:
        -> __init__
        -> cutImage
        -> render
        -> __str__
    
    10) CLASSE GameString:
        -> __init__
        -> set_font
        -> set_string
        -> render
        -> move
        -> __str__
    
    11) CLASSE ResponceBox:
        -> __init__
        -> render
        -> cursorMove
        -> configure

'''

'''
1) IMPORT
'''
import pygame                # Pacchetto standard per videogame in Python
import pygame.freetype       # Per il font delle scritte
import OBJfunctions as objf  # Per le funzioni degli obj e il Menu
import sys                   # Per lavorare con i moduli e pacchetti
#from itertools import chain  # Per calcoli iterativi su dizionari e liste


'''
2) COLORI
'''
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
    un oggetto 'GameInit', 'collider' e 'collided' devono essere oggetti 'Presonaggio'
    o 'Oggetto'. Casi possibili di 'out':
        -> "":   non c'è stata collisione
        -> "1":  collisione da destra
        -> "2":  collisione da sinistra
        -> "3":  collisione dal basso
        -> "4":  collisione dall'alto
        -> "13": collisione dal basso a destra
        -> "14": collisione dall'alto a destra
        -> "23": collisione dal basso a sinistra
        -> "24": collisione dall'alto a sinistra'''
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
    l_txt = s.split('\n')
    list_txt = []
    def handleLimit(s, limit):
        '''Tronca una stringa al limite di caratteri, trasformandola in lista.'''
        list_txt = []   # Inizializza lista di output
        partial_s = ''  # Inizializza stringa parziale
        for w in s.split(' '): # Prendi parola per parola
            len_partial = len(partial_s)
            if len_partial + len(w)  + 1 > limit: # Limite superato
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
        list_txt += handleLimit(i, limit)
    return [s[1:] for s in list_txt if len(s) > 0]

def questYesNo(root, domanda, ans1 = 'No', ans2 = 'Sì', truncQuest = 100, 
               truncAns = 100, QuestBoxSize = None, AnsBoxSize = (94, 56), 
               QuestTextSize = 20, AnsTextSize = 28, QuestPadx = 5, QuestPady = 5, 
               AnsPadx = 5, AnsPady = 10, QuestBg = (255, 255, 255), 
               AnsBg = (255, 255, 255), QuestTextColor = (0, 0, 0), AnsTextColor = 
               (0, 0, 0), current = 0):
    '''Crea una barra dove viene rappresentata la 'domanda'. Si può rispondere 
    'sì' o 'no' alla domanda. Restituisce 0 se è stato risposto 'no', 1 se la 
    risposta è 'sì'. 'domanda' è una stringa (puoi andare a capo con '\n'). 
    'truncQuest' è il limite di caratteri di 'domnda' prima di andare a capo. 
    'truncAns' è il numero di caratteri di 'ans1' e 'ans2' prima di andare a 
    capo. 
    'QuestBoxSize' è la tupla che contiene le dimensioni della finestra che 
    contiene la domada (di default, larghezza pari a quella dello schermo e una 
    altezza pari a 1/6 di quella dello schermo).
    'AnsBoxSize' è la tupla che contiene le dimensioni della finestra che 
    contiene le risposte. 
    'QuestTextSize' è la frandezza del font della domanda; 'AnsTextSize' quello 
    delle risposte.
    'QuestBg' e 'AnsBg' sono il colore di background.
    'current' è la risposta data di default.'''
    # Crea la surface che verrà rappresentata
    if QuestBoxSize == None:
        surf_x, surf_y = root.screen.size[0], root.screen.size[1] / 6
    else:
        surf_x, surf_y = QuestBoxSize
    list_txt = truncString2List(domanda, truncQuest)
    surf = ResponceBox((surf_x, surf_y), list_txt, cursor = False, fontsize = 
                           QuestTextSize, padx = QuestPadx, pady = QuestPady, 
                           bg = QuestBg, textcolor = QuestTextColor)
    
    # Crea il box che contiene le risposte
    ansBox = ResponceBox(AnsBoxSize, truncString2List(ans1, truncAns), 
                             truncString2List(ans2, truncAns), fontsize = AnsTextSize, 
                             padx = AnsPadx, pady = AnsPady, bg = AnsBg, textcolor = 
                             AnsTextColor, current = current)
    
    # Entra nel loop
    while True:
        # Scansiono gli input dello user
        for e in pygame.event.get():
            # Pulsante spinto in basso
            if e.type == pygame.KEYDOWN:
                
                # Pigia pulsante a destra o sinistra
                if e.key == pygame.K_RIGHT:
                    # Modifica il cursore e il valore di ritorno
                    ansBox.cursorMove(1)
                if e.key == pygame.K_LEFT:
                    # Modifica il cursore e il valore di ritorno
                    ansBox.cursorMove(-1)
                
                # Se premi 'Invio'
                if e.key == pygame.K_RETURN:
                    return ansBox.current
        
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
                                            - ansBox.size[0] - 10, -root.window.pos[1] \
                                            + root.screen.size[1] - surf_y - \
                                            ansBox.size[1] - 10))
        root.screen.set_mode.blit(root.window.surface, root.window.pos)
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
                 window_size = (1000, 700), pos_wd = (0, 0), mainloop = _Wait):
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
        self.status_bar = StatusBar([-self.window.pos[0], -self.window.pos[1]], 
                                    [self.screen.size[0], 25])
        
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
                                    self.obj["menu"][0].h / 4)), "puntatore", status = False)
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
                        if e.key == pygame.K_m:
                            # Blocca il movimento del personaggio
                            self.obj["personaggio"][0].xchange = 0
                            self.obj["personaggio"][0].ychange = 0
                            # Apri la funzione del menu
                            objf.menuOpen(self)
                
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
                if self.obj["personaggio"][0].y < self.status_bar.size[1]: # < 0:
                    self.obj["personaggio"][0].y = self.status_bar.size[1] # = 0
                
                # Avvia il main loop
                self.mainloop()
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
        
        # Sporta la finestra
        self.window.MoveWindow((-dx[0], -dy[0]), self.screen.size)
        
        # Aggiungi riga di stato in alto
        self.status_bar.updateBar(self)
        # Rappresenta la finestra nella nuova posizione
        self.window.render(self.screen)
    
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
    def MoveWindow(self, delta_pos, screen_size):
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
            if self.pos[i] > 0:
                self.pos[i] = 0
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
    def __init__(self, pos, size):
        '''Root deve essere un oggetto 'GameInit'. .size[0] dipende dalla 
        dimensione dello schermo 'root.screen.size[0]'. 'BarStatus' viene 
        rappresentato in 'Window.surface' dalla funzione 'GameInit.updateWindow', 
        che richiama 'BarStatus.updateBar'. La barra di stato viene rappresentata
        in alto.'''
        # Posizione della barra di stato in 'Window':
        self.pos = list(pos)        # posizione nella window [X, Y]
        self.size = list(size)      # dimensione della barra
        self.surface = pygame.Surface(size)  # Surface
        self.string = "Monete: {}"  # cosa viene scritto nella barra
        self.bg = (0, 0, 0)         # colore di background (NERO)
        self.text = GameString(     # scritta
                self.string, pos = [20, 5], bg = self.bg)
    
    def updateBar(self, root):
        '''Prende come argomento un oggetto 'GameInit' e rappresenta la 
        barra di stato nella finestra.'''
        # Pulisci la surface
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.bg)
        
        # Ricalcola la posizione della barra rispetto alla window
        self.pos = [-root.window.pos[0], -root.window.pos[1]]
        
        # Reimposta il valore della stringa con il numero di monete prese
        self.text.set_string(self.string.format(root.obj["personaggio"][0].coins))
        self.text.render(self.surface)  # renderizza la scritta
        
        # Rappresenta la barra nella finestra
        root.window.surface.blit(self.surface, self.pos)
    
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
                 pv = 40):
        # Inizializza tutti gli attributi dell'oggetto 'Personaggio'
        self.status = True        # True = rappresenta in window
        self.coins = 0            # Numero di monete raccolte
        self.path = path          # path della sprite
        self.chrono = 0           # conta il numero di loop trascorsi
        self.fun = lambda: _Void()# funzione associata al personaggio
        self.ritaglio = list(ritaglio)  # (x, y, w, h) del ritaglio di 'image'
                                        # solo dell'immagine in alto a sinistra.
        self.pl = pl              # penetrabilità laterale (in pixel)
        self.pv = pv              # penetrabilità verticale (in pixel)
        self.w = size[0]          # larghezza
        self.h = size[1]          # altezza
        self.x = pos[0]           # posizione x in window
        self.y = pos[1]           # posizione y in window
        self.xchange = 0          # spostamento lungo x (moltiplica con xspeed)
        self.ychange = 0          # spostamento lungo y (moltiplica con yspeed)
        self.xspeed = speed[0]    # velocità lungo x
        self.yspeed = speed[1]    # velocità lungo y
        
        # Crea l'immagine che viene rappresentata nalla window
        imageAll = pygame.image.load(path)
        
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
    
    def render(self, surf):
        '''Renderizza il 'Personaggio' in una 'Surface'.'''
        surf.blit(self.image, (self.x, self.y))
    
    def __str__(self):
        a = ["<class 'GameToolKit.Personaggio'>:\r\n\r\n" + 
             ".status       -> logical: {}\r\n".format(self.status) + 
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
                 pv = 0, nFrames = 1):
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
        self.w = size[0]           # larghezza
        self.h = size[1]           # altezza
        self.x = pos[0]            # posizione x in window
        self.y = pos[1]            # posizione y in window
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
        imageAll = pygame.image.load(self.path)
        
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
            new_image = pygame.transform.scale(new_image, (self.w, self.h))
            # aggiorna la lista con la nuova immagine
            self.image_list.append(new_image)
        
        # Prendi l'immagine di default
        return self.image_list[0]  # la prima
    
    def render(self, surf):
        '''Renderizza l'Oggetto in una 'Surface'.'''
        surf.blit(self.image, (self.x, self.y))
    
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
    
    def render(self, surf):
        '''Renderizza la scritta nella Surface 'surf'.'''
        # Renderizza il font in '.master'
        self._font.render_to(surf, self.pos, self.string, self.textcolor, 
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
    '''Crea una finestra che contiene a sinistra la risposta 1 ('ans1') e a 
    destra la risposta 2 ('ans2'). Il puntatore può muoversi da 'ans1' (quando 
    '.current' = 0) a 'ans2' (quando '.current' = 1). 'ans1' e 'ans2' devono 
    essere delle liste del tipo di quelle create con 'OBJfunctions.truncString2List'.
    'size' è la dimensione totale del box. Se 'ans2' non viene dato, crea un 
    unico box. 'size' è una tupla che contiene la dimensione del box (x, y).
    'bg' è il colore di background (di default, bianco).'''
    def __init__(self, size, *args, current = 0, bg = (255, 255, 255), 
                 textcolor = (0, 0, 0), cursor = True, fontsize = 16, 
                 fontname = 'Comic Sans MS', padx = 5, pady = 5, edgeWidth = 5, 
                 inline = None):
        self.ans = args             # colonne di scritte
        self.n_ans = len(self.ans)  # numero di risposte
        self.size = size            # dimensioni del box
        self.current = current      # valore scelto
        self.bg = bg                # colore di background
        self.textcolor = textcolor  # colore del testo
        self.fontsize = fontsize    # dimensioni del font
        self.fontname = fontname    # tipo di font
        self.edgeWidth = edgeWidth  # spessore del bordo
        if inline == None:
            inline = fontsize + 2
        self.inline = inline        # interlinea
        self.padx = padx            # spaziatura da sinistra
        self.pady = pady            # spaziatura dall'alto
        self.cursor = cursor        # 'True' se il cursore viene rappresentato
        # Dimmensioni del cursore
        self.cursor_size = ((self.size[0] - 2 * edgeWidth) / self.n_ans, 
                            self.size[1] - 2 * edgeWidth)
        # Posizione del cursore nella box
        self.cursor_pos = (edgeWidth + self.current * self.cursor_size[0], edgeWidth)
        # Surface del cursore
        self.cursor_surface = pygame.Surface(self.cursor_size)
        
        # Crea la surface principale del box
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.bg, rect = (edgeWidth, edgeWidth, self.size[0] - 
                                           2 * edgeWidth, self.size[1] - 2 * edgeWidth))
        
        # Aggiungi ans
        idx_ans = 0    # indice in 'self.ans'
        for a in self.ans:
            idx = 0
            # Crea il testo
            for t in a:
                txt = GameString(t, pos = [edgeWidth + padx * (idx_ans + 1) + idx_ans * (
                        self.size[0] - 2 * (edgeWidth + padx)) / self.n_ans, edgeWidth + \
            pady + idx * self.inline], bg = self.bg, textcolor = self.textcolor, \
            fontsize = fontsize, fontname = fontname)
                txt.render(self.surface)
                idx += 1
            idx_ans += 1
        
        # Crea trasparenza del cursore
        if self.cursor:
            self.cursor_surface.set_alpha(100)
        else:
            self.cursor_surface.set_alpha(0) # Trasparente
    
    def render(self, surf, pos):
        '''Renderizza il box nella 'pygame.Surface' ('surf') nella posizione in 
        'pos' (x, y).'''
        # Renderizza la surface
        surf.blit(self.surface, pos)
        
        # Renderizza il cursore
        surf.blit(self.cursor_surface, [pos[0] + self.cursor_pos[0], pos[1] + 
                                self.cursor_pos[1]])
    
    def cursorMove(self, direction):
        '''Modifica 'self.current' e la posizione del cursore a seconda del valore 
        di 'direction' (è un intero che indica di quanto vai avanti o indietro).'''
        self.current += direction
        self.current %= self.n_ans
        
        # Modifica la posizione del cursore
        self.cursor_pos = (self.edgeWidth + self.current * self.cursor_size[0], 
                           self.edgeWidth)
    
    def configure(self, size = None, current = None, bg = None, 
                 textcolor = None, cursor = None, fontsize = None, 
                 fontname = None, padx = None, pady = None, edgeWidth = None, 
                 inline = None):
        if size != None:
            self.size = size
        if current != None:
            self.current = current
        if bg != None:
            self.bg = bg
        if textcolor != None:
            self.textcolor = textcolor
        if cursor != None:
            self.cursor = cursor
        if fontsize != None:
            self.fontsize = fontsize
        if fontname != None:
            self.fontname = fontname
        if padx != None:
            self.padx = padx
        if pady != None:
            self.pady = pady
        if edgeWidth != None:
            self.edgeWidth = edgeWidth
        if inline != None:
            self.inline = inline
        # Aggiorna la surface della finestra con i nuovi valori
        self.__init__(self.size, *self.ans, current = self.current, bg = 
                      self.bg, textcolor = self.textcolor, cursor = self.cursor, 
                      fontsize = self.fontsize, fontname = self.fontname, padx = 
                      self.padx, pady = self.pady, edgeWidth = self.edgeWidth, 
                      inline = self.inline)
