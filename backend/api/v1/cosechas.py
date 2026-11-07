from fastapi import APIRouter
from supabase import create_client

router = APIRouter()
supabase = create_client('URL', 'KEY')

@router.get('/cercanas')
async def get_nearby(lat: float, lng: float, radius_km: int = 50, producto: str = None):
    query = f"SELECT *, ST_Distance(ubicacion_acopio::geography, ST_MakePoint({lng}, {lat})::geography) as dist FROM cosechas WHERE ST_DWithin(ubicacion_acopio::geography, ST_MakePoint({lng}, {lat})::geography, {radius_km * 1000}) AND (producto ILIKE '%{producto}%' OR '{producto}' = 'Todos') ORDER BY dist ASC"
    return supabase.rpc('execute_sql', {'query': query}).execute()

@router.get('/agregadas')
async def get_consolidated(municipio: str, producto: str):
    query = f"SELECT producto, SUM(volumen_kg) as total, COUNT(id) as num_prod FROM cosechas WHERE municipio = '{municipio}' AND producto = '{producto}' AND estado = 'DISPONIBLE' GROUP BY producto"
    return supabase.rpc('execute_sql', {'query': query}).execute()
