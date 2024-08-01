class BKTreeNode:
    def __init__(self, palabra):
        self.palabra = palabra
        self.hijos = {}

    def agregar(self, palabra, funcion_distancia):
        distancia = funcion_distancia(self.palabra, palabra)
        if distancia in self.hijos:
            self.hijos[distancia].agregar(palabra, funcion_distancia)
        else:
            self.hijos[distancia] = BKTreeNode(palabra)

    def buscar(self, palabra, max_distancia, funcion_distancia):
        resultados = []
        distancia = funcion_distancia(self.palabra, palabra)
        if distancia <= max_distancia:
            resultados.append(self.palabra)

        for dist in range(max(1, distancia - max_distancia), distancia + max_distancia + 1):
            hijo = self.hijos.get(dist)
            if hijo:
                resultados.extend(hijo.buscar(palabra, max_distancia, funcion_distancia))

        return resultados


class BKTree:
    def __init__(self, funcion_distancia):
        self.funcion_distancia = funcion_distancia
        self.raiz = None

    def insertar(self, palabra):
        if not self.raiz:
            self.raiz = BKTreeNode(palabra)
        else:
            self.raiz.agregar(palabra, self.funcion_distancia)

    def buscar(self, palabra, max_distancia):
        if not self.raiz:
            return []
        return self.raiz.buscar(palabra, max_distancia, self.funcion_distancia)


def distancia_levenshtein(palabra1, palabra2):
    len1, len2 = len(palabra1), len(palabra2)
    if len1 < len2:
        palabra1, palabra2 = palabra2, palabra1
        len1, len2 = len2, len1

    if len2 == 0:
        return len1

    prev_row = list(range(len2 + 1))
    for i, c1 in enumerate(palabra1):
        curr_row = [i + 1]
        for j, c2 in enumerate(palabra2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row

    return prev_row[-1]
