listas_de_campos = {
    "Categorias": ["_id", "nombre","grad", "descripcion", "tipo", "estado"],
    "Sub_categoria": ["_id", "nombre","categoria_principal", "descripcion", "tipo", "estado"],
    "Micro_categoria": ["_id", "nombre","sub_categoria", "descripcion", "tipo", "estado"],
    "Nano_categoria": ["_id", "nombre","micro_categoria", "descripcion", "tipo", "estado"],
    "Preguntas":["_id","pregunta","opciones","respuesta_correcta","categoria", "usuario_carga", "tipo", "estado"]
}   
