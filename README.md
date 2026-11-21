# AndyTV Plus 🚀

Reproductor multimedia open-source de televisión y listas propias (BYOL) para **Android TV** y **Web (PWA)** con soporte para control remoto y pantallas táctiles.

## 📺 Características

- **Soporte Dual:**
  - **App Android TV Nativa:** Reproducción acelerada por hardware con **ExoPlayer / Media3** y soporte para control remoto D-Pad / CH+ / CH-.
  - **Versión Web (PWA):** Despliegue estático instalable en móviles, tablets y PC con `hls.js`.
- **Modelo BYOL (Bring Your Own List):** El usuario puede vincular sus propias listas JSON externas (por ejemplo mediante un GitHub Secret Gist privado) desde la interfaz.
- **Auto-Fallback:** Cambio automático de señal ante caídas y selector manual desde el reproductor.

## 📁 Estructura del Proyecto

- `index.html`: Aplicación web PWA SPA.
- `canales_extra.template.json`: Plantilla de ejemplo (con URLs ficticias) para documentar el esquema JSON BYOL.
- `app/`: Código fuente de la aplicación Android TV (`com.mitele.tv.plus`).
- `tests/`: Suite de pruebas unitarias (`node --test`).

## 🛠️ Pruebas Locales

```bash
node --test tests/plus-architecture.test.js tests/source-health.test.js
```

## ⚖️ Aviso Legal / Disclaimer

- **AndyTV Plus** es un reproductor multimedia independiente de código abierto. **No aloja, retransmite, almacena ni provee contenido audiovisual de terceros.**
- La aplicación no incluye señales pagas ni enlaces no oficiales en su código fuente. Cualquier lista externa vinculada por el usuario mediante la función *Fuentes Extra* (BYOL) es responsabilidad exclusiva de quien la configura.
- Todas las marcas, nombres comerciales y logotipos mencionados pertenecen a sus respectivos propietarios.
- Si sos titular de derechos y deseás solicitar la remoción de alguna referencia en el catálogo base, abrí un *Issue* en este repositorio para su baja inmediata.

## 📄 Licencias

- Código del proyecto: **MIT License**.
- `hls.min.js`: **Apache License 2.0** (video-dev/hls.js).
