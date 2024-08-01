import tweepy
from bktree import BKTree, distancia_levenshtein
from config import API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import time
import matplotlib.pyplot as plt

class ClasificadorDeTexto:
    def __init__(self):
        self.arbol_positivo = BKTree(distancia_levenshtein)
        self.arbol_negativo = BKTree(distancia_levenshtein)
        self.arbol_neutro = BKTree(distancia_levenshtein)
        self.cargar_palabras_clave()

    def cargar_palabras_clave(self):
        self._cargar_arbol("data/palabras_clave_positivas.txt", self.arbol_positivo)
        self._cargar_arbol("data/palabras_clave_negativas.txt", self.arbol_negativo)
        self._cargar_arbol("data/palabras_clave_neutras.txt", self.arbol_neutro)

    def _cargar_arbol(self, ruta_archivo, arbol):
        try:
            with open(ruta_archivo, "r") as archivo:
                for linea in archivo:
                    palabras = linea.strip().lower().split(',')  # Suponiendo palabras separadas por comas
                    for palabra in palabras:
                        arbol.insertar(palabra)
        except FileNotFoundError:
            print(f"No se encontró el archivo {ruta_archivo}.")

    def clasificar(self, texto, max_distancia=2):
        texto = texto.lower().strip()
        palabras = texto.split()

        coincidencias_positivas = sum(1 for palabra in palabras if self.arbol_positivo.buscar(palabra, max_distancia))
        coincidencias_negativas = sum(1 for palabra in palabras if self.arbol_negativo.buscar(palabra, max_distancia))
        coincidencias_neutras = sum(1 for palabra in palabras if self.arbol_neutro.buscar(palabra, max_distancia))

        # Imprimir coincidencias para depuración
        print(f"Texto: {texto}")
        print(f"Coincidencias Positivas: {coincidencias_positivas}")
        print(f"Coincidencias Negativas: {coincidencias_negativas}")
        print(f"Coincidencias Neutras: {coincidencias_neutras}")

        # Decidir la clasificación final con prioridad a negativos en caso de empate
        if coincidencias_negativas > coincidencias_positivas:
            return "Negativo"
        elif coincidencias_positivas > coincidencias_negativas:
            return "Positivo"
        elif coincidencias_neutras >= max(coincidencias_positivas, coincidencias_negativas):
            return "Neutro"
        elif coincidencias_positivas == coincidencias_negativas and coincidencias_positivas > 0:
            return "Negativo"
        else:
            return "Neutro"

    def obtener_tweets(self, query, cantidad=10):
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        try:
            tweets = api.search_tweets(q=query, count=cantidad, tweet_mode='extended', lang='es')
            return [tweet.full_text for tweet in tweets]
        except tweepy.errors.Forbidden:
            print("No tienes acceso al endpoint requerido. Verifica tus credenciales y niveles de acceso.")
            return []
        except tweepy.errors.TweepError as e:
            print(f"Error al buscar tweets: {e}")
            return []

    def medir_rendimiento(self, textos, max_distancia=2):
        tiempos = []
        resultados = []

        for texto in textos:
            inicio = time.time()
            resultado = self.clasificar(texto, max_distancia)
            fin = time.time()
            tiempos.append(fin - inicio)
            resultados.append(resultado)

        return tiempos, resultados

    def graficar_rendimiento(self, tiempos):
        plt.figure(figsize=(10, 5))
        plt.plot(tiempos, label='Tiempos de Clasificación')
        plt.xlabel('Número de Textos')
        plt.ylabel('Tiempo (segundos)')
        plt.title('Tiempo de Clasificación vs. Número de Textos')
        plt.legend()
        plt.grid(True)
        plt.show()
