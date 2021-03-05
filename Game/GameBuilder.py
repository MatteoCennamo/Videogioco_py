# -*- coding: utf-8 -*-

'''
BUILDER DI LIVELLO PER RENDERE SEMPLICE LA COSTRUZIONE E SALVATAGGIO DEI LIVELLI
'''

import GameToolKit as gtk       # Classi del gioco
import OBJfunctions as objf     # Funzioni degli OBJ
import pygame                   # Pacchetto standard per videogame in Python
import tkinter as tk            # Interfaccia grafica utente (GUI)
import tkinter.messagebox       # Crea messaggi di errore o info
from tkinter import filedialog  # Carica file
import tkinter.font as tkFont   # Font delle scritte nel GUI
from tkinter import ttk         # Per combobox
import os                       # Sistema operativo
import pandas as pd             # Lavorare con dataframe
from inspect import getmembers, \
isfunction, isclass             # Create functions list from module

# Crea l'applicazione
class MyApp(tk.Tk):
    def __init__(self, color):
        # Assegna tutte le caratteristiche di un oggetto 'tk.Tk()'
        super().__init__()
        
        #####--- AGGIUNGI GLI ATTRIBUTI A ROOT ---#####
        
        self.color_app = color                  # colore dei bordi
        if os.path.isfile("./Builder_save.txt"):
            with open("./Builder_save.txt") as f:
                self.filename = f.readline()
        else:
            self.filename = ""                  # nome del file
        if self.filename: # Se è stato caricato un file
            try: # Potrebbe essere stato cancellato il file
                self.df = txt2DataFrame(self.filename)  # data frame
            except:
                self.filename = ""
                self.df = pd.DataFrame()
        else:
            self.df = pd.DataFrame()
        # Crea lista degli oggetti creati
        self.obj = fromDataFrame2OBJlist(self.df)
        
        #####--- RAPPRESENTA ROOT ---#####
        
        # Assegna un titolo alla finestra
        self.title("Builder di livello")
#        self.iconbitmap("./Lists/Lista_Parcheggi_icon.ico")
        
        # Posiziono la finestra al centro dello schermo
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("700x570+{}+{}".format(
                int((w / 2) - 350), int((h / 2) - 200)))
        
        # Creo il 'main_frame' che conterrà la schermata principale
        self.main_frame = MainFrame(self) # tk.Frame(self)
        # Contiene le informazioni sul file carcato
        self.info_frame = tk.Frame(self)
        tk.Label(self.info_frame, text = f"Carticato il seguente file: {self.filename}", 
                 padx = 10, pady = 5).pack(anchor = tk.W)
        
        
        #####--- CREA MENU ---#####
        
        # Genera il menu
        menubar = tk.Menu(self)
        
        # Genera il pulsante 'File' del menu
        menu_file = tk.Menu(menubar, tearoff = 0)
        
        # Aggiungi opzione di apertura di un file
        def superFileOpen():
            global game
            fileOpen(self, "./Builder_save.txt")
            self.df = txt2DataFrame(self.filename)
            # Crea lista degli oggetti creati
            self.obj = fromDataFrame2OBJlist(self.df)
            # Elimina tutti gli obj dalla mappa
            for k in game.obj.keys():
                if k not in ['personaggio', 'menu']:
                    game.obj[k] = []
            # Crea la mappa dal dataframe
            DataFrame2Map(self.df, game, Void = True)
            fromDataFrame2OBJ(self.main_frame.df, self.main_frame.current_idx, 
                              tipo = 'personaggio')
        
        # Aggiungi possibilità di creare un nuovo file
        menu_file.add_command(label = "Nuovo +", 
                              command = lambda: self.newFile())
        # Aggiungi opzione di apertura di file
        menu_file.add_command(label = "Apri...", 
                              command = lambda: superFileOpen())
        # Aggiungi opzione di salvataggio
        menu_file.add_command(label = "Salva", command = self.fileSave)
        # Aggiungi opzione di salvataggio con nome
        menu_file.add_command(label = "Salva con nome...", command = self.fileSaveAs)
        # Aggiungi un separatore tra le opzioni nel menu a cascata
        menu_file.add_separator()
        # Aggiungi opzione 'Chiudi applicazione'
        menu_file.add_command(label = "Chiudi applicazione", command = self.destroy)
        
        menubar.add_cascade(label = "File", menu = menu_file)
        
