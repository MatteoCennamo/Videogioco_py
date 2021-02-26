# -*- coding: utf-8 -*-
'''
Questo pacchetto contiene tutte le funzioni degli oggetti in 
'GameToolKit.GameInit.obj'.

INDICE:
    
    1) IMPORT
    
    2) FUNZIONI DI COLLISIONE:
        -> collinionObstacles
        -> collisionCoins
    
    3) FUNZIONI DI ANIMAZIONE:
        -> playerAnimation
        -> collisionAnimationObj
    
    4) FUNZIONI DEL MENU
        -> menuSalva
        -> menuOggetti
        -> menuOpen
        
'''

'''
1) IMPORT
'''
# Importa i pacchetti
import pygame
import GameToolKit as gtk


'''
2) FUNZIONI DI COLLISIONE
'''
def _Void(root = None, obj = None):
    return root, obj

def collinionObstacles(root = None, obj = None):
    '''Funzione associata a oggetti impenetrabili per il personaggio.'''
    if obj.status:  # se è visibile
        # Verifica la collisione
        out = gtk.collisionDetection(root, root.obj["personaggio"][0], obj)
        # 'out' = '' se non c'è stata collisione
        if len(out) > 0:   # c'è stata collisione
            done = False
            # Collided = True
            obj.collided = True
            if "1" in out: # collisione da destra
                root.obj["personaggio"][0].x = obj.x + obj.w - obj.pl
                done = True
            if "2" in out: # collisione da sinistra
                root.obj["personaggio"][0].x = (obj.x - 
                        root.obj["personaggio"][0].w + obj.pl)
                done = True
            if ("3" in out) and (not done): # collisione dal basso
                root.obj["personaggio"][0].y = (obj.y + obj.h -  
                        root.obj["personaggio"][0].pv)
            if ("4" in out) and (not done): # collisione dall'alto
                root.obj["personaggio"][0].y = (obj.y - 
                        root.obj["personaggio"][0].h + obj.pv)
        else:  # non c'è stata collisione
            obj.collided = False
    return root, obj

def collisionCoins(root = None, obj = None):
    '''Funzione associata alla collisione con le monete.'''
    if obj.status == True:
        x = root.obj["personaggio"][0].x
        y = root.obj["personaggio"][0].y
        w = root.obj["personaggio"][0].w
        h = root.obj["personaggio"][0].h
        pl = root.obj["personaggio"][0].pl
        pv = root.obj["personaggio"][0].pv
        # collision detection
        if x + w - pl >= obj.x and x <= obj.x + obj.w - pl:
            if y + h - obj.pv >= obj.y and y <= obj.y + obj.h - pv:
                obj.collided = True
                # Aggiungi uno alle monete raccolte
                root.obj["personaggio"][0].coins += 1
                # Resetta il cronometro per l'animazione 'collisionAnimationObj'
                obj.chrono = 0
        
        #####--- Animazione ---#####
        timeframe = 8
        obj.image = obj.image_list[int(obj.chrono / timeframe) % 
                                   len(obj.image_list)]
        # Animazione in caso di collisione
        collisionAnimationObj(root, obj, 15) # 15 = frame di animazione
        
        # Aggiorna il cronometro
        obj.chrono += 1
    return root, obj


'''
3) FUNZIONI DI ANIMAZIONE
'''
def playerAnimation(root = None, obj = None):
    '''Funzione associata all'animazione del movimento del personaggio.'''
    if obj.xchange == 0 and obj.ychange == 0:  # il personaggio è fermo
        # Prendi l'immagine del personaggio fermo, nella direzione 'OLDdirection'
        obj.image = obj.image_dict[obj.OLDdirection][1]
        obj.chrono = 0  # resetta il cronometro
    else:  # il personaggio è in movimento
        timeframe = 3 # 8   # numero di frame prima del cambio immagine
        if obj.ychange < 0: # si sta muovendo verso l'alto
            direction = "up"
        if obj.ychange > 0:
            direction = "down"
        if obj.xchange < 0: # si sta muovendo verso sinistra
            direction = "left"
        if obj.xchange > 0:
            direction = "right"
        # Prendi da 'obj.image_dict' l'immagine corrispondente al movimento 
        # ('up', down', ...) e al cronometro
        obj.image = obj.image_dict[direction][int(obj.chrono / timeframe) % 4]
        # Imposta la vecchia direzione con il valore di quella attuale
        obj.OLDdirection = direction
        # Aggiorna il cronometro
        obj.chrono += 1
    
    return root, obj

