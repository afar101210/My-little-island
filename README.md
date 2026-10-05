# My Little Island

Juego para niñas y niños de 8 a 12 años sobre **por qué estudiar ingeniería**.

1. Saca una carta de **problema** (puente caído, río sucio, casas sin luz…).
2. Saca una carta de **presupuesto** (monedas).
3. Construye la solución con bloques; cada tipo de bloque cuesta distinto.
4. Antes de ganar hay que pasar **la prueba**: gravedad, peso del camión sobre las vigas y viento sobre torres delgadas. Lo mal construido se cae. Piezas limitadas en la bodega y 5 minutos.

Tiene dos modos: **en la pantalla** (isla de 8×8 con bloques) y **con Legos de verdad** (la app saca las cartas, cuenta 5 minutos y suma el precio de las piezas).

## Archivos

- `app.html`: el juego (HTML, CSS y JS en un solo archivo).
- `index.html`: versión instalable; se genera con `./build.sh` después de editar `app.html`.
- `manifest.webmanifest`, `icon.svg`: para "Añadir a pantalla de inicio".

Para tenerlo como app en el teléfono, publica la carpeta (por ejemplo con GitHub Pages), abre el enlace y usa *Añadir a la pantalla principal*.
