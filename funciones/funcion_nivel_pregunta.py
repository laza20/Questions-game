from fastapi import HTTPException, status

def cargar_nivel_pregunta(puntos):
    if puntos == 0:
        nivel = "Muy facil"
    elif puntos > 0 and puntos < 400:
        nivel = "Facil"
    elif puntos >= 400 and puntos < 700:
        nivel = "Medio"
    elif puntos >= 700 and puntos < 900:
        nivel = "Dificil"
    elif puntos >= 900 and puntos < 1000:
        nivel = "Imposible"
    elif puntos == 1000:
        nivel = "Infinito"
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Los puntos se encuentran en una categoria indefinida. Cantidad de puntos de la pregunta: {puntos}")
    
    return nivel
    
    
def cargar_muchos_niveles_de_preguntas(lista_puntos: list[int]) -> list[str]:
    return [cargar_nivel_pregunta(puntos) for puntos in lista_puntos]
        