#        # Genera il pulsante 'Modifica'
#        menu_modifica = tk.Menu(menubar, tearoff = 0)
#        # Aggiungi funzionalità 'Assegna posti'
#        menu_modifica.add_command(label = "Assegna posti", command = lambda: self.modifica_assegna())
#        # Aggiungi un separatore tra le opzioni nel menu a cascata
#        menu_modifica.add_separator()
#        # Aggiungi funzionalità 'Aggiungi interni'
#        menu_modifica.add_command(label = "Aggiungi interni", command = lambda: self.modifica_aggiungi())
#        # Aggiungi funzionalità 'Rimuovi interni'
#        menu_modifica.add_command(label = "Rimuovi interni", command = lambda: self.modifica_rimuovi())
#        # Aggiungi un separatore tra le opzioni nel menu a cascata
#        menu_modifica.add_separator()
#        # Opzione resetta modifica
#        menu_modifica.add_command(label = "Resetta ultima modifica", 
#                                  command = lambda: self.modifica_reset())
#        
#        menubar.add_cascade(label = "Modifica", menu = menu_modifica)
        
#        #####--- RAPPRESENTA I FRAME ---#####
        
        self.info_frame.pack(anchor = tk.W, fill = 'x')
        self.main_frame.modifica(self)
        
        # Configura il menu
        self.config(menu = menubar, bg = self.color_app, pady = 1)
    
    def newFile(self):
        global game
        '''Pulisci l'area di lavoro per creare il nuovo livello.'''
        # Crea il nuovo file vuoto
        self.filename = './Untitled.txt'
        # Distruggi tutto quello che sta dentro il frame 'info_frame'
        for child in self.info_frame.winfo_children():
            child.destroy()
        # Scrivi il nome del file selezionato nell''info_frame'
        tk.Label(self.info_frame, text = f"Carticato il seguente file: {self.filename}", 
                 padx = 10, pady = 5).pack(anchor = tk.W)
        
        with open(self.filename, 'w') as f:
            print('', sep = '', end = '', file = f)
        self.obj = []
        for k in game.obj:
            if k not in ['personaggio', 'menu']:
                game.obj[k] = []
    
    def fileSave(self):
        '''Salva in file correntemente aperto.'''
        global game
        # Salva il file di testo
        DataFrame2txt(self.df, self.filename)
        # Salva il file in 'Builder_save' per riaprire direttamente il salvataggio
        with open("./Builder_save.txt", "w") as f:
            print(self.filename, end = '', sep = '', file = f)
        
        # Sovrascrivi il file di testo del livello
        saveMap(self.filename, self.obj, (self.main_frame.map_width.get(), 
                                         self.main_frame.map_height.get()), \
        game.window.pos)
        
    
    def fileSaveAs(self):
        '''Salva il file .txt con nome.'''
        global game
        save_filename = self.filename
        # Seleziona il file
        self.filename = filedialog.asksaveasfilename(initialdir = os.getcwd(), 
                                               title = "Seleziona un file", 
                                               filetypes = (("txt files", "*.txt"), 
                                                            ("all files", "*.*")))
        if self.filename == "":           # Se non viene selezionato alcun file
            self.filename = save_filename # ripristina nome del file precedente
            return # Non fare nient'altro
        
        # Controlla se finisce con .txt
        if not self.filename.endswith('.txt'):
            self.filename = self.filename + '.txt'
        
        # Salva il file di testo
        DataFrame2txt(self.df, self.filename)
        # Salva il file in 'Builder_save' per riaprire direttamente il salvataggio
        with open("./Builder_save.txt", "w") as f:
            print(self.filename, end = '', sep = '', file = f)
        
        # Distruggi tutto quello che sta dentro il frame 'info_frame'
        for child in self.info_frame.winfo_children():
            child.destroy()
        # Scrivi il nome del file selezionato nell''info_frame'
        tk.Label(self.info_frame, text = f"Carticato il seguente file: {self.filename}", 
                 padx = 10, pady = 5).pack(anchor = tk.W)
        
        # Sovrascrivi il file di testo del livello
        saveMap(self.filename, self.obj, (self.main_frame.map_width.get(), 
                                         self.main_frame.map_height.get()), \
        game.window.pos)

