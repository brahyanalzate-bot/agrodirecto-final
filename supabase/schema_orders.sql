-- Esquema de la tabla de Pedidos para Agrodirecto
CREATE TABLE orders (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  product_id UUID REFERENCES products(id) NOT NULL,
  buyer_id UUID REFERENCES auth.users(id) NOT NULL,
  producer_id UUID REFERENCES auth.users(id) NOT NULL,
  quantity DECIMAL NOT NULL,
  total_price DECIMAL NOT NULL,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Habilitar RLS (Row Level Security)
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Política: Los compradores pueden ver sus propios pedidos
CREATE POLICY 'Buyers can view own orders' ON orders 
  FOR SELECT USING (auth.uid() = buyer_id);

-- Política: Los productores pueden ver los pedidos de sus productos
CREATE POLICY 'Producers can view their product orders' ON orders 
  FOR SELECT USING (auth.uid() = producer_id);

-- Política: Insertar pedidos (cualquier usuario autenticado)
CREATE POLICY 'Authenticated users can create orders' ON orders 
  FOR INSERT WITH CHECK (auth.role() = 'authenticated');
