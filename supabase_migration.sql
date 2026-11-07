-- 1. Tablas de Perfiles (Extensión de auth.users)
CREATE TABLE IF NOT EXISTS profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  full_name TEXT,
  role TEXT CHECK (role IN ('PROD', 'COMP', 'LOG')),
  phone TEXT,
  location TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 2. Tabla de Productos
CREATE TABLE IF NOT EXISTS products (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  producer_id UUID REFERENCES profiles(id) NOT NULL,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  quantity DECIMAL NOT NULL,
  price DECIMAL NOT NULL,
  harvest_date DATE NOT NULL,
  description TEXT,
  image_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 3. Tabla de Pedidos (Orders)
CREATE TABLE IF NOT EXISTS orders (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  product_id UUID REFERENCES products(id) NOT NULL,
  buyer_id UUID REFERENCES profiles(id) NOT NULL,
  producer_id UUID REFERENCES profiles(id) NOT NULL,
  quantity DECIMAL NOT NULL,
  total_price DECIMAL NOT NULL,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 4. Habilitar RLS (Seguridad de Nivel de Fila)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- 5. Políticas de Seguridad (RLS)
-- Profiles: Cualquiera puede ver perfiles, solo el dueño puede editar
CREATE POLICY "Public profiles are viewable by everyone" ON profiles FOR SELECT USING (true);
CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);

-- Products: Cualquiera puede ver productos, solo el productor puede editar/borrar
CREATE POLICY "Products are viewable by everyone" ON products FOR SELECT USING (true);
CREATE POLICY "Producers can insert their own products" ON products FOR INSERT WITH CHECK (auth.uid() = producer_id);
CREATE POLICY "Producers can update own products" ON products FOR UPDATE USING (auth.uid() = producer_id);
CREATE POLICY "Producers can delete own products" ON products FOR DELETE USING (auth.uid() = producer_id);

-- Orders: Comprador y Productor ven el pedido, cualquiera autenticado puede crear
CREATE POLICY "Users can view their own orders" ON orders FOR SELECT USING (auth.uid() = buyer_id OR auth.uid() = producer_id);
CREATE POLICY "Authenticated users can create orders" ON orders FOR INSERT WITH CHECK (auth.role() = 'authenticated');
