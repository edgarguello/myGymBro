import tkinter as tk
from tkinter import messagebox, ttk

class VistaGrafica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.controlador = None  
        self.title("MyGymBro")
        self.geometry("600x400")
        self._init_frames()
        self.mostrar_menu()

    def set_controlador(self, controlador):
        self.controlador = controlador

    def _init_frames(self):
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
        self.normalizar()
        self._show_frame("MenuFrame")

    def mostrar_seleccionar(self):
        f = self.frames["SeleccionFrame"]
        f.actualizar_lista(self.controlador.obtener_rutinas())
        f.on_eliminar = self.eliminar_rutina
        self.normalizar()
        self._show_frame("SeleccionFrame")

    def mostrar_crear(self):
        form = self.frames["CrearFrame"]
        form.limpiar()
        self.maximizar()
        self._show_frame("CrearFrame")

    def mostrar_realizar(self, rutina):
        form = self.frames["RealizarFrame"]
        form.iniciar_rutina(rutina)
        self.normalizar()
        self._show_frame("RealizarFrame")

    def _show_frame(self, name):
        for f in self.frames.values():
            f.pack_forget() 
            f.grid_remove()
        frame = self.frames[name]
        frame.grid()
        frame.tkraise()
    
    def eliminar_rutina(self, rutina):
        self.controlador.eliminar_rutina(rutina)
        self.mostrar_seleccionar()  # Refresca la lista

    def maximizar(self):
        try:
            self.state('zoomed') 
        except Exception:
            try:
                self.attributes('-zoomed', True) 
            except Exception:
                pass 

    def normalizar(self):
        self.state('normal')

    def mostrar_error(self, mensaje: str):
        messagebox.showerror("Error", mensaje)


class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Menú Principal", font=('Arial', 18)).pack(pady=20)
        tk.Button(self, text="Seleccionar rutina", width=20,
                  command=controller.mostrar_seleccionar).pack(pady=5)
        tk.Button(self, text="Crear rutina", width=20,
                  command=controller.mostrar_crear).pack(pady=5)
        tk.Button(self, text="Salir", width=20,
                  command=controller.destroy).pack(pady=5)

class SeleccionFrame(tk.Frame):
    def __init__(self, parent, controller):
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
        self.lst.delete(0, tk.END)
        self._rutinas = rutinas
        for r in rutinas:
            descripcion = f"{r.nombre} ({len(r.ejercicios)} ejercicios)"
            self.lst.insert(tk.END, descripcion)

    def _realizar(self, controller):
        sel = self.lst.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una rutina.")
            return
        rutina = self._rutinas[sel[0]]
        controller.mostrar_realizar(rutina)

    def _mostrar_detalle(self):
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
        sel = self.lst.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una rutina para eliminar.")
            return
        rutina = self._rutinas[sel[0]]
        confirm = messagebox.askyesno("Confirmar", f"¿Deseas eliminar la rutina '{rutina.nombre}'?")
        if confirm:
            self.on_eliminar(rutina)

class CrearFrame(tk.Frame):
    def __init__(self, parent, controller):
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
        if entry.get() == "Nombre de la rutina":
            entry.delete(0, tk.END)
            entry.config(fg='white')

    def _set_placeholder(self, entry):
        if not entry.get():
            entry.insert(0, "Nombre de la rutina")
            entry.config(fg='grey')

    def _on_tipo_seleccionado(self, event=None):
        tipo = self.tipo_var.get()
        subtipos = self.controller.controlador.obtener_subtipos(tipo)
        self.subtipo_cb.config(values=subtipos)
        self.subtipo_var.set("")
        self._limpiar_campos()

    def _on_subtipo_seleccionado(self, event=None):
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
        for widget in self.campos_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

    def _agregar(self):
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
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.lbl = tk.Label(self, text="", font=('Arial', 18))
        self.lbl.pack(pady=10)
        self.detalle = tk.Label(self, text="", justify="left")
        self.detalle.pack(pady=10)
        self.btn_siguiente = tk.Button(self, text="Siguiente", command=self.siguiente)
        self.btn_siguiente.pack(pady=5)
        tk.Button(self, text="Cancelar", command=controller.mostrar_menu).pack(pady=5)

    def iniciar_rutina(self, rutina):
        self.rutina = rutina
        self.ejs = lista = rutina.ejercicios[:]  # copia
        self.idx = 0
        self._mostrar_actual()

    def _mostrar_actual(self):
        if self.idx < len(self.ejs):
            ej = self.ejs[self.idx]
            self.lbl.config(text=f"Ejercicio {self.idx+1}/{len(self.ejs)}: {ej.nombre_ejercicio}")
            self.detalle.config(text=ej.descripcion())
        else:
            messagebox.showinfo("¡Fin!", "Rutina completada.")
            self.controller.mostrar_menu()

    def siguiente(self):
        # Aquí puedes añadir temporizador o lógica
        self.idx += 1
        self._mostrar_actual()
