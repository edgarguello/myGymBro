import tkinter as tk
from tkinter import messagebox, ttk

class VistaGrafica(tk.Tk):
    """
    Ventana principal de la aplicación MyGymBro, que gestiona los distintos frames (pantallas) y coordina la navegación.
    """
    
    def __init__(self):
        """
        Inicializa la ventana principal, configura tamaño y estructura, y muestra el menú inicial.
        """
        super().__init__()
        self.controlador = None  
        self.title("MyGymBro")
        self.geometry("600x400")
        self._init_frames()
        self.mostrar_menu()

    def set_controlador(self, controlador):
        """
        Asigna el controlador principal del modelo.
        Args:
            controlador: Instancia que gestiona la lógica del programa.
        """
        self.controlador = controlador

    def _init_frames(self):
        """
        Inicializa y almacena las pantallas (frames) disponibles en la aplicación: Menú, Selección, Creación y Ejecución.
        """
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MenuFrame, SeleccionFrame, CrearFrame, RealizarFrame):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def mostrar_menu(self):
        """
        Muestra la pantalla principal del menú.
        """
        self.normalizar()
        self._show_frame("MenuFrame")

    def mostrar_seleccionar(self):
        """
        Muestra la pantalla de selección de rutina, actualizando la lista disponible.
        """
        f = self.frames["SeleccionFrame"]
        f.actualizar_lista(self.controlador.obtener_rutinas())
        f.on_eliminar = self.eliminar_rutina
        self.normalizar()
        self._show_frame("SeleccionFrame")

    def mostrar_crear(self):
        """
        Muestra el formulario para crear una nueva rutina desde cero.
        """
        form = self.frames["CrearFrame"]
        form.limpiar()
        self.maximizar()
        self._show_frame("CrearFrame")

    def mostrar_realizar(self, rutina):
        """
        Muestra la pantalla para ejecutar una rutina.
        Args:
            rutina: Rutina a ejecutar.
        """
        form = self.frames["RealizarFrame"]
        form.iniciar_rutina(rutina)
        self.normalizar()
        self._show_frame("RealizarFrame")

    def _show_frame(self, name):
        """
        Muestra en pantalla el frame correspondiente y oculta los demás.
        Args:
            name (str): Nombre del frame a mostrar.
        """
        for f in self.frames.values():
            f.pack_forget() 
            f.grid_remove()
        frame = self.frames[name]
        frame.grid()
        frame.tkraise()
    
    def eliminar_rutina(self, rutina):
        """
        Elimina una rutina del sistema y actualiza la lista en la vista de selección.
        Args:
            rutina: Rutina a eliminar.
        """
        self.controlador.eliminar_rutina(rutina)
        self.mostrar_seleccionar()  # Refresca la lista

    def maximizar(self):
        """
        Intenta maximizar la ventana principal según el sistema operativo.
        """
        try:
            self.state('zoomed') 
        except Exception:
            try:
                self.attributes('-zoomed', True) 
            except Exception:
                pass 

    def normalizar(self):
        """
        Restaura el tamaño normal de la ventana.
        """
        self.state('normal')

    def mostrar_error(self, mensaje: str):
        """
        Muestra un mensaje de error en un cuadro de diálogo.
        Args:
            mensaje (str): Texto del error a mostrar.
        """
        messagebox.showerror("Error", mensaje)


class MenuFrame(tk.Frame):
    """
    Pantalla de menú principal con opciones para seleccionar, crear rutina o salir.
    """
    def __init__(self, parent, controller):
        """
        Inicializa la pantalla de menú y sus botones de navegación.
        Args:
            parent: Contenedor padre.
            controller: Controlador principal que gestiona los cambios de pantalla.
        """
        super().__init__(parent)
        tk.Label(self, text="Menú Principal", font=('Arial', 18)).pack(pady=20)
        tk.Button(self, text="Seleccionar rutina", width=20,
                  command=controller.mostrar_seleccionar).pack(pady=5)
        tk.Button(self, text="Crear rutina", width=20,
                  command=controller.mostrar_crear).pack(pady=5)
        tk.Button(self, text="Salir", width=20,
                  command=controller.destroy).pack(pady=5)

