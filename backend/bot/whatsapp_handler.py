from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class WhatsAppMsg(BaseModel):
    From: str
    Body: str

@app.post('/whatsapp/webhook')
async def handle_whatsapp(msg: WhatsAppMsg):
    text = msg.Body.lower()
    if '1' in text or 'registrar' in text:
        return {'reply': 'Ingrese: Producto, Variedad, Kilos, Calidad (1-3), Ciudad'}
    if '2' in text or 'actualizar' in text:
        return {'reply': 'Seleccione el lote a actualizar...'}
    if '3' in text or 'ventas' in text:
        return {'reply': 'Sus ventas totales son: $X.XXX'}
    return {'reply': 'Bienvenido a Agrodirecto. Use: 1. Registrar, 2. Actualizar, 3. Ventas'}
