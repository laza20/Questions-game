def sub_categoria_schema(sub_categoria)->dict:
    return{
        "id"                  : str(sub_categoria["_id"]),
        "nombre"              : str(sub_categoria["nombre"]),
        "descripcion"         : str(sub_categoria["descripcion"]),
        "categoria_principal" : str(sub_categoria["categoria_principal"]),
        "tipo"                : str(sub_categoria["tipo"]),
        "estado"              : bool(sub_categoria["estado"])       
    }
    
def sub_categorias_schema(sub_categorias)->list:
    return [sub_categoria_schema(sub_categoria) for sub_categoria in sub_categorias]