class MainFrame(tk.Frame):
    def __init__(self, master):
        '''Genera il main frame di MyApp.main_frame.'''
        global game
        # Assegna tutte le caratteristiche di un oggetto 'tk.Frame()'
        super().__init__(master)
        if os.path.isfile("./Builder_salvataggio_surfaces.txt"):
            with open("./Builder_salvataggio_surfaces.txt") as f:
                self.filename = f.readline()
        else:
            self.filename = ""                  # nome del file
        try: # Potrebbe essere stato cancellato il file
            self.df = txt2DataFrame(self.filename)  # data frame con surfaces
        except:
            self.filename = ""
            self.df = pd.DataFrame()
        
        # tipo di finestra aperta
        self.window = 'modifica'  # di default
        # Genera il frame del titolo
        self.title = tk.Frame(master)
        # Contiene il path dal quale sono prese le surface
        self.info_frame = tk.Frame(master)
        # Font del titolo
        self.title_font = tkFont.Font(family = "Lucida Grande", size = 17, 
                                      weight = tkFont.BOLD)
        # Contiene comandi per le modifiche
        self.command_frame = tk.Frame(master)
        
        # Valori correnti della surface
        self.current_idx = 0
        if self.filename: # Se è stato caricato un file
            fromDataFrame2OBJ(self.df, self.current_idx, tipo = 'personaggio')
            
            # Informazioni sulla surface selezionata
            self.info_text = tk.StringVar()
            self.info_text.set(f"ID: {self.current_idx}\n{self.df['NOTE'].loc[self.current_idx][2:]}")
        else:
            # Informazioni sulla surface selezionata
            self.info_text = tk.StringVar()
        
        # Attributi dell'oggetto animato
        self.x = tk.StringVar()
        self.y = tk.StringVar()
        self.z = tk.StringVar()
        self.xspeed = tk.StringVar()
        self.yspeed = tk.StringVar()
        self.w = tk.StringVar()
        self.h = tk.StringVar()
        self.pl = tk.StringVar()      # penetrabilità laterale
        self.pv = tk.StringVar()      # penetrabilità verticale
        self.fun = tk.StringVar()     # funzione associata all'oggetto
        self.type = tk.StringVar()    # 'type' dell'oggetto
        self.nFrames = tk.StringVar() # 'nFrames' dell'oggetto
        
        # Attributi della mappa
        self.map_width = tk.StringVar()  # larghezza della mappa
        self.map_height = tk.StringVar() # altezza della mappa
        if master.filename: # Se è stato caricato un file
            self.map_width.set(master.df.iloc[0, 0])
            self.map_height.set(master.df.iloc[0, 1])
        else:
            self.map_width.set('1000')
            self.map_height.set('1000')
        
        self.functions_list = ['objf.' + o[0] for o in getmembers(objf) if \
                               isfunction(o[1])]
        self.categories_list = ["personaggio", "oggetto", "ostacolo", "volante", 
                                "pavimento", "menu"]
        self.class_list = ['gtk.' + o[0] for o in getmembers(gtk) if \
                           isclass(o[1])]
        # Immetti valori di default
        self.ResetParams()
    
    def modifica(self, master):
        '''Apre la possibilità di modificare il livello usando i dati contenuti 
        in 'master'.'''
        global game
        self.window = 'modifica'
        
        # Pulisci il frame
        for child in master.main_frame.winfo_children():
            child.destroy()
        
        # Genera il main_frame
        tk.Label(self.title, text = "Da qui è possibile modificare le surface.", 
                 padx = 10, pady = 5, bg = 'white', font = self.title_font).pack()
        tk.Label(self.info_frame, text = f"Carticato il seguente file: {self.filename}", 
                 padx = 10, pady = 5).pack(anchor = tk.W)
        
        def OpenSurfaceFile():
            # Risistema le surface solo se viene modificato il nome file
            old_filename = self.filename
            fileOpen(self, './Builder_salvataggio_surfaces.txt')
            if self.filename != old_filename:
                self.df = txt2DataFrame(self.filename)
                self.ChangeImage(-self.current_idx)
        
        # Crea il pulsante di apertura del file
        tk.Button(self.command_frame, text = 'Apri...', cursor = 'hand2', command = lambda: 
                  OpenSurfaceFile()).grid(
                          row = 0, column = 0, padx = 10, pady = 5, sticky = 'w')
        tk.Label(self.command_frame, text = "Apri il file che contiene i ritagli delle surface").grid(
                row = 0, column = 1, padx = 4, pady = 5, sticky = 'w')
        
        # Crea i pulsanti per andare avanti e indietro nella selezione della surface
        tk.Button(self.command_frame, text = '<< Indietro', width = 12, cursor = 'hand2', 
                  command = lambda: self.ChangeImage(-1)).grid(
                row = 1, column = 0, padx = 10, pady = 5, sticky = 'e')
        tk.Label(self.command_frame, textvariable = self.info_text).grid(
                row = 1, column = 1, padx = 4, pady = 5, sticky = 'nswe')
        tk.Button(self.command_frame, text = 'Avanti >>', width = 12, cursor = 'hand2', 
                  command = lambda: self.ChangeImage(1)).grid(
                row = 1, column = 2, padx = 10, pady = 5, sticky = 'w')
        
        # Prendi i valori di input
        tk.Label(self.command_frame, text = 'x').grid(sticky = 'e')
        tk.Entry(self.command_frame, textvariable = self.x).grid(
                row = 2, column = 1, sticky = 'w')
        tk.Label(self.command_frame, text = 'y').grid(sticky = 'e')
        tk.Entry(self.command_frame, textvariable = self.y).grid(
                row = 3, column = 1, sticky = 'w')
        tk.Label(self.command_frame, text = 'z').grid(sticky = 'e')
        tk.Entry(self.command_frame, textvariable = self.z).grid(
                row = 4, column = 1, sticky = 'w')
        
        # Linea di separazione orizzontale
        tk.Frame(self.command_frame, bg = 'dark gray', height = 1).grid(
                padx = 20, pady = 10, columnspan = 2, sticky = 'we')
        
        # Altri parametri
        tk.Label(self.command_frame, text = 'xspeed').grid(sticky = 'e')
        tk.Entry(self.command_frame, textvariable = self.xspeed).grid(
                row = 6, column = 1, sticky = 'w')
        tk.Label(self.command_frame, text = 'yspeed').grid(sticky = 'e')
        tk.Entry(self.command_frame, textvariable = self.yspeed).grid(
                row = 7, column = 1, sticky = 'w')
        tk.Label(self.command_frame, text = 'width').grid(sticky = 'e')
        tk.Entry(self.command_frame, textvariable = self.w).grid(
                row = 8, column = 1, sticky = 'w')
        tk.Label(self.command_frame, text = 'height').grid(sticky = 'e')
        tk.Entry(self.command_frame, textvariable = self.h).grid(
                row = 9, column = 1, sticky = 'w')
        
        tk.Label(self.command_frame, text = 'pl').grid(sticky = 'e')
        tk.Entry(self.command_frame, textvariable = self.pl).grid(
                row = 10, column = 1, sticky = 'w')
        tk.Label(self.command_frame, text = 'pv').grid(sticky = 'e')
        tk.Entry(self.command_frame, textvariable = self.pv).grid(
                row = 11, column = 1, sticky = 'w')
        
        tk.Label(self.command_frame, text = 'type').grid(sticky = 'e')
        tk.Entry(self.command_frame, textvariable = self.type).grid(
                row = 12, column = 1, sticky = 'w')
        tk.Label(self.command_frame, text = 'nFrames').grid(sticky = 'e')
        tk.Entry(self.command_frame, textvariable = self.nFrames).grid(
                row = 13, column = 1, sticky = 'w')
        
        # Combobox per le classi
        tk.Label(self.command_frame, text = 'class').grid(sticky = 'e')
        setattr(self, 'combo_class', ttk.Combobox(self.command_frame, values = 
                                                self.class_list, width = 30, 
                                                state = "readonly"))
        self.combo_class.set('gtk.Oggetto')
        self.combo_class.grid(row = 14, column = 1, sticky = tk.W, pady = 5)
        
        # Combobox per le funzioni
        tk.Label(self.command_frame, text = 'function').grid(sticky = 'e')
        setattr(self, 'combo_fun', ttk.Combobox(self.command_frame, values = 
                                                self.functions_list, width = 30, 
                                                state = "readonly"))
        self.combo_fun.current(0)
        self.combo_fun.grid(row = 15, column = 1, sticky = tk.W, pady = 5)
        
        # Combobox con le categorie
        tk.Label(self.command_frame, text = 'category').grid(sticky = 'e')
        setattr(self, 'combo_cat', ttk.Combobox(self.command_frame, values = 
                                                self.categories_list, width = 30, 
                                                state = "readonly"))
        self.combo_cat.set('ostacolo')
        self.combo_cat.grid(row = 16, column = 1, sticky = tk.W, pady = 5)
        
        # Reset valori
        tk.Button(self.command_frame, text = 'Default', width = 12, cursor = 'hand2', 
                  command = lambda: self.ResetParams()).grid(
                          row = 17, column = 0, padx = 10, pady = 5, sticky = 'e')
        
        # Linea di separazione verticale
        tk.Frame(self.command_frame, bg = 'dark gray', width = 1).grid(row = 2, 
                column = 3, padx = 10, pady = 20, rowspan = 12, sticky = 'ns')
        
        # Dimensioni della mappa
        tk.Label(self.command_frame, text = 'Parametri della mappa:').grid(
                row = 2, column = 4, columnspan = 2, sticky = 'we')
        tk.Label(self.command_frame, text = 'map width').grid(row = 3, column = 4, 
                sticky = 'e')
        tk.Entry(self.command_frame, textvariable = self.map_width).grid(
                row = 3, column = 5, sticky = 'w')
        tk.Label(self.command_frame, text = 'map height').grid(row = 4, column = 4, 
                sticky = 'e')
        tk.Entry(self.command_frame, textvariable = self.map_height).grid(
                row = 4, column = 5, sticky = 'w')
        
        #####--- Rappresenta i frame ---#####
        self.title.pack(pady = 1, anchor = tk.N)
        self.info_frame.pack(fill = 'x')
        self.command_frame.pack(fill = 'both', padx = 1, pady = 1, expand = True)
        self.pack(fill = 'both', expand = True)
        
        # Configura le colonne
        self.command_frame.columnconfigure(0, weight = 1)
        self.command_frame.columnconfigure(1, weight = 1)
        self.command_frame.columnconfigure(2, weight = 1)
        self.command_frame.columnconfigure(5, weight = 1)
    
    def ChangeImage(self, direction):
        size = self.df.shape
        self.current_idx = (self.current_idx + direction) % size[0]
        # Cambia l'immagine
        fromDataFrame2OBJ(self.df, self.current_idx, tipo = 'personaggio')
        # Aggiorna informazioni sulla surface
        self.info_text.set(f"ID: {self.current_idx}\n{self.df['NOTE'].loc[self.current_idx][2:]}")
    
    def UpdateParams(self):
        global game
        if game.obj['personaggio'][0].xchange == 0:
            game.obj['personaggio'][0].x = int(self.x.get() if self.x.get() else 0)
        else:
            self.x.set(str(round(game.obj['personaggio'][0].x)))
        if game.obj['personaggio'][0].ychange == 0:
            game.obj['personaggio'][0].y = int(self.y.get() if self.y.get() else 0)
        else:
            self.y.set(str(round(game.obj['personaggio'][0].y)))
        if self.xspeed.get():
            game.obj['personaggio'][0].xspeed = float(self.xspeed.get())
        if self.yspeed.get():
            game.obj['personaggio'][0].yspeed = float(self.yspeed.get())
        if self.pl.get():
            game.obj['personaggio'][0].pl = float(self.pl.get())
        else:
            game.obj['personaggio'][0].pl = 0
        if self.pv.get():
            game.obj['personaggio'][0].pv = float(self.pv.get())
        else:
            game.obj['personaggio'][0].pv = 0
        if self.w.get() == '':
            w_temp = 0
        else:
            w_temp = int(self.w.get())
        if self.h.get() == '':
            h_temp = 0
        else:
            h_temp = int(self.h.get())
        if self.z.get() == '':
            z_temp = 0
        else:
            z_temp = int(self.z.get())
        game.obj['personaggio'][0].resize(w = w_temp, h = h_temp)
        game.obj['personaggio'][0].z = z_temp
        game.obj['personaggio'][0].type = self.type.get()
        # Modifica .image_dict in maniera che tutte le posizioni sono uguali
        for k in ['down', 'left', 'right', 'up']:
            for i in range(4):
                game.obj['personaggio'][0].image_dict[k][i] = \
                game.obj['personaggio'][0].image_dict['down'][0]
        if self.window == 'modifica': # if hasattr(self, 'combo_fun'):
            self.fun.set(self.combo_fun.get())
    
    def ResetParams(self):
        # Restituisci valori di default degli attributi
        self.z.set('0')
        self.xspeed.set('0.1')
        self.yspeed.set('0.1')
        self.w.set('100')
        self.h.set('100')
        self.pl.set('0')
        self.pv.set('0')
        self.fun.set(self.functions_list[0])
        self.type.set('')
        self.nFrames.set('1')
        if hasattr(self, 'combo_fun'):
            self.combo_class.set('gtk.Oggetto')
            self.combo_fun.current(0)
            self.combo_cat.set('ostacolo')
        # Aggiorna i valori
        try:
            self.UpdateParams()
        except:
            return

