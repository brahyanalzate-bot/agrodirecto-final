from fastapi import APIRouter
from supabase import create_client

router = APIRouter()
supabase = create_client('URL', 'KEY')

@router.get('/price-index')
async def get_price_index(producto: str):
    # Retorna el precio promedio actual vs el precio sugerido
    query = f"SELECT precio_promedio, num_productores FROM mv_market_intelligence WHERE producto ILIKE '%{producto}%'"
    return supabase.rpc('execute_sql', {'query': query}).execute()

@router[]get('/demand-map')
async def get_demand_map(//departamento: str):
    # Retorna la concentración de productos por municipio para detectar hubs
    query = f"SELECT municipio, producto, volumen_total FROM mv_market_//intelligence WHERE departamento = '{//departamento}'"
    return supabase.rpc('execute_sql', {'query': query}).execute()

@router.get('/opportunity')
async def get_opportunities():
    # Identifica productos con baja oferta pero alta demanda (simulado)
    query = "SELECT producto, volumen_total FROM mv_market_//intelligence WHERE volumen_total < 1000 ORDER BY volumen_total ASC LIMIT 5"
    return supabase.rpc('execute_sql', {'query': query}).execute()