class SeleccionFrame(tk.Frame):
    """
    Pantalla para seleccionar una rutina existente, mostrar sus detalles y ejecutarla o eliminarla.
    """

    def __init__(self, parent, controller):
        """
        Inicializa la pantalla de selección de rutinas y sus componentes gráficos.
        Args:
            parent: Contenedor padre.
            controller: Controlador principal para manejar eventos de navegación.
        """
        super().__init__(parent)
        tk.Label(self, text="Seleccionar Rutina", font=('Arial', 18)).pack(pady=10)
        self.lst = tk.Listbox(self)
        self.lst.pack(fill='both', expand=True, padx=20)

        self.detalle = tk.Text(self, height=6, state='disabled')
        self.detalle.pack(padx=20, pady=5, fill='x')

        self.lst.bind("<<ListboxSelect>>", lambda e: self._mostrar_detalle())

        btn = tk.Button(self, text="Realizar", command=lambda: self._realizar(controller))
        btn.pack(pady=10)
        btn_eliminar = tk.Button(self, text="Eliminar", command=self._eliminar)
        btn_eliminar.pack(pady=5)
        self.on_eliminar = lambda rutina: None 
        tk.Button(self, text="Volver", command=controller.mostrar_menu).pack()

    def actualizar_lista(self, rutinas):
        """
        Actualiza la lista de rutinas disponibles.
        Args:
            rutinas (list): Lista de rutinas a mostrar.
        """
        self.lst.delete(0, tk.END)
        self._rutinas = rutinas
        for r in rutinas:
            descripcion = f"{r.nombre} ({len(r.ejercicios)} ejercicios)"
            self.lst.insert(tk.END, descripcion)

    def _realizar(self, controller):
        """
        Inicia la rutina seleccionada, si se ha hecho una selección.
        Args:
            controller: Controlador para mostrar la pantalla de ejecución.
        """
        sel = self.lst.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una rutina.")
            return
        rutina = self._rutinas[sel[0]]
        controller.mostrar_realizar(rutina)

    def _mostrar_detalle(self):
        """
        Muestra una descripción detallada de los ejercicios de la rutina seleccionada.
        """
        sel = self.lst.curselection()
        if not sel:
            return
        rutina = self._rutinas[sel[0]]
        texto = "\n".join(f"- {e.nombre_ejercicio}: {e.descripcion()}" for e in rutina.ejercicios)
        self.detalle.config(state='normal')
        self.detalle.delete('1.0', tk.END)
        self.detalle.insert(tk.END, texto)
        self.detalle.config(state='disabled')
    
    def _eliminar(self):
        """
        Solicita confirmación y elimina la rutina seleccionada si el usuario acepta.
        """
        sel = self.lst.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una rutina para eliminar.")
            return
        rutina = self._rutinas[sel[0]]
        confirm = messagebox.askyesno("Confirmar", f"¿Deseas eliminar la rutina '{rutina.nombre}'?")
        if confirm:
            self.on_eliminar(rutina)