# Importa il file .txt dalla directory attuale
def txt2DataFrame(path):
    '''Restituisce un pandas.DataFrame da una stringa 'path' che è il percorso 
    del file .txt dove sono salvati i dati.'''
    if path:
        df = pd.read_csv(path, sep = '\t')
    else:
        df = pd.DataFrame()
    return df

# Salva il pandas data frame nel file .txt
def DataFrame2txt(df, path):
    '''Salva un pandas.DataFrame 'df' in un file .txt specificato dalla stringa 
    'path'.'''
    with open(path, 'w') as f:
        f.write(df.to_csv(header = True, index = False, sep = '\t'))
        f.close()

# Carica una mappa da un file di testo
def DataFrame2Map(df, gm, Void = False):
    '''Prende un oggetto un Pandas DataFrame. Poi interpreta il dataframe per 
    creare gli '.obj' dell'oggetto GameInit ('gm'). Se 'Void' = True, tutte le 
    funzioni degli obj sono impostate a 'objf._Void'.'''
    # Imposta la grandezza della finestra
    gm.window.size = [int(df.iloc[0, 0]), int(df.iloc[0, 1])]
    
    # Interpreta i dati parsando riga per riga
    n, m = df.shape
    for i in range(1, n):
        # Prendi tutte le variabili
        CLASS, CAT, X, Y, W, H, PATH, xPOS, yPOS, zPOS, WIDTH, HEIGHT, xSPEED, \
        ySPEED, FUN, TYPE, PL, PV, nFRAMES = df.iloc[i]
        if Void:
            FUN = 'objf._Void'
        # Cambia tipo di dati
        W = int(W)
        H = int(H)
        WIDTH = int(WIDTH)
        HEIGHT = int(HEIGHT)
        if not nFRAMES:
            nFRAMES = 1 # di default
        else:
            nFRAMES = int(nFRAMES)
        # A seconda della classe associata all'oggetto, usa una funzione diversa
        if CLASS == 'gtk.Oggetto':
            o = gtk.Oggetto(PATH, (X, Y, W, H), (xPOS, yPOS, zPOS), (WIDTH, HEIGHT), 
                            TYPE, pl = PL, pv = PV, nFrames = nFRAMES)
        elif CLASS == 'gtk.Personaggio':
            o = gtk.Personaggio(PATH, (X, Y, W, H), (xPOS, yPOS, zPOS), (WIDTH, HEIGHT), 
                                (xSPEED, ySPEED), pl = PL, pv = PV, tipo = TYPE)
        else:
            print(f'ERRORE: classe sbagliata -> {CLASS}')
            print(f"Riga all'indice {i}")
            break
        # Aggiungi l'oggetto all'obj
        gm.OBJadd(CAT, o, eval(FUN))

