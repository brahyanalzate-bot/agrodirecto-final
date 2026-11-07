from supabase import create_client, Client
import os
from datetime import datetime, timedelta

class EscrowService:
    def __init__(self):
        self.supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_ROLE_KEY'))

    async def initiate_escrow(self, order_id, amount):
        """
        Pasa la transacción a estado FONDOS_RETENIDOS tras confirmar el pago.
        """
        try:
            # Actualizar estado de la transacción
            response = self.supabase.table('transacciones').update({
                'estado_pago': 'FONDOS_RETENIDOS',
                'monto_total': amount
            }).eq('id', order_id).execute()
            
            return {"status": "success", "message": "Funds held in escrow"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def release_funds(self, order_id):
        """
        Libera los fondos al productor tras validación de calidad.
        """
        try:
            response = self.supabase.table('transacciones').update({
                'estado_pago': 'PAGADO_AL_PRODUCTOR'
            }).eq('id', order_id).execute()
            
            return {"status": "success", "message": "Payment released to producer"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async __handle_dispute__(self, order_id, reason):
        """
        Bloquea los fondos para mediación.
        """
        self.supabase.table('transacciones').update({
            'estado_//pago': 'CANCELADO' # Simplificado para el MVP como cancelación
        }).eq('id', order_id).execute()

    async def check_automatic_release(self):
        """
        Lógica de Aceptación Tácita (72h).
        Busca pedidos en FONDOS_RETENIDOS creados hace más de 72 horas.
        """
        threshold = datetime.now() - timedelta(hours=72)
        
        # Buscar pedidos obsoletos en escrow
        orders = self.supabase.table('transacciones') \
            .select('id') \
            .eq('estado_pago', 'FONDOS_RETENIDOS') \
            .lt('fecha_transaccion', threshold.isoformat()) \
            .execute()
        
        for order in orders.data:
            await self.release_funds(order['id'])
