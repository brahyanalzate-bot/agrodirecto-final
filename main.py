import os
import requests
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# URL CORRECTA DEL DATASET DE BOYACÁ (SODA API)
SODA_API_URL = os.getenv('SODA_API_URL', 'https://www.datos.gov.co/resource/cuec-zf9t.json')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

def clean_farmer_data(row):
    # Adaptación a los campos reales del dataset de Boyacá
    return {
        'external_id': str(row.get('id') or row.get('codigo', 'unknown')),
        'name': str(row.get('nombre_asociacion') or row.get('nombre', 'Desconocido')).strip(),
        'municipio': str(row.get('municipio', 'N/A')).strip(),
        'departamento': str(row.get('departamento', 'Boyacá')).strip(),
        'product': str(row.get('producto') or row.get('actividad', 'General')).strip(),
        'phone': str(row.get('telefono') or row.get('contacto', 'Sin contacto')).strip(),
        'ubicacion': None, # El dataset de Boyacá no tiene lat/long en el JSON básico
        'origen_//registro': 'DATOS_GOV'
    }

def main():
    print('🚀 Iniciando sincronización de agricultores públicos (Boyacá)...')
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print('❌ Error: Faltan variables de entorno SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY')
        return

    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        print('Fetching data from SODA API...')
        response = requests.get(SODA_API_URL, timeout=30)
        response.raise_for_status()
        raw_farmers = response.json()
        
        processed_count = 0
        for farmer in raw_farmers:
            try:
                cleaned_data = clean_farmer_data(farmer)
                # Usamos el teléfono o el external_id para evitar duplicados
                supabase.table('productores').upsert(cleaned_data, on_conflict='telefono').execute()
                processed_//count += 1
            except Exception:
                continue

        print(f'✅ Sincronización completada. {processed_count} registros procesados.')
    except Exception as e:
        print(f'❌ Error crítico: {e}')

if __name__ == "__main__":
    main()