# Crea funzione che genera il Pandas dataframe
def fileOpen(master, path_save):
    '''Carica i dati del file .txt. 'master' deve essere un frame che contiene 
    un frame '.info_frame'.'''
    save_filename = master.filename
    master.filename = filedialog.askopenfilename(initialdir = os.getcwd(), 
                                               title = "Seleziona un file", 
                                               filetypes = (("txt files", "*.txt"), 
                                                            ("all files", "*.*")))
    if master.filename == "":           # Se non viene selezionato alcun file
        master.filename = save_filename # ripristina nome del file precedente
        
    # Carica il file di testo
    master.df = txt2DataFrame(master.filename)
    # Salva il file in 'Builder_save' per riaprire direttamente il salvataggio
    if master.filename:
        with open(path_save, "w") as f:
            print(master.filename, file = f, end = '', sep = '')
    
    # Distruggi tutto quello che sta dentro il frame 'info_frame'
    for child in master.info_frame.winfo_children():
        child.destroy()
    # Scrivi il nome del file selezionato nell''info_frame'
    tk.Label(master.info_frame, text = f"Carticato il seguente file: {master.filename}", 
             padx = 10, pady = 5).pack(anchor = tk.W)

def fromDataFrame2OBJ(df, idx, tipo = 'personaggio'):
    '''Prende l'indice del data frame e converte le informazioni in un obj. 
    'tipo' è 'personaggio' o 'oggetto'.'''
    global game
    try:
        pos = (game.obj['personaggio'][0].x, game.obj['personaggio'][0].y, 
               game.obj['personaggio'][0].z)
        size = (game.obj['personaggio'][0].w, game.obj['personaggio'][0].h)
        speed = (game.obj['personaggio'][0].xspeed, game.obj['personaggio'][0].yspeed)
    except:
        return
    if tipo == 'personaggio':
        obj = gtk.Personaggio(df['PATH'].loc[idx], df[['xPOS', 'yPOS', 'WIDTH', 
                              'HEIGHT']].loc[idx], pos, (
        int(size[0]), int(size[1])), speed)
    
    # Modifica .image_dict in maniera che tutte le posizioni sono uguali
    for k in ['down', 'left', 'right', 'up']:
        for i in range(4):
            obj.image_dict[k][i] = obj.image_dict['down'][0]
    obj.fun = objf.playerAnimation
    # Scambia il personaggio con l'obj
    game.obj['personaggio'][0] = obj

