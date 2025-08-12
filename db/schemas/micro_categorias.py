def micro_categoria_schema(sub_categoria)->dict:
    return{
        "id"                  : str(sub_categoria["_id"]),
        "nombre"              : str(sub_categoria["nombre"]),
        "descripcion"         : str(sub_categoria["descripcion"]),
        "sub_categoria"       : str(sub_categoria["sub_categoria"]),
        "tipo"                : str(sub_categoria["tipo"]),
        "estado"              : bool(sub_categoria["estado"])       
    }
    
def micro_categorias_schema(micro_categorias)->list:
    return [micro_categoria_schema(micro_categoria) for micro_categoria in micro_categorias]