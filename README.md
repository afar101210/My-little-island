# My Little Island

Juego para niñas y niños de 8 a 12 años sobre **por qué estudiar ingeniería**.

1. Saca una carta de **problema** (puente caído, río contaminado, casas sin luz, inundación, hospital sin señal, peces sin medir).
2. Saca una carta de **condición** (viento fuerte, lluvia, camión pesado, terreno blando, poco tiempo).
3. Construye en una isla vista de lado (mar, playa, río y colina) con gravedad, cimientos, pilares, vigas, cables y energía solar, usando solo las piezas de la bodega.
4. **Prueba** la obra: peso, viento, agua y una persona que camina por lo construido. Si algo falla, mejora y prueba otra vez.

También tiene un modo **con Legos de verdad**: la app saca las cartas, dice qué construir y cómo probarlo, y lleva el tiempo.

## Instalar en el teléfono desde GitHub

1. En GitHub: **Settings → Pages → Build and deployment**, elige *Deploy from a branch*, la rama `claude/my-little-island-lego-game-tyh104` y la carpeta `/ (root)`. Guarda.
2. Abre en el teléfono `https://afar101210.github.io/My-little-island/`.
3. Android (Chrome): menú ⋮ → **Instalar app**. iPhone (Safari): Compartir → **Añadir a pantalla de inicio**.

Queda como app con su ícono y funciona sin internet después de abrirla una vez.

## Archivos

- `app.html`: el juego (HTML, CSS y JS en un solo archivo).
- `index.html`: versión instalable; se genera con `./build.sh` después de editar `app.html`.
- `manifest.webmanifest`, `sw.js`, `icon*.png`, `icon.svg`: lo necesario para instalarla como app.