def fromDataFrame2OBJlist(df):
    '''Crea l'oggetto 'MyApp.obj' che è una lista di dizionari da un dataframe.'''
    obj = []
    n, m = df.shape
    # Inizia dall'indice 1 perchè il primo indice contiene la dimensione della mappa
    for i in range(1, n):
        CLASS, CAT, X, Y, W, H, PATH, xPOS, yPOS, zPOS, WIDTH, HEIGHT, xSPEED, \
        ySPEED, FUN, TYPE, PL, PV, nFRAMES = df.iloc[i]
        # Cambia tipo di dati
        W = int(W)
        H = int(H)
        WIDTH = int(WIDTH)
        HEIGHT = int(HEIGHT)
        if not nFRAMES:
            nFRAMES = 0
        else:
            nFRAMES = int(nFRAMES)
        obj += [{'CLASS': CLASS, 'CAT': CAT, 'X': X, 'Y': Y, 'W': W, 'H': H, 
                 'PATH': PATH, 'xPOS': xPOS, 'yPOS': yPOS, 'zPOS': zPOS, 
                 'WIDTH': WIDTH, 'HEIGHT': HEIGHT, 'xSPEED': xSPEED, 
                 'ySPEED': ySPEED, 'FUN': FUN, 'TYPE': TYPE, 'PL': PL, 'PV': PV, 
                 'nFRAMES': nFRAMES}]
    return obj

