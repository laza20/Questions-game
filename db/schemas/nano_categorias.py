def nano_categoria_schema(sub_categoria)->dict:
    return{
        "id"                  : str(sub_categoria["_id"]),
        "nombre"              : str(sub_categoria["nombre"]),
        "descripcion"         : str(sub_categoria["descripcion"]),
        "micro_categoria"     : str(sub_categoria["micro_categoria"]),
        "tipo"                : str(sub_categoria["tipo"]),
        "estado"              : bool(sub_categoria["estado"])       
    }
    
def nano_categorias_schema(nano_categorias)->list:
    return [nano_categoria_schema(nano_categoria) for nano_categoria in nano_categorias]