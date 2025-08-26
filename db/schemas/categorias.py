from datetime import datetime

def categoria_schema(categoria)->dict:
    return{
        "id"               : str(categoria["_id"]),
        "nombre_categoria" : str(categoria["nombre_categoria"]),
        "descripcion"      : str(categoria["descripcion"]),
        "padre_id"         : str(categoria["padre_id"]),
        "creador_id"       : str(categoria["creador_id"]),
        "fecha_carga"      : datetime(categoria["fecha_carga"]),
        "tipo"             : str(categoria["tipo"]),
        "estado"           : bool(categoria["estado"])       
    }
    
    
def categorias_schema(categorias)->list:
    return [categoria_schema(categoria) for categoria in categorias]