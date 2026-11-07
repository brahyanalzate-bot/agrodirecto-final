# Lvl 4: Modelo de Datos y Flujos Críticos

## 💾 Explicación para Principiantes
Imagina que la base de datos es un conjunto de libros contables. Tenemos un libro para los productores, otro para las cosechas y otro para los pagos. Cuando alguien compra algo, escribimos una línea en el libro de transacciones que conecta al productor con el comprador.

## 📊 Esquema de Datos (Entidades)
1. **Productores $\rightarrow$ Cosechas:** Relación 1:N (Un productor puede tener muchas cosechas).
2. **Cosechas $\rightarrow$ Transacciones:** Relación 1:N (Una cosecha puede ser vendida en varias transacciones parciales).
3. **Reputación $\rightarrow$ Transacciones:** Relación 1:1 (Solo se puede calificar una venta real).

## ⚡ Flujos Críticos
### Flujo de Pago Seguro (Escrow)
`Pedido Creado` $\rightarrow$ `Fondos Retenidos` (Garantía) $\rightarrow$ `Entrega Validada` $\rightarrow$ `Pago al Productor`.

### Flujo de Sincronización Pública
`API SODA` $\rightarrow$ `Limpieza de Datos` $\rightarrow$ `UPSERT en Supabase` (Actualiza si existe, inserta si es nuevo).