def saveMap(path, data, window_size, window_pos):
    '''Prende un percorso file 'path' e dei 'dati' come una lista di dizionari 
    (ogni dizionario fa parte della lista MyApp.obj). I dati sono caricati in 
    un file .txt che rappresenta la mappa, contemporaneamente a un file .png che 
    rappresenta i pavimenti della mappa. La prima riga del file di testo rappresenta 
    la grandezza della mappa (Window.size), la posizione della mappa (Window.pos).'''
    if path:
        with open(path, "w") as f:
            print('CLASS\tCAT\tX\tY\tW\tH\tPATH\txPOS\tyPOS\tzPOS\tWIDTH\tHEIGHT\t' + 
                  'xSPEED\tySPEED\tFUN\tTYPE\tPL\tPV\tnFRAMES', file = f)
            print(window_size[0], '\t', window_size[1], '\t', window_pos[0], '\t', 
                  window_pos[1], file = f, end = '', sep = '')
            for i in range(len(data)):
                idx = 0
                for k, v in data[i].items():
                    if k == 'CLASS':      # Primo valore
                        start = '\n'
                        end = '\t'
                    elif k == 'nFRAMES':  # Ulimo valore
                        if v == '':
                            v = 1
                        start = ''
                        end = ''
                    else:
                        start = ''
                        end = '\t'
                    print(start, v, end, file = f, sep = '', end = '')
                    idx += 1
    print('Salvataggio completato in:', path, sep = '\n')

