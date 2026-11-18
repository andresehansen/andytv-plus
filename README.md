# AndyTV Plus 🚀

Plataforma dual de televisión en vivo y deportes para **Android TV** y **Web (PWA)** con soporte para control remoto y pantallas táctiles.

## 📺 Características

- **Soporte Dual:**
  - **App Android TV Nativa:** Extracción transparente de flujos `.m3u8` protegidos por token mediante `DynamicStreamResolver` y reproducción acelerada por hardware con **ExoPlayer / Media3**.
  - **Versión Web (PWA):** Despliegue estático en GitHub Pages con soporte PWA (instalable en móviles, tablets y PC) y reproductores limpios a pantalla completa con audio habilitado.
- **Modelo BYOL (Bring Your Own List):** Vinculación segura de señales deportivas y canales adicionales mediante GitHub Secret Gist privado (código corto o URL).
- **Lista Blanca Dinámica IPTV-Org:** Fusión inteligente de señales de aire y noticias de Argentina (`https://iptv-org.github.io/iptv/countries/ar.m3u`) como respaldos automáticos sin duplicar canales.
- **Auto-Fallback Inteligente:** Tolerancia a caídas con cambio automático de fuente secundaria y selector manual de señal en pantalla.

## 📁 Estructura del Proyecto

- `index.html`: Aplicación web PWA SPA (raíz para GitHub Pages).
- `canales_extra.template.json`: Plantilla de canales deportivos y respaldos para subir a tu GitHub Secret Gist.
- `app/`: Código fuente de la aplicación Android TV (`com.mitele.tv.plus`).
- `tests/`: Suite de pruebas unitarias (`node --test`).

## 🛠️ Pruebas Locales

```bash
node --test tests/plus-architecture.test.js tests/source-health.test.js
```
