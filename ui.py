import tkinter as tk
from tkinter import messagebox
from classifier import ClasificadorDeTexto


class App:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Clasificador de Texto BKTree")
        self.ventana.geometry("400x400")

        self.clasificador = ClasificadorDeTexto()

        self.etiqueta = tk.Label(self.ventana, text="Ingrese un texto o palabra clave:")
        self.etiqueta.pack(pady=10)

        self.entrada = tk.Entry(self.ventana)
        self.entrada.pack(pady=5)

        self.boton_clasificar = tk.Button(self.ventana, text="Clasificar Texto", command=self.clasificar_texto)
        self.boton_clasificar.pack(pady=5)

        self.boton_tweets = tk.Button(self.ventana, text="Buscar Tweets", command=self.buscar_tweets)
        self.boton_tweets.pack(pady=5)

        self.boton_graficos = tk.Button(self.ventana, text="Mostrar Gráficos", command=self.mostrar_graficos)
        self.boton_graficos.pack(pady=5)

        self.etiqueta_resultado = tk.Label(self.ventana, text="Resultado:")
        self.etiqueta_resultado.pack(pady=5)

        self.texto_resultado = tk.Text(self.ventana, height=10, width=40)
        self.texto_resultado.pack(pady=10)

    def clasificar_texto(self):
        texto = self.entrada.get()
        if not texto:
            messagebox.showwarning("Advertencia", "Por favor ingrese un texto.")
            return

        resultado = self.clasificador.clasificar(texto)
        self.texto_resultado.delete(1.0, tk.END)
        self.texto_resultado.insert(tk.END, resultado)

    def buscar_tweets(self):
        query = self.entrada.get()
        if not query:
            messagebox.showwarning("Advertencia", "Por favor ingrese una palabra clave.")
            return

        tweets = self.clasificador.obtener_tweets(query)
        resultados = [f"{tweet} - {self.clasificador.clasificar(tweet)}" for tweet in tweets]

        self.texto_resultado.delete(1.0, tk.END)
        self.texto_resultado.insert(tk.END, "\n".join(resultados))

    def mostrar_graficos(self):
        textos = [
            "Me encanta este producto, es maravilloso!",
            "No me gustó para nada, fue una experiencia terrible.",
            "El servicio fue regular, no tengo mucho que decir."
        ]
        tiempos, resultados = self.clasificador.medir_rendimiento(textos)
        self.clasificador.graficar_rendimiento(tiempos)

    def run(self):
        self.ventana.mainloop()
