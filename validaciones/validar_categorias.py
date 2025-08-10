from fastapi import HTTPException, status
from validaciones_generales import validaciones_simples
from errores_generales import errores_simples


def validacion_carga_categoria(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        categorias = set()
        for dato in datos:
            key = validacion_carga_categoria_2(dato, base_de_datos)
            validar_carga_repetida(key, categorias, dato, base_de_datos)
            categorias.add(key)   
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        key = validacion_carga_categoria_2(dato, base_de_datos)
            
def validar_carga_repetida(key, categorias, dato, base_de_datos):
    if key in categorias:
       errores_simples.error_carga_repetida_un_solo_dato(dato.nombre_categoria, base_de_datos)
            
def validacion_carga_categoria_2(dato, base_de_datos):
    key = create_key(dato)
    validaciones_simples.validacion_simple_general(base_de_datos, dato.nombre_categoria)
    validaciones_simples.validacion_simple_general(base_de_datos, dato.descripcion)
    return key

def create_key(dato):
    key = (dato.nombre_categoria.lower())   
    return key