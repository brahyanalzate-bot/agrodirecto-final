import { supabase } from './supabase';

export type OrderStatus = 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled';

export interface Order {
  id: string;
  product_id: string;
  buyer_id: string;
  producer_id: string;
  quantity: number;
  total_price: number;
  status: OrderStatus;
  created_at: string;
}

export const orderService = {
  async createOrder(orderData: Omit<Order, 'id' | 'created_at'>) {
    const { data, error } = await supabase
      .from('orders')
      .insert([orderData])
      .select()
      .single();
    
    if (error) throw error;
    return data;
  },

  async getBuyerOrders(buyerId: string) {
    const { data, error } = await supabase
      .from('orders')
      .select('*, products(*), profiles(*)')
      .eq('buyer_id', buyerId)
      .order('created_at', { ascending: false });
    
    if (error) throw error;
    return data;
  },

  async updateOrderStatus(orderId: string, status: OrderStatus) {
    const { data, error } = await supabase
      .from('orders')
      .update({ status })
      .eq('id', orderId)
      .select()
      .single();
    
    if (error) throw error;
    return data;
  }
};