class CrearFrame(tk.Frame):
    """
    Pantalla para crear una nueva rutina de ejercicios (de tipo fuerza o cardio).
    """
    def __init__(self, parent, controller):
        """
        Inicializa el formulario de creación de rutinas con campos dinámicos según el tipo/subtipo seleccionado.
        Args:
            parent: Contenedor padre.
            controller: Controlador para gestionar acciones y navegación.
        """
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Crear Rutina", font=('Arial', 18)).pack(pady=10)

        self.nombre = tk.StringVar()
        entry = tk.Entry(self, textvariable=self.nombre, fg='grey', bg='black', insertbackground='white')
        entry.insert(0, "Nombre de la rutina")
        entry.pack(pady=5)
        entry.bind("<FocusIn>", lambda e: self._clear_placeholder(entry))
        entry.bind("<FocusOut>", lambda e: self._set_placeholder(entry))
        self._entry = entry

        tipo_frame = tk.Frame(self)
        tipo_frame.pack(pady=5, fill='x', padx=10)
        tk.Label(tipo_frame, text="Tipo:").pack(side='left')
        self.tipo_var = tk.StringVar()
        self.tipo_cb = ttk.Combobox(tipo_frame, textvariable=self.tipo_var, state="readonly")
        self.tipo_cb.pack(side='left', fill='x', expand=True)
        self.tipo_cb['values'] = ["Fuerza", "Cardio"]
        self.tipo_cb.bind("<<ComboboxSelected>>", self._on_tipo_seleccionado)

        subtipo_frame = tk.Frame(self)
        subtipo_frame.pack(pady=5, fill='x', padx=10)
        tk.Label(subtipo_frame, text="Subtipo:").pack(side='left')
        self.subtipo_var = tk.StringVar()
        self.subtipo_cb = ttk.Combobox(subtipo_frame, textvariable=self.subtipo_var, state="readonly")
        self.subtipo_cb.pack(side='left', fill='x', expand=True)
        self.subtipo_cb.bind("<<ComboboxSelected>>", self._on_subtipo_seleccionado)

        self.campos_frame = ttk.Frame(self)
        self.campos_frame.pack(pady=10, fill='both', expand=True, padx=10)

        tk.Button(self, text="Agregar ejercicio", command=self._agregar).pack(pady=5)

        tk.Label(self, text="Ejercicios agregados:").pack()
        self.lst_ejercicios = tk.Listbox(self, height=6)
        self.lst_ejercicios.pack(fill='both', expand=False, padx=20, pady=5)

        botones_frame = tk.Frame(self)
        botones_frame.pack(pady=5)
        tk.Button(botones_frame, text="Guardar rutina", command=self._guardar).pack(side='left', padx=5)
        tk.Button(botones_frame, text="Volver", command=controller.mostrar_menu).pack(side='left', padx=5)

        self.entries = {} 
        self.lista = []   

    def limpiar(self):
        """
        Restaura el formulario a su estado inicial para crear una nueva rutina.
        """
        self.nombre.set("")
        self._entry.delete(0, tk.END)
        self._entry.insert(0, "Nombre de la rutina")
        self._entry.config(fg='grey')
        self.lista.clear()
        self.lst_ejercicios.delete(0, tk.END)
        self.tipo_var.set("")
        self.subtipo_var.set("")
        self._limpiar_campos()

    def _clear_placeholder(self, entry):
        """
        Elimina el texto de marcador cuando el campo gana foco.
        Args:
            entry: Campo de entrada (tk.Entry) a limpiar.
        """
        if entry.get() == "Nombre de la rutina":
            entry.delete(0, tk.END)
            entry.config(fg='white')

    def _set_placeholder(self, entry):
        """
        Restaura el marcador de texto si el campo está vacío al perder foco.
        Args:
            entry: Campo de entrada (tk.Entry).
        """
        if not entry.get():
            entry.insert(0, "Nombre de la rutina")
            entry.config(fg='grey')

    def _on_tipo_seleccionado(self, event=None):
        """
        Carga los subtipos disponibles según el tipo seleccionado y limpia los campos.
        """
        tipo = self.tipo_var.get()
        subtipos = self.controller.controlador.obtener_subtipos(tipo)
        self.subtipo_cb.config(values=subtipos)
        self.subtipo_var.set("")
        self._limpiar_campos()

    def _on_subtipo_seleccionado(self, event=None):
        """
        Carga dinámicamente los campos necesarios para el subtipo seleccionado.
        """
        self._limpiar_campos()
        tipo = self.tipo_var.get()
        subtipo = self.subtipo_var.get()
        campos = self.controller.controlador.obtener_campos_para(tipo, subtipo)
        for i, campo in enumerate(campos):
            lbl = ttk.Label(self.campos_frame, text=campo + ":")
            lbl.grid(row=i, column=0, sticky='w', padx=5, pady=2)
            ent = ttk.Entry(self.campos_frame)
            ent.grid(row=i, column=1, sticky='ew', padx=5, pady=2)
            self.entries[campo] = ent
        self.campos_frame.columnconfigure(1, weight=1)

    def _limpiar_campos(self):
        """
        Elimina todos los campos dinámicos actuales del formulario.
        """
        for widget in self.campos_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

    def _agregar(self):
        """
        Valida los campos y agrega un nuevo ejercicio a la rutina en construcción.
        """
        tipo = self.tipo_var.get()
        subtipo = self.subtipo_var.get()
        if not tipo or not subtipo:
            messagebox.showwarning("Atención", "Seleccione tipo y subtipo.")
            return
        datos = {}
        for campo, entry in self.entries.items():
            valor = entry.get().strip()
            if not valor:
                messagebox.showwarning("Atención", f"El campo '{campo}' no puede estar vacío.")
                return
            datos[campo] = valor

        ejercicio = self.controller.controlador.crear_ejercicio(tipo, subtipo, datos)
        self.lista.append(ejercicio)
        self.lst_ejercicios.insert(tk.END, ejercicio.nombre_ejercicio)
        messagebox.showinfo("Ejercicio agregado", f"{ejercicio.nombre_ejercicio} agregado.")

        self.tipo_var.set("")
        self.subtipo_var.set("")
        self._limpiar_campos()

    def _guardar(self):
        """
        Guarda la rutina con los ejercicios agregados y vuelve al menú.
        """
        nom = self.nombre.get().strip()
        if nom == "Nombre de la rutina" or not nom:
            messagebox.showwarning("Atención", "El nombre no puede estar vacío.")
            return
        if not self.lista:
            messagebox.showwarning("Atención", "Agrega al menos un ejercicio.")
            return
        self.controller.controlador.crear_rutina(nom, self.lista)
        messagebox.showinfo("Éxito", f"Rutina '{nom}' creada.")
        self.lista.clear()
        self.lst_ejercicios.delete(0, tk.END)
        self.controller.mostrar_menu()

