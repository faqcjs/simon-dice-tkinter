from tkinter import *
from tkinter import ttk, font,messagebox
from claseJugador import Jugador
from claseGestorJugadores import GestorJugadores
import tkinter as tk
import time, random 
import datetime

class Aplicacion():
    def __init__(self):

        #   Configuraciones de la ventana
        self.__ventana =tk.Tk()
        self.__ventana.title('Simon dice')
        self.__ventana.geometry('250x450')

        self.__ventana.configure(bg='beige')
        self.__ventana.resizable(0,0)
        self.colores = ["#006400", "#8B0000", "#CCCC00", "#00008B"]
        # Barra menu
        barraMenu = Menu(self.__ventana)
        self.__ventana.config(menu = barraMenu)
        
        menuPuntaje = Menu(barraMenu, tearoff=0)
        barraMenu.add_cascade(label='Puntajes', menu = menuPuntaje)
        menuPuntaje.add_command(label='Galeria de Puntajes', command=self.galeria_puntaje)
        menuPuntaje.add_command(label='Salir', command=self.salir_aplicacion)
    
        #   Datos jugador
        self.__jugador = None
        self.__fecha = None
        self.__hora = None
        self.__puntaje = 0
        
        #   Creo instancias de jugadores nuevos y cargo jugadores anteriores al gestor
        self.__gestor = GestorJugadores()
        self.__gestor.cargarJugadores()
        
        #   Botones y sus posiciones
        self.botones = []
        
        #   para cada elemento de self.colores i es el indice del elemento color
        for i, color in enumerate(self.colores):
            #   Creo el canvas
            boton = tk.Canvas(self.__ventana, width=100, height=150, background=color, relief="raised")
            #   posiciono los canvas con los calculos de i // 2 y i % 2
            #   i // 2 esto organiza el canvas en filas de 2 
            #   i %  2 esto alterna en las posiciones entre las columnas 0 y 1
            boton.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            #   Agrego el boton q se creo en una lista de botones q son canvas en realidad
            self.botones.append(boton)
        #   Creo los botones de comenzar y salir
        self.botonComenzar = tk.Button(self.__ventana, text="Start", command=self.ventana_jugador, bg='beige', font='weight' )
        self.botonComenzar.grid(row=4, column=1, ipady=10, ipadx=30)
        
        
        #   Labels
        fuente = font.Font(weight='bold')
        self.labelJugador = tk.Label(self.__ventana, text='', font=fuente, padx=5, pady=5, bg='beige' )
        self.labelJugador.grid(column=0, row=3)
        self.puntaje = tk.Label(self.__ventana, text='0', font=fuente, padx=5, pady=5, bg='beige')
        self.puntaje.grid(column=1, row=3)
        
        
        #   Destroy de la ventana y guarda puntajes
        self.__ventana.protocol("WM_DELETE_WINDOW", self.salir_aplicacion)
        
        #   Main loop de la ventana
        self.__ventana.mainloop()


    #   Inicio el juego reseteando secuencia y respuesta del juegador
    def iniciar_juego(self):
        self.botonComenzar.config(state=tk.DISABLED) # luego de apretar el boton comenzar se inhabilita
        self.secuencia = []
        self.respuesta_jugador = []
        self.generar_color()  

    def generar_color(self):  
        if self.secuencia == []:                        # primer secuencia inicia con verde si la lsita esta vacioa
            color_nuevo = self.colores[0]
            self.secuencia.append(color_nuevo)
            self.mostrar_secuencia()
        else:
            color_nuevo = random.choice(self.colores)
            self.secuencia.append(color_nuevo)
            self.mostrar_secuencia()

    def mostrar_secuencia(self):                        # muestra la secuencia al jugador
        time.sleep(1)                                   # demora el programa 1 segund
        for color in self.secuencia:                    # itero sobre cada color guardada en la secuencia
            index_color = self.colores.index(color)     # encuentro el indice actual del self.secuenica
            self.botones[index_color].config(bg="gray") # con el indice actual cambio de color el boton a gris
            self.__ventana.update()                     # se actualiza la ventana para mostrar los cambios hechos 
            time.sleep(1)                               # demoro el programa en un segundo
            self.botones[index_color].config(bg=color)  # restablece al color original
            self.__ventana.update()                     # actualizo para ver los cambios
            time.sleep(0.5)
        self.jugar()                                    # llamo al metodo jugar

    def jugar(self):
        self.respuesta_jugador = []                             # renicia la lista donde esta la respuesta del jugador
        self.__ventana.bind("<Button-1>", self.procesar_clic)   # cada vez q haga click llama al metodo self.procesar_click

    def procesar_clic(self, event):
        colores_click = ['#7fbf80','#df5f5f','#ffff80','#7f7fbf'] # colores q sirven para der el efecto de boton clickeado
        boton_presionado = event.widget                           # guardo la referencia del boton clickeado
        color_presionado = boton_presionado.cget("background")    # guardo el color q fue presionado por el jugador
        self.respuesta_jugador.append(color_presionado)           # guardo el color del boton presionado por el jugador
        
        for i in range(len(self.colores)):                       
                                                                  
            if self.colores[i] == color_presionado:               # cambio de un color mas claro al boton presionado por el jugador
                boton_presionado.config(bg=colores_click[i])      # da el efecto del boton clickeado
                
        self.__ventana.update()
        time.sleep(0.2)
        boton_presionado.config(bg=color_presionado)              # restablece al color original
        self.__ventana.update()

        if len(self.respuesta_jugador) == len(self.secuencia):    # verifica la respuesta del jugador
            self.verificar_respuesta()

    def verificar_respuesta(self):
        
        if self.respuesta_jugador == self.secuencia:            # si la respuesta es correcta actualizo el puntaje
            self.actualizar_puntaje(len(self.secuencia))        # actualizo el puntaje obtenido
            self.generar_color()                                # vuelve a generar una nueva secuencia de colores
        else:
            messagebox.showinfo("¡Perdiste!", "¡Inténtalo de nuevo!") # si las secuencias son distintas
            self.botonComenzar.config(state=tk.NORMAL)                # restablezco el boton start
            self.guardar_record()                                     # guardo el record del jugador
            self.resetPuntaje()                                       # reseteo puntajes
            
    def resetPuntaje(self):
        self.puntaje.config(text='0')       # pongo en 0 el label del puntaje
        self.__puntaje = 0                  # reinicio en 0 la variable del puntaje
    def actualizar_puntaje(self, puntos):
        puntaje_actual = int(self.puntaje.cget("text")) # obtengo el puntaje actual desde el label
        self.__puntaje = puntaje_actual + puntos        # sumo el puntaje actual con el nuevo puntaje
        self.puntaje.config(text=str(self.__puntaje))   # acutualizo en el label el nuevo puntaje obtenido
        
     
    def guardar_record(self):
        fecha_hora = datetime.datetime.now() # obtengo fecha y hora del sistema
        self.__fecha = fecha_hora.date()    # guardo la hora
        self.__hora = fecha_hora.strftime('%H:%M:%S') #guardo la fecha
        self.__gestor.agregarJugador(Jugador(self.__jugador,self.__fecha,self.__hora,self.__puntaje))  # agrego un nuevo Jugador al gestor
        self.resetPuntaje()
    
    #  Ventana donde ingresa el nombre el jugador
    def ventana_jugador(self):
        self.__ventanaJug = Toplevel()         # creo la ventana hija de la principal
        fuente = font.Font(weight='bold')
        self.__ventanaJug.resizable(0,0)
        self.__ventanaJug.title('Ingresa tu Nick!')
        
        #   Labels e inputs
        self.labelDatosJug = tk.Label(self.__ventanaJug, text='Datos del jugador')
        self.labelDatosJug.grid(row=0, column=0)
        
        self.nombre_jugador = tk.Label(self.__ventanaJug, text='Jugador', font=fuente, padx=5, pady=5)
        self.nombre_jugador.grid(row=1, column=0)
        self.__jugador = StringVar()
        self.__jugador.set('')
       
        self.ctext1 = tk.Entry(self.__ventanaJug, textvariable=self.__jugador, width=30 )
        self.ctext1.grid(column=1, row=1, columnspan=2)
        
        #   Botones
        
        self.botonIniciar = tk.Button(self.__ventanaJug, text="Iniciar Juego",padx=5, pady=5, command=self.actualizarNombre)
        self.botonIniciar.grid(row=2, column=1)
        self.__ventanaJug.mainloop()
        
    def actualizarNombre(self):
        self.__jugador = self.ctext1.get()
        self.labelJugador.configure(text=self.__jugador)
        self.__ventanaJug.destroy()
        self.iniciar_juego()
    
    def salir_aplicacion(self):
        print('Saliendo de la app...\nGuardando records...')
        datos = self.__gestor.toJson()
        self.__gestor.guardarJSONArchivo(datos)
        self.__ventana.destroy()

    def galeria_puntaje(self):
        galeria = Toplevel()
        galeria.resizable(0,0)
        galeria.title('Galeria de Puntajes')
        frame = ttk.Frame(galeria)
        frame.pack(padx=10, pady=10)
        tree = ttk.Treeview(frame, columns=('Jugador', 'Fecha', 'Hora', 'Puntaje'), show='headings', height=5)
        
        tree.heading("Jugador", text="Jugador")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Hora", text="Hora")
        tree.heading("Puntaje", text="Puntaje")        
        
        tree.column("Jugador", width=100)
        tree.column("Fecha", width=100)
        tree.column("Hora", width=100)
        tree.column("Puntaje", width=100)
        
        jugadores = self.__gestor.get_jugadores()
        jugadores.sort()
        for jugador in jugadores:
            tree.insert("", tk.END, values=(jugador.getJugador(), jugador.getFecha(), jugador.getHora(), jugador.getPuntaje()))
            
        tree.pack()
        boton_salir = ttk.Button(galeria, text="Cerrar", command=galeria.destroy)
        boton_salir.pack(pady=10)
        
        galeria.mainloop()
        
if __name__ == '__main__':
    app = Aplicacion()
    