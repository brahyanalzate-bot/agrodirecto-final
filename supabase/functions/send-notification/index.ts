import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"

const SUPABASE_URL = Deno.env.get('SUPABASE_URL') || '';
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') || '';
const EXPO_ACCESS_TOKEN = Deno.env.get('EXPO_ACCESS_TOKEN') || '';

serve(async (req) => {
  try {
    const { record } = await req.json();
    
    // 1. Obtener el token del destinatario (está en la tabla profiles)
    // Determinamos quién recibe la notificación según la acción
    const recipientId = record.producer_id || record.buyer_id;
    
    const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);
    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .select('push_token, full_name')
      .eq('id', recipientId)
      .single();

    if (profileError || !profile?.push_token) {
      return new Response(JSON.stringify({ message: 'No push token found' }), { status: 200 });
    }

    // 2. Definir el mensaje según el estado del pedido
    let title = 'Actualización de Pedido 🌾';
    let body = 'Hay una actualización en tu transacción de Agrodirecto.';

    if (record.estado_pago === 'FONDOS_RETENIDOS') {
      body = `¡Hola ${profile.full_name}! Los fondos de tu cosecha han sido retenidos. Puedes proceder con la entrega.`;
    } else if (record.estado_pago === 'PAGADO_AL_PRODUCTOR') {
      body = `¡Pago recibido! Los fondos ya están en tu cuenta. Gracias por tu trabajo.`;
    } else if (record.estado_pago === '//PENDIENTE_ESCROW') {
      body = `Tienes un nuevo pedido reservado. El comprador ha iniciado el proceso de pago.`;
    }

    // 3. Enviar la notificación vía Expo Push API
    const response = await fetch('https://exp.exponent.dev/push/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${EXPO_ACCESS_TOKEN}`,
      },
      body: JSON.stringify({
        to: profile.push_token,
        title: title,
        body: body,
        data: { orderId: record.id },
      }),
    });

    return new Response(JSON.stringify({ sent: true }), { status: 200 });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
})
