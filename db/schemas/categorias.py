def categoria_schema(categoria)->dict:
    return{
        "id"               : str(categoria["_id"]),
        "nombre_categoria" : str(categoria["nombre_categoria"]),
        "descripcion"      : str(categoria["descripcion"]),
        "tipo"             : str(categoria["tipo"]),
        "estado"           : bool(categoria["estado"])       
    }
    
def categorias_schema(categorias)->list:
    return [categoria_schema(categoria) for categoria in categorias]