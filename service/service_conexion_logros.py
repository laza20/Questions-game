from db.client import db_client
from utils import db_helpers

def orquestador_logros(current_user, evento, datos_evento):
    usuario_actualizado = db_client.Usuarios.find_one({"_id":current_user["_id"]})
    if evento == "pregunta_respondida":
        if datos_evento.get("respuesta_acertada") == "CORRECTA":
            
            campo_categoria        = _obtener_campo_categoria(datos_evento)
            campo_dificultad_final = _obtener_campo_nivel(datos_evento)
            
            verificador_preguntas_correctas(usuario_actualizado)
            logros_niveles(usuario_actualizado, campo_dificultad_final)
            logros_categorias(usuario_actualizado, campo_categoria)
            logros_puntos(usuario_actualizado)


def logros_puntos(current_user):
    """
    Funcion encargada de obtener:
    los puntos totales de un usuario (stats).
    los logros de condicion.tipo: puntos_totales
    """
    logros_nivel = list(db_client.Logros.find({"condicion.tipo": "puntos_totales"}))
    contador = current_user["stats"]["puntos_xp"]
    otorgar_logro(current_user, logros_nivel, contador)
    return current_user

def logros_niveles(current_user, campo_dificultad):
    """
    Funcion encargada de obtener:
    las preguntas correctas del usuario de un nivel determinado.
    los logros de condicion.tipo: ejemplo: preguntas_facil_correctas.
    """
    logros_nivel = list(db_client.Logros.find({"condicion.tipo": campo_dificultad}))
    contador = current_user["progreso"].get(campo_dificultad, 0)
    otorgar_logro(current_user, logros_nivel, contador)
    return current_user



def logros_categorias(current_user, campo_categoria):
    """
    Funcion encargada de obtener:
    las preguntas correctas del usuario en una categoria.
    los logros de condicion.tipo: ejemplo: preguntas_historia_correctas.
    """
    logros_por_categoria = list(db_client.Logros.find({"condicion.tipo": campo_categoria.replace("progreso.", "")}))
    campo_categoria_key = campo_categoria.replace("progreso.", "")
    contador = current_user["progreso"].get(campo_categoria_key, 0)
    otorgar_logro(current_user, logros_por_categoria, contador)
    return current_user

def verificador_preguntas_correctas(current_user):
    """
    Funcion encargada de obtener:
    las preguntas correctas del usuario.
    los logros de condicion.tipo: preguntas_correctas.
    """
    logros = list(db_client.Logros.find({"condicion.tipo": "preguntas_correctas"}))
    contador = current_user["progreso"]["preguntas_correctas"]
    otorgar_logro(current_user, logros, contador)
    return current_user



def otorgar_logro(current_user, logros, contador):
    """
    Funcion encargada de verificar si se cumple un logro y en caso afirmativo cargarlo en la base de datos
    del usuario.
    """
    user_logros = set(str(l) for l in current_user.get("logros", []))
    for logro in logros:
        if str(logro["_id"]) not in user_logros and logro["condicion"]["valor"] <= contador:
            current_user["logros"].append(logro["_id"])


    db_client.Usuarios.update_one(
    {"_id": current_user["_id"]},
    {"$set": {"logros": current_user["logros"]}}
    )
    return current_user

 
def _obtener_campo_categoria(datos_evento):
    """
    Funcion encargada de recibir los datos, y devolver el campo de la categoria que se va a utilizar.
    ejemplo de return: progreso.preguntas_deportes_correctas
    """
    if datos_evento["categoria_id"]:
        id_categoria = db_helpers.get_categoria_id(datos_evento["categoria_id"])
        categoria_principal = db_helpers.identificar_categoria_con_graphlookup(id_categoria)
        nombre_categoria_principal = categoria_principal["nombre"]
    
    if categoria_principal:
        campo_categoria = f"progreso.preguntas_{nombre_categoria_principal}_correctas"
        
    return campo_categoria
    
def _obtener_campo_nivel(datos_evento):
    """
    Funcion encargada de recibir los datos, y devolver el campo del nivel que se va a utilizar.
    ejemplo de return: progreso.preguntas_muy_facil_correctas
    ejemplo de return: progreso.preguntas_facil_correctas
    """
    dificultad = datos_evento.get("nivel")
    if dificultad:
        campo_dificultad_normalizado = db_helpers.verificador_nivel(dificultad)
        campo_dificultad_final = f"preguntas_{campo_dificultad_normalizado}_correctas"
        
    return campo_dificultad_final