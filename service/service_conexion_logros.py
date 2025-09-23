from db.client import db_client
from utils import db_helpers
from bson.objectid import ObjectId

def orquestador_logros(current_user, evento, datos_evento):
    usuario_actualizado = db_client.Usuarios.find_one({"_id":current_user["_id"]})
    if evento == "pregunta_respondida":
        if datos_evento.get("respuesta_acertada") == "CORRECTA":
            logros_preguntas(usuario_actualizado)
            logros_puntos(usuario_actualizado)
            logros_nivel_usuario(usuario_actualizado)

def logros_nivel_usuario(current_user):
    """
    Funcion encargada de obtener:
    el nivel del usuario.
    verificar los logros de condicion.tipo: nivel
    """
    logros_por_nivel_usuario = [
        logro for logro in db_client.Logros.find({"condicion.tipo": "nivel"})
        if logro["condicion"]["valor"] != "maximo"
        ]
    contador = current_user["stats"]["nivel"]
    otorgar_logro(current_user, logros_por_nivel_usuario, contador)
    return current_user

def logros_puntos(current_user):
    """
    Funcion encargada de obtener:
    los puntos totales de un usuario (stats).
    los logros de condicion.tipo: puntos_totales
    """
    logros_de_puntos = list(db_client.Logros.find({"condicion.tipo": "puntos_totales"}))
    contador = current_user["stats"]["puntos_xp"]
    otorgar_logro(current_user, logros_de_puntos, contador)
    return current_user

def logros_preguntas(current_user):
    """
    Funcion encargada de cargar todos los logros de preguntas.
    """
    logros = list(db_client.Logros.find({"condicion.tipo": {"$regex": "^preguntas_.*"}}))
    user_logros = set(str(l) for l in current_user.get("logros", []))
    logros_nuevos = []
    for logro in logros:
        condicion = logro["condicion"]["tipo"]
        if logro["condicion"]["tipo"] != "maximo" and condicion != "preguntas_creadas":
            if logro["_id"] not in user_logros and logro["condicion"]["valor"] <= current_user["progreso"][condicion]:
                logros_nuevos.append(logro["_id"])
                current_user["logros"].append(ObjectId(logro["_id"]))

    if logros_nuevos:
        db_client.Usuarios.update_one(
            {"_id": current_user["_id"]},
            {"$addToSet": {"logros": {"$each": logros_nuevos}}}
        )
                    
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

 