def collisionAnimationObj(root, obj, frames):
    '''Funzione che anima gli oggetti quando vengono presi dal personaggio
    (quando 'obj.collided' = True). 'frames' = numero di frame di durata 
    dell'animazione.'''
    # Si attiva solo se l'oggetto è stato colpito.
    # NOTA BENE!: quando l'oggeto viene colpito, il suo cronometro va reimpostato
    # a 0 per permettere l'animazione.
    if obj.collided: #and obj.chrono <= frames:
        if obj.chrono == 0:
            root.obj["oggetto"].remove(obj) # Rimuovi da 'oggetto'
            root.obj["volante"].append(obj) # Aggiungi a 'volante'
        # Imposta trasparenza
        obj.image.set_alpha(255 - int(obj.chrono * 255 / frames))
        # Riposiziona l'oggetto sopra il personaggio, centrato sopra la testa 
        # del personaggio.
        obj.x = root.obj["personaggio"][0].x + (
                root.obj["personaggio"][0].w - obj.w) / 2
        # posiziona 10 pixel soplra il personaggio:
        obj.y = root.obj["personaggio"][0].y - obj.h - 10
        # Ridimensiona l'oggetto
        obj.w += 2
#        obj.h += 2
        obj.image = pygame.transform.scale(obj.image, (int(obj.w), int(obj.h)))
        # Dopo 'frames' numero di frame, l'animazione termina
        if obj.chrono == frames:
            obj.status = False

'''
4) FUNZIONI DEL MENU
'''
def menuSalva(root):
    ans = gtk.multiQuest(root, '''Salvare questo salvataggio?
Sei proprio sicuro?
Va bene...''', "No! Lasciami\nstare!", "Sì, fammi\nsalvare!", 
AnsBoxSize = (150, 168), AnsParams = {'fontsize': 22, 'padx': 10, 'pady': 15})
#    if ans:
#        # Apri il file 'salvataggio'
#        with open('salvataggio.pickle', 'wb') as f:
#            # Sovrascrivi il salvataggio
#            pickle.dump(root.obj, f)

def menuOggetti(root):
    '''Apre il Menu degli oggetti.'''
    ans = gtk.multiQuest(root, '''Seleziona un oggetto.''', "No! Lasciami\nstare!", 
                         "Sì, fammi\nsalvare!", "Più oggetti!", "Un altro", "Ancora!", 
                         "1\n2\n3????????? Ancora", 'Basta', ['Monete:', root.obj['oggetto'][0]], 
                         AnsBoxSize = (560, 450), #truncAns = 12, 
                         AnsParams = {'fontsize': 17, 'padx': 5, 'pady': 10, 
                                      'disposition': '5x4', 'bg': (250, 240, 240)})

 # Apre il Menu principale
def menuOpen(root):
    '''Apre il Menu principale.'''
    # funzioni:
    fun = [menuSalva, gtk._Void, menuOggetti, gtk._Void]
    # Numero di elementi del menu
    nitems = len(fun) # -> numero di funzioni associate al Menu
    # Elemento del Menu correntemente selezionato
    current = 0
    # Riposiziona il Menu in base alla posizione di Window
    root.obj["menu"][0].x = -root.window.pos[0] + 50
    root.obj["menu"][0].y = -root.window.pos[1] + (root.screen.size[1] - 
            root.obj["menu"][0].h) / 2
    # Riposiziona il puntatore
    root.obj["menu"][1].x, root.obj["menu"][1].y = root.obj["menu"][0].x, \
        root.obj["menu"][0].y
    
    # Cambia status a puntatore e menu
    root.obj["menu"][0].status = True
    root.obj["menu"][1].status = True
    
    # Entra nel loop
    while True:
        # Scansiono gli input dello user
        for e in pygame.event.get():
            # Quit
            if e.type == pygame.QUIT:
                root.run = False
                return
            
            # Pulsante spinto in basso
            if e.type == pygame.KEYDOWN:
                # Quit
                if e.key == pygame.K_q:
                    root.run = False
                    return
                # Chiude il Menu
                if e.key == pygame.K_m:
                    root.obj["menu"][0].status = False
                    root.obj["menu"][1].status = False
                    return
                
                if e.key == pygame.K_DOWN:
                    current += 1
                
                if e.key == pygame.K_UP:
                    current -= 1
                # Se premi 'Invio'
                if e.key == pygame.K_RETURN:
                    if current == nitems - 1:
                        root.obj["menu"][0].status = False
                        root.obj["menu"][1].status = False
                        return # 'ESCI' (è l'ultimo elemento)
                    else:
                        # Usa la funzione associata all'elemento selezionato
                        fun[current](root)
        
        # Modifica il valore di 'current' in modo che sia tra 0 e 'nitems'
        current %= nitems
        # Aggiorna posizione del puntatore
        root.obj["menu"][1].y = root.obj["menu"][0].y + (current * 
                root.obj["menu"][1].h) - 1
        # Pulisci la surface di 'root.window'
        root.window.surface = pygame.Surface(root.window.size)
        # Colora la surface di 'root.window' di verde
        root.window.surface.fill(gtk.GREEN)
        # Aggiorna la finestra
        root.updateWindow()
        pygame.display.update()
