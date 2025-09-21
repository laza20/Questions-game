from db.client import db_client

def orquestador_logros(current_user, evento, datos_evento):
    """
    Funcion orquestadora, recibe, el usuario que esta jugando, 
    el evento (pregunta respondida, duelo ganado) 
    y datos del evento (categoria, respuesta)
    """
    if evento == "pregunta_respondida":
        es_correcta = datos_evento.get("es_correcta", False)
        categoria   = datos_evento.get("categoria")
        dificultad  = datos_evento.get("dificultad")

    if es_correcta:
        db_client.Usuarios.update_one(
        {"_id": current_user["_id"]},
        {"$inc": {"progreso.preguntas_correctas": 1}}
        )

    if categoria:
        campo_categoria = f"progreso.preguntas_{categoria}_correctas"
        db_client.Usuarios.update_one(
        {"_id": current_user["_id"]},
        {"$inc": {campo_categoria: 1}}
        )
    if dificultad:
        campo_dificultad = f"progreso.preguntas_{dificultad}_correctas"
        db_client.Usuarios.update_one(
        {"_id": current_user["_id"]},
        {"$inc": {campo_dificultad: 1}}
        )

    usuario_actualizado = db_client.Usuarios.find_one({"_id": current_user["_id"]})

    verificador_preguntas_correctas(current_user)
    _orquestador_niveles(current_user,datos_evento)


def _orquestador_niveles(current_user, datos_evento):
    nivel = datos_evento.get("nivel")
    if not nivel:
        return
    
    mapping = {
        "Muy facil": verificador_preguntas_muy_faciles_correctas,
        "Facil": verificador_preguntas_faciles_correctas,
        "Medio": verificador_preguntas_medias_correctas,
        "Dificil": verificador_preguntas_dificiles_correctas,
        "Imposible": verificador_preguntas_imposibles_correctas,
        "Infinito": verificador_preguntas_infinitas_correctas,
    }
    
    if nivel in mapping:
        mapping[nivel](current_user)

def verificador_preguntas_correctas(current_user):
    logros = list(db_client.Logros.find({"condicion.tipo": "preguntas_correctas"}))
    contador = current_user["progreso"]["preguntas_correctas"]

    otorgar_logro(current_user, logros, contador)

    return current_user

def verificador_preguntas_muy_faciles_correctas(current_user):
    logros = list(db_client.Logros.find({"condicion.tipo": "preguntas_muy_faciles_correctas"}))
    contador = current_user["progreso"]["preguntas_muy_faciles_correctas"]

    otorgar_logro(current_user, logros, contador)

    return current_user

def verificador_preguntas_faciles_correctas(current_user):
    logros = list(db_client.Logros.find({"condicion.tipo": "preguntas_faciles_correctas"}))
    contador = current_user["progreso"]["preguntas_faciles_correctas"]

    otorgar_logro(current_user, logros, contador)

    return current_user

def verificador_preguntas_medias_correctas(current_user):
    logros = list(db_client.Logros.find({"condicion.tipo": "preguntas_medias_correctas"}))
    contador = current_user["progreso"]["preguntas_medias_correctas"]

    otorgar_logro(current_user, logros, contador)

    return current_user

def verificador_preguntas_dificiles_correctas(current_user):
    logros = list(db_client.Logros.find({"condicion.tipo": "preguntas_dificiles_correctas"}))
    contador = current_user["progreso"]["preguntas_dificiles_correctas"]

    otorgar_logro(current_user, logros, contador)

    return current_user

def verificador_preguntas_imposibles_correctas(current_user):
    logros = list(db_client.Logros.find({"condicion.tipo": "preguntas_imposibles_correctas"}))
    contador = current_user["progreso"]["preguntas_imposibles_correctas"]

    otorgar_logro(current_user, logros, contador)

    return current_user

def verificador_preguntas_infinitas_correctas(current_user):
    logros = list(db_client.Logros.find({"condicion.tipo": "preguntas_infinito_correctas"}))
    contador = current_user["progreso"]["preguntas_infinito_correctas"]

    otorgar_logro(current_user, logros, contador)

    return current_user


def otorgar_logro(current_user, logros, contador):
    user_logros = set(str(l) for l in current_user.get("logros", []))
    for logro in logros:
        if str(logro["_id"]) not in user_logros and logro["condicion"]["valor"] <= contador:
            current_user["logros"].append(logro["_id"])


    db_client.Usuarios.update_one(
    {"_id": current_user["_id"]},
    {"$set": {"logros": current_user["logros"]}}
    )
    return current_user
 