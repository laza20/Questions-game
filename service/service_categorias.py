from validaciones_generales import validaciones_simples
from errores_generales import errores_simples
from funciones import funciones_logicas
from db.client import db_client


def validacion_carga_categoria(datos, base_de_datos):
    if isinstance(datos, list) and len(datos) >= 2:
        datos = [datos]
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
       errores_simples.error_carga_repetida_un_solo_dato(dato.nombre, base_de_datos)
            
def validacion_carga_categoria_2(dato, base_de_datos):
    if dato.grado == "Primer":
        verificar_limite_categoria_principal()
        
    oid_padre = funciones_logicas.validate_object_id(dato.padre_id)
    #oid_usuario = funciones_logicas.validate_object_id(dato.creador_id)
    key = create_key(dato, oid_padre)
    validaciones_simples.validacion_simple_general(base_de_datos, dato.nombre)
    #oid_usuario = funciones_logicas.validate_object_id(dato.creador_id)
    #validaciones_simples.validacion_simple_general_negativa("Usuarios", oid_usuario)
    validaciones_simples.validacion_simple_general(base_de_datos, dato.descripcion)
    validaciones_simples.validacion_simple_general_negativa(base_de_datos, oid_padre)
    return key

def verificar_limite_categoria_principal():
    cantidad_principal = db_client.Categorias.count_documents({"grado": "Primer"})
    if cantidad_principal >= 5:
        errores_simples.limite_de_documentos_cumplido("Primer grado", "Categorias")   

def create_key(dato, oid_padre):
    #cuando la coleccion de usuario este funcional se le deben agregar validaciones para
    #permitir que un usuario solo pueda cargar la categoria bajo ciertas normas.
    key = (dato.nombre.lower(), oid_padre)   
    return key

