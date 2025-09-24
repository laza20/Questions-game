from db.client import db_client
from utils import db_helpers
from bson.objectid import ObjectId

def orquestador_logros(current_user:dict, evento:str, datos_evento:dict):
    usuario_actualizado = db_client.Usuarios.find_one({"_id":current_user["_id"]})
    if evento == "pregunta_respondida":
        if datos_evento.get("respuesta_acertada") == "CORRECTA":
            logros_ranking_level(usuario_actualizado)
            logros_preguntas(usuario_actualizado)
            logros_puntos(usuario_actualizado)
            logros_nivel_usuario(usuario_actualizado)
    
    if evento == "pregunta_creada":
        logros_creacion_preguntas(usuario_actualizado)
            
            
def logros_creacion_preguntas(current_user:dict):
    """
    Función encargada de verificar las preguntas creadas por el usuario y otorgar un logro en base a esto.
    """
    logros_preguntas_creadas = list(db_client.Logros.find({"condicion.tipo": "preguntas_creadas"}))
    if current_user["nombre_usuario"] == "lazasalvi20":
        preguntas = list(db_client.Preguntas.find({"usuario_carga": "Master"}))
        preguntas_dos  = list(db_client.Preguntas.find({"usuario_carga": "lazasalvi20"}))
        contador = len(preguntas) + len(preguntas_dos)
    else:
        preguntas_usuario = list(db_client.Preguntas.find({"usuario_carga":current_user["nombre_usuario"]}))
        contador = len(preguntas_usuario)
        
    lista_logros = []
            
    for logro in logros_preguntas_creadas:
        if contador >= logro["condicion"]["valor"]:
            lista_logros.append(logro["_id"])
            current_user["logros"].append(ObjectId(logro["_id"]))
            
    if lista_logros:
        db_client.Usuarios.update_one(
            {"_id": current_user["_id"]},
            {"$addToSet": {"logros": {"$each": lista_logros}}}
        )  

def logros_ranking_level(current_user:dict):
    """
    Función encargada de verificar si el usuario es uno de los primeros en llegar a un nivel
    y otorgarle el logro de ranking.
    """
    logros_ranking = list(db_client.Logros.find({"condicion.tipo": "ranking_nivel"}))
    user_logros_set = set(str(l) for l in current_user.get("logros", []))
    logros_a_otorgar = []

    for logro in logros_ranking:
        nivel_requerido = logro["condicion"]["nivel"]
        posicion_requerida = logro["condicion"]["posicion"]

        if str(logro["_id"]) in user_logros_set:
            continue

        if current_user["stats"]["nivel"] >= nivel_requerido:
            
            usuarios_en_nivel = db_client.Usuarios.count_documents({
                "stats.nivel": {"$gte": nivel_requerido}
            })

            if usuarios_en_nivel < posicion_requerida:
                # Si es así, añade el logro a la lista
                logros_a_otorgar.append(logro["_id"])
                current_user["logros"].append(ObjectId(logro["_id"]))
                
    if logros_a_otorgar:
        db_client.Usuarios.update_one(
            {"_id": current_user["_id"]},
            {"$addToSet": {"logros": {"$each": logros_a_otorgar}}}
        )


def logros_nivel_usuario(current_user:dict):
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

def logros_puntos(current_user:dict):
    """
    Funcion encargada de obtener:
    los puntos totales de un usuario (stats).
    los logros de condicion.tipo: puntos_totales
    """
    logros_de_puntos = list(db_client.Logros.find({"condicion.tipo": "puntos_totales"}))
    contador = current_user["stats"]["puntos_xp"]
    otorgar_logro(current_user, logros_de_puntos, contador)
    return current_user

def logros_preguntas(current_user:dict):
    """
    Funcion encargada de cargar todos los logros de preguntas.
    """
    logros = list(db_client.Logros.find({"condicion.tipo": {"$regex": "^preguntas_.*"}}))
    user_logros = set(str(l) for l in current_user.get("logros", []))
    logros_nuevos = []
    for logro in logros:
        condicion = logro["condicion"]["tipo"]
        if logro["condicion"]["tipo"] != "maximo" and condicion != "preguntas_creadas":
            if str(logro["_id"]) not in user_logros and logro["condicion"]["valor"] <= current_user["progreso"][condicion]:
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

 