class RealizarFrame(tk.Frame):
    """
    Pantalla que permite ejecutar paso a paso los ejercicios de una rutina seleccionada.
    Incluye control de series, descansos, y visualización de progreso.
    """

    def __init__(self, parent, controller):
        """
        Inicializa la interfaz de ejecución de rutina, con etiquetas, botones y barras de progreso.
        Args:
            parent: Contenedor padre.
            controller: Controlador principal para volver al menú o manejar eventos.
        """
        super().__init__(parent)
        self.controller = controller

        self.lbl = tk.Label(self, text="", font=('Arial', 18))
        self.lbl.pack(pady=10)

        self.lbl_serie = tk.Label(self, text="", font=('Arial', 14))
        self.lbl_serie.pack(pady=5)

        self.detalle = tk.Label(self, text="", justify="center", anchor="center")
        self.detalle.pack(pady=10, fill="both")

        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=5)
        self.progress["value"] = 0
        self.progress.pack_forget()

        self.lbl_descanso = tk.Label(self, text="", font=('Arial', 16), fg="red")
        self.lbl_descanso.pack(pady=5)
        self.lbl_descanso.pack_forget()

        self.btn_siguiente = tk.Button(self, text="Siguiente", command=self._avanzar)
        self.btn_siguiente.pack(pady=5)

        tk.Button(self, text="Cancelar", command=controller.mostrar_menu).pack(pady=5)

        self.rutina_terminada = False
        self.descanso_activo = False
        self.after_id = None  

    def iniciar_rutina(self, rutina):
        """
        Inicia la ejecución de la rutina recibida, preparando el primer ejercicio.
        Args:
            rutina: Rutina a ejecutar.
        """
        self.rutina = rutina
        self.ejs = rutina.ejercicios[:]
        self.idx = 0
        self.serie_actual = 1
        self.rutina_terminada = False
        self.descanso_activo = False
        self.after_id = None
        self._mostrar_actual()

    def _mostrar_actual(self):
        """
        Muestra en pantalla el ejercicio actual, incluyendo descripción y estado de series.
        """
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.progress.pack_forget()
        self.lbl_descanso.pack_forget()
        self.descanso_activo = False

        if self.idx >= len(self.ejs):
            self._finalizar_rutina()
            return

        ej = self.ejs[self.idx]
        self.lbl.config(text=f"Ejercicio {self.idx+1}/{len(self.ejs)}: {ej.nombre_ejercicio}")

        if hasattr(ej, "sets"):
            total_series = ej.sets
            self.lbl_serie.config(text=f"Serie {self.serie_actual}/{total_series}")
        else:
            self.lbl_serie.config(text="")

        if hasattr(ej, "descripcion_lineas"):
            desc_str = "\n".join(ej.descripcion_lineas())
        else:
            desc_str = ej.descripcion()
        self.detalle.config(text=desc_str)

        self.btn_siguiente.config(state="normal")

    def _avanzar(self):
        """
        Avanza a la siguiente serie o ejercicio según corresponda, considerando los descansos.
        """
        if self.descanso_activo:
            return

        if self.rutina_terminada:
            return

        self.btn_siguiente.config(state="disabled")

        ej = self.ejs[self.idx]
        descanso = getattr(ej, "descanso", 0)
        self._iniciar_descanso(descanso)

    def _iniciar_descanso(self, minutos):
        """
        Inicia un temporizador de descanso visual si el ejercicio lo requiere.
        Args:
            minutos (int): Tiempo de descanso en minutos.
        """
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

        ej = self.ejs[self.idx]
        es_ultima_serie = not hasattr(ej, "sets") or self.serie_actual >= ej.sets
        es_ultimo_ejercicio = self.idx == len(self.ejs) - 1

        if minutos == 0:
            if es_ultimo_ejercicio and es_ultima_serie:
                self._avanzar_despues_de_descanso()
                return

            self.progress.pack()
            self.lbl_descanso.pack()
            self.progress["maximum"] = 1
            self.progress["value"] = 1
            self.lbl_descanso.config(text="DESCANSA - 0 seg")
            self.descanso_activo = True
            self.after_id = self.after(1000, self._ocultar_descanso_y_avanzar)
            return

        self.descanso_activo = True
        total_segundos = 2

        self.progress.pack()
        self.lbl_descanso.pack()
        self.progress["maximum"] = total_segundos
        self.progress["value"] = 0
        self._actualizar_barra(0, total_segundos)


    def _actualizar_barra(self, segundos_transcurridos, total_segundos):
        """
        Actualiza la barra de progreso durante el descanso.
        Args:
            segundos_transcurridos (int): Tiempo transcurrido.
            total_segundos (int): Duración total del descanso.
        """
        if not self.descanso_activo:
            return

        segundos_restantes = total_segundos - segundos_transcurridos

        if segundos_restantes <= 0:
            self.progress["value"] = total_segundos
            self.lbl_descanso.config(text="DESCANSA - 0 seg")
            self.after_id = self.after(1000, self._ocultar_descanso_y_avanzar)
            return

        self.progress["value"] = segundos_transcurridos
        self.lbl_descanso.config(text=f"DESCANSA - {segundos_restantes} seg")
        self.after_id = self.after(1000, lambda: self._actualizar_barra(segundos_transcurridos + 1, total_segundos))

    def _ocultar_descanso_y_avanzar(self):
        """
        Oculta elementos de descanso y avanza al siguiente paso del ejercicio.
        """
        self.progress.destroy()
        self.lbl_descanso.destroy()

        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress["value"] = 0
        self.progress.pack(pady=5)
        self.progress.pack_forget()

        self.lbl_descanso = tk.Label(self, text="", font=('Arial', 16), fg="red")
        self.lbl_descanso.pack(pady=5)
        self.lbl_descanso.pack_forget()

        self.descanso_activo = False
        self.after_id = None
        self._avanzar_despues_de_descanso()

    def _avanzar_despues_de_descanso(self):
        """
        Lógica que decide si continuar con otra serie o pasar al siguiente ejercicio.
        """
        if self.rutina_terminada:
            return
        ej = self.ejs[self.idx]
        if hasattr(ej, "sets") and self.serie_actual < ej.sets:
            self.serie_actual += 1
        else:
            self.idx += 1
            self.serie_actual = 1

        if self.idx >= len(self.ejs):
            self._finalizar_rutina()
            return
        self._mostrar_actual()


    def _finalizar_rutina(self):
        """
        Finaliza la rutina actual, muestra calorías estimadas y vuelve al menú.
        """
        self.rutina_terminada = True
        total_calorias = self.controller.controlador.calorias_estimadas_rutina(self.rutina)
        messagebox.showinfo("¡Fin!", f"Rutina completada.\n🔥 Calorías estimadas: {total_calorias:.2f} kcal")
        self.controller.mostrar_menu()
        self.btn_siguiente.config(state="disabled")
