import os, requests
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SODA_URL = os.getenv('SODA_API_URL', 'https://www.datos.gov.co/resource/agro_farmers.json')
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_ROLE_KEY'))

def sync_farmers():
    response = requests.get(SODA_URL)
    data = response.json()
    for row in data:
        cleaned = {
            'external_id': str(row.get('id') or row.get('id_farmer')),
            'name': str(row.get('nombre') or row.get('nombre_agricultor', 'Desconocido')).strip(),
            'municipio': row.get('municipio', 'N/A'),
            'departamento': row.get('departamento', 'N/A'),
            'product': row.get('producto', 'General'),
            'phone': str(row.get('telefono', 'Sin contacto')).strip(),
            'ubicacion': f'POINT({row.get("long")}, {row.get("lat")})',
            'origen_//registro': 'DATOS_GOV'
        }
        supabase.table('productores').upsert(cleaned, on_conflict='telefono').execute()

if __name__ == "__main__":
    sync_farmers()
