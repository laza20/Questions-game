from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# --- Esquemas de Conversión de Subdocumentos ---

def usuario_stats_schema(stats: dict) -> dict:
    """Convierte un documento de stats a un diccionario,
       manejando conversiones y valores nulos."""
    return {
        "nivel": int(stats.get("nivel", 0)) if stats.get("nivel") is not None else 0,
        "puntos_xp": int(stats.get("puntos_xp", 0)) if stats.get("puntos_xp") is not None else 0,
    }

def usuario_control_schema(control: dict) -> dict:
    """Convierte un documento de control a un diccionario,
       manejando conversiones y valores nulos."""
    return {
        "ultimo_login": control.get("ultimo_login"),
        "fecha_creacion": control.get("fecha_creacion"),
        "fecha_actualizacion": control.get("fecha_actualizacion"),
        "tipo": str(control.get("tipo", "Player")),
        "estado": bool(control.get("estado", False)),
    }
    
def usuario_preguntas_creadas_schema(pregunta: dict) -> dict:
    """Convierte un subdocumento de preguntas creadas."""
    return {
        "id_pregunta": str(pregunta.get("id_pregunta", ""))
    }

def usuario_categoria_favorita_schema(favorito: dict) -> dict:
    """Convierte un subdocumento de categoría favorita."""
    return {
        "id_categoria": str(favorito.get("id_categoria", ""))
    }

# --- Esquema de Conversión del Documento Principal ---

def usuario_total_schema(user: dict) -> dict:
    """Convierte un documento completo de usuario a un diccionario,
       manejando conversiones y subdocumentos."""
    return {
        "id": str(user["_id"]),
        "nombre_usuario": str(user.get("nombre_usuario", "")),
        "mail_usuario": str(user.get("mail_usuario", "")), # Pydantic's EmailStr is not used here
        "password_hash": str(user.get("password_hash", "")),
        "nombre": str(user.get("nombre", "")),
        "apellido": str(user.get("apellido", "")),
        "fecha_nacimiento": user.get("fecha_nacimiento"),
        "avatar_url": str(user.get("avatar_url", "")),
        "descripcion": str(user.get("descripcion", "")),
        "stats": usuario_stats_schema(user.get("stats", {})),
        "logros": [str(logro) for logro in user.get("logros", [])],
        "retos": [str(reto) for reto in user.get("retos", [])],
        "favoritos": [usuario_categoria_favorita_schema(fav) for fav in user.get("favoritos", [])],
        "preguntas": [usuario_preguntas_creadas_schema(preg) for preg in user.get("preguntas", [])],
        "control": usuario_control_schema(user.get("control", {})),
    }