from fastapi import HTTPException, status
from validaciones_generales import validaciones_simples, validaciones_dobles
from errores_generales import errores_simples


def validacion_carga_nano_categoria(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        sub_categoria_nombre      = set()
        sub_categoria_descripcion = set()
        for dato in datos:
            key, key_2 = validacion_carga_nano_categoria_2(dato, base_de_datos)
            validar_carga_repetida(key, key_2, sub_categoria_nombre, sub_categoria_descripcion, dato, base_de_datos)
            sub_categoria_nombre.add(key)
            sub_categoria_descripcion.add(key_2)   
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        key, key_2 = validacion_carga_nano_categoria_2(dato, base_de_datos)
            
def validar_carga_repetida(key,key_2, sub_categoria_nombre,sub_categoria_descripcion, dato, base_de_datos):
    if key in sub_categoria_nombre:
       errores_simples.error_carga_repetida_un_solo_dato(dato.nombre, base_de_datos)
    if key_2 in sub_categoria_descripcion:
       errores_simples.error_carga_repetida_un_solo_dato(dato.descripcion, base_de_datos)

            
def validacion_carga_nano_categoria_2(dato, base_de_datos):
    key, key_2 = create_key(dato)
    validaciones_dobles.validacion_doble_general(base_de_datos, dato.nombre, dato.micro_categoria)
    validaciones_simples.validacion_simple_general(base_de_datos, dato.descripcion)
    validaciones_simples.validacion_simple_general_negativa("Micro_categoria", dato.micro_categoria)
    return key, key_2

def create_key(dato):
    key = (dato.nombre.lower())   
    key_2 = (dato.descripcion.lower())
    return key, key_2