def puntos_por_nivel_pregunta(nivel_pregunta):
    if nivel_pregunta == "Muy facil":
        puntos_positivos = 2
        puntos_negativos = -6
    if nivel_pregunta == "Facil":
        puntos_positivos = 3
        puntos_negativos = -5
    if nivel_pregunta == "Medio":
        puntos_positivos = 5
        puntos_negativos = -4
    if nivel_pregunta == "Dificil":
        puntos_positivos = 7
        puntos_negativos = -2      
    if nivel_pregunta == "Imposible":
        puntos_positivos = 9
        puntos_negativos = -1        
    if nivel_pregunta == "Infinito":
        puntos_positivos = 10
        puntos_negativos = -1
        
    return puntos_positivos, puntos_negativos