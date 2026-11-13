import tkinter as tk
from tkinter import messagebox

usuarios = []

preguntas = [
    {
        "pregunta": "1) ¿Te gusta el amanecer o el atardecer?",
        "opciones": ["Amanecer", "Atardecer"],
        "puntos": {
            0: {"Gryffindor": 1, "Ravenclaw": 1},
            1: {"Hufflepuff": 1, "Slytherin": 1}
        }
    },
    {
        "pregunta": "2) Cuando muera, quiero que me recuerden como:",
        "opciones": [
            "Una persona buena",
            "Una persona grandiosa",
            "Una persona sabia",
            "Una persona valiente"
        ],
        "puntos": {
            0: {"Hufflepuff": 2},
            1: {"Slytherin": 2},
            2: {"Ravenclaw": 2},
            3: {"Gryffindor": 2}
        }
    },
    {
        "pregunta": "3) ¿Qué instrumento musical te gusta más?",
        "opciones": [
            "El violín",
            "La trompeta",
            "El piano",
            "El tambor"
        ],
        "puntos": {
            0: {"Slytherin": 4},
            1: {"Hufflepuff": 4},
            2: {"Ravenclaw": 4},
            3: {"Gryffindor": 4}
        }
    }
]

casas = ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]

ventana = tk.Tk()
ventana.title("El Sombrero Seleccionador")
ventana.geometry("600x500")
ventana.resizable(False, False)
ventana.configure(bg="#1c1c2e")

puntuaciones = {}
pregunta_actual = 0
nombre_usuario = ""

titulo = tk.Label(
    ventana,
    text="HOGWARTS",
    font=("Georgia", 28, "bold"),
    fg="#f5d76e",
    bg="#1c1c2e"
)
titulo.pack(pady=20)

etiqueta_pregunta = tk.Label(
    ventana,
    text="¡Bienvenido a Hogwarts!",
    font=("Arial", 15),
    fg="white",
    bg="#1c1c2e",
    wraplength=520
)
etiqueta_pregunta.pack(pady=20)

entrada_nombre = tk.Entry(
    ventana,
    font=("Arial", 14),
    justify="center"
)
entrada_nombre.pack(pady=10)

marco_botones = tk.Frame(ventana, bg="#1c1c2e")
marco_botones.pack(pady=15)

etiqueta_info = tk.Label(
    ventana,
    text="Descubre a qué casa de Hogwarts perteneces.",
    font=("Arial", 11),
    fg="#cccccc",
    bg="#1c1c2e"
)
etiqueta_info.pack(pady=10)


def limpiar_botones():
    for elemento in marco_botones.winfo_children():
        elemento.destroy()


def crear_boton(texto, funcion):
    boton = tk.Button(
        marco_botones,
        text=texto,
        command=funcion,
        font=("Arial", 12),
        width=30,
        bg="#37375c",
        fg="white",
        activebackground="#555580",
        activeforeground="white",
        cursor="hand2"
    )
    boton.pack(pady=5)


def comenzar_juego():
    global nombre_usuario, puntuaciones, pregunta_actual

    nombre_usuario = entrada_nombre.get().strip()

    if not nombre_usuario:
        messagebox.showwarning(
            "Aviso",
            "¡Por favor, introduce tu nombre!"
        )
        return

    puntuaciones = {casa: 0 for casa in casas}
    pregunta_actual = 0

    entrada_nombre.pack_forget()
    etiqueta_info.config(text="¡Selecciona una respuesta!")

    mostrar_pregunta()


def mostrar_pregunta():
    global pregunta_actual

    limpiar_botones()

    if pregunta_actual >= len(preguntas):
        mostrar_resultado()
        return

    pregunta = preguntas[pregunta_actual]

    etiqueta_pregunta.config(text=pregunta["pregunta"])

    for indice, opcion in enumerate(pregunta["opciones"]):
        crear_boton(
            f"{indice + 1}) {opcion}",
            lambda i=indice: responder_pregunta(i)
        )


def responder_pregunta(respuesta):
    global pregunta_actual

    pregunta = preguntas[pregunta_actual]
    puntos = pregunta["puntos"][respuesta]

    for casa, puntos_obtenidos in puntos.items():
        puntuaciones[casa] += puntos_obtenidos

    pregunta_actual += 1
    mostrar_pregunta()


def mostrar_resultado():
    limpiar_botones()

    puntuacion_maxima = max(puntuaciones.values())

    ganadoras = [
        casa for casa, puntos in puntuaciones.items()
        if puntos == puntuacion_maxima
    ]

    resultado = " / ".join(ganadoras)

    usuarios.append({
        "nombre": nombre_usuario,
        "casa": resultado,
        "puntuaciones": puntuaciones.copy()
    })

    etiqueta_pregunta.config(
        text=f"¡Felicidades, {nombre_usuario}!\n\n"
             f"Tu casa de Hogwarts es:\n\n{resultado}"
    )

    texto_puntuaciones = "\n".join(
        f"{casa}: {puntuaciones[casa]}"
        for casa in casas
    )

    etiqueta_info.config(
        text=f"Tus puntuaciones:\n{texto_puntuaciones}"
    )

    crear_boton("Volver a jugar", reiniciar_juego)
    crear_boton("Ver todos los jugadores", mostrar_usuarios)
    


def reiniciar_juego():
    global pregunta_actual

    limpiar_botones()
    pregunta_actual = 0

    entrada_nombre.delete(0, tk.END)
    entrada_nombre.pack(pady=10)

    etiqueta_pregunta.config(
        text="¡Bienvenido a Hogwarts!"
    )

    etiqueta_info.config(
        text="Descubre a qué casa de Hogwarts perteneces. Poner tu nombre."
    )

    crear_boton("Comenzar", comenzar_juego)


def mostrar_usuarios():
    if not usuarios:
        messagebox.showinfo(
            "Jugadores",
            "Todavía no hay jugadores."
        )
        return

    texto = ""

    for usuario in usuarios:
        texto += (
            f"Nombre: {usuario['nombre']}\n"
            f"Casa: {usuario['casa']}\n\n"
        )

    messagebox.showinfo("Todos los jugadores", texto)


crear_boton("Comenzar", comenzar_juego)

ventana.mainloop()