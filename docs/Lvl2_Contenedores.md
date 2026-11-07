# Lvl 2: Contenedores - Arquitectura Técnica

## 📦 Explicación para Principiantes
Si la app fuera una ciudad, los "contenedores" serían los edificios. No todo sucede en un solo lugar. Tenemos un edificio para la interfaz (lo que el usuario toca), un edificio para la base de datos (donde se guarda la información) y un sistema de tuberías que conecta todo.

## 🏗️ Mapa de Contenedores
1. **Frontend (App Móvil):** Construido con **Expo y React Native**. Es el "rostro" del sistema. Corre en el teléfono del usuario.
2. **Backend (Servicios):** Capa de lógica implementada en **FastAPI (Python)** y **Supabase Edge Functions**. Se encarga de las reglas de negocio (ej: calcular el total de un pedido).
3. **Base de Datos (Almacén):** **PostgreSQL con PostGIS**. Aquí guardamos la ubicación geográfica de los cultivos y el historial de transacciones.
4. **Sincronizador (ETL):** Un script de **Python** que viaja a los servidores del gobierno (`datos.gov.co`) y trae datos de agricultores para alimentar el sistema.

## 🔄 Flujo de Datos Global
`SODA API` $\rightarrow$ `Python Script` $\rightarrow$ `Supabase DB` $\rightarrow$ `Mobile App` $\rightarrow$ `Usuario Final`
