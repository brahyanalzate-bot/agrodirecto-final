# Lvl 3: Componentes - Organización del Código

## 🧩 Explicación para Principiantes
Dentro de la app, el código no está tirado en cualquier lugar. Usamos algo llamado **Screaming Architecture**. Esto significa que si miras las carpetas del proyecto, el nombre de la carpeta te "grita" qué hace el negocio, no qué tecnología usa.

## 📂 Estructura de Componentes
- **`/features/productor`**: Todo lo relacionado con el campesino (Registro de cosecha, inventario).
- **`/features/comprador`**: Todo lo relacionado con la compra (Buscador, detalle de producto, mis pedidos).
- **`/features/logistica`**: Gestión de rutas y estados de entrega.
- **`/services`**: La lógica pesada. Aquí están `orderService` (pedidos) y `authService` (seguridad).
- **`/components/ui`**: Los ladrillos básicos (botones, inputs) que siguen la **Ley del Front** (Design System Agro).

## 📐 Estándares de Calidad
- **TDD:** Cada componente tiene un test. Si el test no pasa, el componente no entra en la app.
- **Accesibilidad:** Targets táctiles de 48px para uso en campo.