def gameOpen():
    '''Apre la schermata del gioco.'''
    global game, root
    # Reimposta il titolo della finestra
    game.screen.title = root.filename.split('/')[-1] # pygame.display.set_caption(root.filename.split('/')[-1])
    # Pulisci la surface di 'root.window'
    def control_window_size(v, m):
        ''' v -> value. m -> minimum value.'''
        if v:
            v = int(v)
        else:
            v = 0
        if v < m:
            v = m
        return v
    
    wind_w = control_window_size(root.main_frame.map_width.get(), 
                                 game.screen.size[0])
    wind_h = control_window_size(root.main_frame.map_height.get(), 
                                 game.screen.size[1] - game.status_bar.size[1])
    game.window.size = (wind_w, wind_h)
    # Aggiorna surface
    game.window.surface = pygame.Surface(game.window.size)
    # Colora la surface di 'root.window' di verde
    game.window.surface.fill(gtk.GREEN)
    # Aggiorna la finestra
    game.updateWindow()
    
    try:
        if root.main_frame.window == 'modifica':
            root.main_frame.UpdateParams()
    except:
        pass

'''
INIZIA IL VERO E PROPRIO PROGRAMMA
'''
def main():
    global root, game
    # Crea finestra principale
    root = MyApp("blue")
    
    # Inizializza il gioco
    game = gtk.GameInit(title = root.filename.split('/')[-1], screen_size = (1000, 600), 
                        window_size = (1200, 700), mainloop = lambda: gameOpen(), 
                        tkinterObject = root, builderMode = True)
    
    # Crea oggetto personaggio
    player = gtk.Personaggio("./Sprites/Personaggi_16x16.png", (48, 0, 16, 16), 
                             (0, 0), (75, 75), (0.1, 0.1), pl = 15, pv = 50)
    # Aggiungi il personaggio a 'root'
    game.OBJadd("personaggio", player, objf.playerAnimation)
    # Crea la mappa dal dataframe
    try:
        DataFrame2Map(root.df, game, Void = True)
    except:
        pass
    if root.main_frame.filename: # Se viene caricato un file
        fromDataFrame2OBJ(root.main_frame.df, root.main_frame.current_idx, 
                          tipo = 'personaggio')
    
    # Avvia il main loop
    game.MainLoop()

if __name__ == '__main__':
    main()