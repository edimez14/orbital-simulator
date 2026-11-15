# código nuevo edizon
# Despliegue gratuito del simulador orbital

La aplicación ya está preparada para publicarse. No necesita base de datos,
secretos ni archivos externos: solo el puerto que entregue la plataforma.

## Opción recomendada: Render (gratis)

Render lee el archivo `render.yaml` que está en la raíz y configura todo solo.

1. Sube el proyecto a GitHub (ya está en `edimez14/orbital-simulator`).
2. Entra a `https://render.com` y crea una cuenta con GitHub.
3. En el panel: **New +** → **Blueprint**.
4. Elige el repositorio `orbital-simulator` y pulsa **Apply**.
5. Render instala `requirements-deploy.txt`, arranca con Gunicorn y comprueba
   `/health`.
6. Cuando termine, abre la dirección que aparece, con esta forma:

   ```
   https://orbital-simulator.onrender.com
   ```

Cada `git push` a `main` vuelve a desplegar automáticamente.

**Límites del plan gratuito de Render:** el servicio se duerme tras 15 minutos
sin visitas y tarda alrededor de 50 segundos en despertar; memoria de 512 MB; un
solo proceso. Para una demostración y un proyecto académico es suficiente.

## Alternativa: Hugging Face Spaces (gratis, con Docker)

1. Entra a `https://huggingface.co` → **New Space**.
2. Nombre: `orbital-simulator`. SDK: **Docker**. Visibilidad: pública. Hardware:
   CPU básica (gratis).
3. Copia el contenido del repositorio al Space (puedes clonar el Space y copiar
   los archivos, o subirlos desde la web).
4. Reemplaza el `README.md` del Space por
   `deploy/huggingface_README.md`. Ese archivo ya trae la configuración
   `sdk: docker` y `app_port: 7860`.
5. El Space construye el `Dockerfile` y publica en una dirección como:

   ```
   https://TU-USUARIO-orbital-simulator.hf.space
   ```

**Límites:** CPU básica gratuita, 16 GB de memoria y pausa tras 48 horas sin
uso. El puerto 7860 ya está configurado en la imagen.

## Alternativa: Docker en cualquier plataforma

El `Dockerfile` sirve para Koyeb, Fly.io, Google Cloud Run o cualquier servidor
con Docker. La aplicación escucha en `$PORT` o, si no existe, en 7860.

```bash
docker build -t orbital-simulator .
docker run --rm -p 7860:7860 orbital-simulator
```

Abre `http://127.0.0.1:7860`.

En esas plataformas solo hay que definir `PORT` si lo piden; no hace falta nada
más.

## Comprobación antes de publicar

```bash
# 1. Pruebas
.venv/bin/python -m pytest -q          # deben pasar 114

# 2. Imagen y arranque
docker build -t orbital-simulator .
docker run --rm -p 7860:7860 orbital-simulator

# 3. Salud y página
curl http://127.0.0.1:7860/health       # {"status":"ok"}
```

## Qué usa la aplicación en ejecución

| Recurso | Necesidad |
|---|---|
| Variables de entorno | `PORT` (lo entrega la plataforma). Sin secretos |
| Disco | Solo lectura: `data/presets.json` y `assets/` |
| Base de datos | Ninguna. Cada navegador guarda su simulación |
| Memoria | Menos de 512 MB en una corrida normal |
| Tiempo por corrida | Unos 4 s para 30 días con dt = 60 s |
| Timeout del servidor | 120 s (holgado) |

## Limitaciones que debes conocer

- En Render gratis el servicio duerme: la primera visita puede tardar ~50 s.
- Hay un solo worker. Si dos personas simulan a la vez, las corridas se turnan;
  no se pierde ningún dato, solo esperan.
- Los resultados no se guardan en el servidor. Al cerrar o recargar la página,
  se pierde la corrida; los presets y el código sí quedan.
- El empaquetado de escritorio (tarea A38) es otra cosa y sigue en pausa.
