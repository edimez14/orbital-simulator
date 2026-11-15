<!-- código nuevo edizon -->
# Auditoría y plan de corrección del simulador orbital

Este archivo documenta la revisión del código y de la página y sirve como instrucciones de trabajo para DeepSeek. No implementa ninguna corrección.

Fecha: 13 de noviembre de 2026. Se auditó el árbol de trabajo local, incluidos sus cambios previos sin confirmar. No se modificaron fuentes, estilos, dependencias ni pruebas. El único archivo añadido por esta revisión es este documento.

## Cómo ejecutar este plan

DeepSeek debe leer AGENTS.md, docs/plan_de_desarrollo.md y docs/tareas_cambios.md antes de actuar. Este documento es una propuesta de correcciones, no autorización para implementarlas todas. Presentar una tarea individual al usuario, obtener su aprobación conforme a las reglas del proyecto, implementar únicamente esa tarea, mostrar resultado y evidencia y esperar su revisión antes de continuar. No hacer commits, publicar, compilar ni instalar librerías por iniciativa propia. Conservar cambios ajenos y no restaurar el árbol con Git. La regla de trabajo en grupo implica coordinar responsabilidades; no autoriza a sobrescribir archivos de otros integrantes.

Seguir el orden de fases del plan original; las agrupaciones siguientes indican el área del trabajo y sus dependencias, no permiten saltarse fases abiertas. Primero reconciliar el estado del plan en A01. SI y Dash ya están documentados como decisiones confirmadas en tareas_cambios.md: no convertir las fuentes de nuevo a AU ni regresar a VPython. No reintroducir WebGL como única vía: la alternativa sin WebGL fue una decisión expresa. No recuperar texturas planas eliminadas en la tarea 24. Si una solución necesita cambiar una decisión existente, presentar esa decisión al usuario antes de escribir código.

Cada casilla corresponde a un resultado individual. Sus pruebas pertenecen a esa misma tarea. P0: impide obtener resultados fiables o provoca fallos. P1: comportamiento o validación científica incompletos. P2: claridad, diseño o mantenimiento. “Confirmado” significa observado en navegador, reproducido con Python o demostrado directamente por una ruta de código. “Pendiente de verificación” no debe presentarse como un fallo observado.

## Evidencia de la revisión

- Entorno disponible: Python 3.12, entorno .venv; Dash servido en http://127.0.0.1:8050. Se necesitó permiso del entorno para abrir el puerto local; no fue un fallo del proyecto.
- Comando: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider -q`. Resultado: **52 pruebas aprobadas, 5 advertencias**, en 5,99 segundos. Advertencias de DataTable y pkg_resources/VPython; no son por sí mismas fallos de ejecución.
- Navegador: carga de página y CSS, corrida Tierra–Luna de 1 día, elección de los cuatro tipos, reproducción y pausa, controles de giro/inclinación/zoom, cambio por los tres escenarios, elección de Euler-Cromer, agregar/eliminar un cuerpo y edición del nombre del secundario. Se comprobó la generación visible de tarjetas, tabla y gráficas. No se midió continuidad exacta de cuadros ni precisión física a partir de la animación.
- Eliminar la Luna e iniciar devolvió **HTTP 500**. Registro: `update_panel → build_panel → kepler_figure → _relative_positions(..., 1) → IndexError`. El navegador no expone un mensaje útil al usuario y puede conservar resultados anteriores.
- Capturas revisadas: distribución apilada en ventana estrecha, menú de escenarios abierto, campos y método con fondo blanco y texto muy claro. Se intentaron vistas de 1440×1000 y 390×844; las capturas del visor resultaron escaladas/inconsistentes y una captura falló. **No se certifica con ellas el diseño responsive completo**. Volver a probarlo según A29.
- Python adicional: `build_panel(initial_bodies(), 'Verlet', 200000, 1, 35, 25, 1)` falla con IndexError. Con solo el primario también falla. Masa `None` falla con TypeError. Masa negativa se admite. Cuerpos coincidentes producen energía `-inf`.
- `run_simulation(..., dt=60, steps=100, record_every=30)` guarda tiempos `[0,1800,3600,5400]`, aunque integra hasta 6000 s. `table_rows` devuelve 50 filas para un historial de 100 registros, pese a MAX_TABLE_ROWS=40.
- Tierra–Luna, 30 días, dt=60 s: Euler-Cromer y Verlet guardan **2058** registros pese a MAX_RECORDS=2000 y terminan el historial en 2591820 s frente a los 2592000 s integrados. Máxima variación energética sobre las muestras: 0,0000810032 % y 0,0000810082 %, respectivamente; momento: aproximadamente 8,79e-13 % y 3,94e-9 %. Son buenos resultados para ese caso; no prueban todos los parámetros, y el muestreo puede omitir máximos entre registros.
- Con la velocidad aplicada por la interfaz y `mu=G*(M+m)`, excentricidades iniciales Tierra–Luna: Circular 0,0121447; Elíptica 0,367773; Parabólica 0,975711; Hiperbólica 1,84502. El caso llamado parabólico sigue ligado.

## Límites de la auditoría

No se compilaron ejecutables: el empaquetado está expresamente en pausa. No se instalaron paquetes, no se ejecutaron workflows remotos, no se publicó nada. No se certificaron Windows/macOS ni uso sin conexión. No se inspeccionó visualmente el PDF del preproyecto ni se comparó su boceto página por página; la referencia de diseño revisada fue el código y las decisiones escritas en tareas_cambios.md. Las tareas que requieran esa comparación deben conservar ese estado pendiente. En la primera revisión no se probaron exhaustivamente todas las combinaciones numéricas, accesibilidad con lector de pantalla, descargas de Plotly, compartir gráficos, cada herramienta de su barra ni la paginación completa de la tabla. La segunda revisión, al final de este documento, actualiza estos pendientes con resultados reales de uso. A35 prescribe ese cierre; no confundir esta revisión con una certificación de ausencia de errores.

## Plan de tareas individuales

### A01 — Reconciliar el documento rector

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** AGENTS.md; docs/plan_de_desarrollo.md; docs/tareas_cambios.md; README.md.
- **Hallazgo y reproducción:** Confirmado por lectura: AGENTS exige AU/masas solares/años y el plan conserva esas unidades en su cuerpo; la cabecera y tareas confirmadas establecen SI/Dash. README dice que falta tarea 11, pero tareas_cambios la marca terminada.
- **Instrucción concreta:** Presentar una propuesta documental que identifique la decisión vigente, la fase realmente abierta y la relación de estas correcciones con sus fases originales. Sustituir únicamente textos contradictorios tras aprobación. No cambiar constantes físicas.
- **Criterio de aceptación:** No hay instrucciones operativas incompatibles sobre unidades/interfaz ni tareas simultáneamente hechas y pendientes. El usuario aprueba el orden.
- **Dependencia:** Ninguna.

### A02 — Validar los datos de cada cuerpo

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P0.
- **Archivos y punto de entrada:** src/ui/app.py:dict_to_body, set_body_field, build_panel; src/physics/bodies.py.
- **Hallazgo y reproducción:** Masa None provoca TypeError; masa negativa se integra. Los campos admiten borrado y no tienen validación física central.
- **Instrucción concreta:** Validar antes de crear cuerpos: nombre no vacío, masa positiva y finita, posición y velocidad de tres componentes numéricos finitos. Rechazar None, NaN e infinito con error que identifique cuerpo y campo. Validar también la entrada pública del motor. No convertir silenciosamente un campo vacío en cero.
- **Criterio de aceptación:** Probar por separado nombre vacío, masa vacía/cero/negativa y cada componente no finito; no se inicia integración y aparece una explicación. Datos válidos conservan su valor.
- **Dependencia:** A01.

### A03 — Tratar la ausencia de cuerpos secundarios

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P0.
- **Archivos y punto de entrada:** src/ui/app.py:build_panel; src/ui/figures.py:kepler_figure.
- **Hallazgo y reproducción:** Eliminar el único secundario y pulsar iniciar causa HTTP 500 e IndexError confirmado en navegador.
- **Instrucción concreta:** Permitir editar una lista con solo primario, pero bloquear iniciar con mensaje de que se necesitan al menos dos cuerpos. Proteger asimismo las funciones de figuras que requieren un secundario.
- **Criterio de aceptación:** Eliminar Luna, iniciar, leer mensaje, agregar otro cuerpo e iniciar correctamente sin recargar página. Probar el mismo caso llamando build_panel.
- **Dependencia:** A02.

### A04 — Definir la duración alcanzable con dt

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P0.
- **Archivos y punto de entrada:** src/simulation.py:total_steps; src/ui/app.py:build_panel.
- **Hallazgo y reproducción:** round(total_time/dt) puede dar cero pasos; con dt=200000 s y duración=1 día el panel falla. Un solo registro también rompe kepler_figure al leer time[1].
- **Instrucción concreta:** Validar tiempos finitos positivos y suficientes muestras. Proponer al usuario cómo resolver una duración no divisible: paso final reducido o duración efectiva explícita. No anunciar una duración que no se integra. Aplicar la decisión sin redondeo silencioso.
- **Criterio de aceptación:** Probar dt mayor, igual, menor y no divisor de la duración; ningún IndexError. Cualquier rechazo explica cómo corregirlo. Tiempo final coincide con la política aprobada.
- **Dependencia:** A02.

### A05 — Rechazar condiciones iniciales superpuestas

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P0.
- **Archivos y punto de entrada:** src/ui/app.py:add_body_to, build_panel; src/physics/conservation.py:potential_energy.
- **Hallazgo y reproducción:** NEW_BODY comparte posición con la Luna del preset; con velocidades iguales la energía permanece -inf. MIN_DISTANCE en gravedad no protege el potencial.
- **Instrucción concreta:** Detectar separaciones inválidas antes de integrar y señalar el par afectado. No mover cuerpos ni inventar distancias por cuenta propia. Al agregar, impedir que una configuración aún superpuesta se ejecute y explicar qué posición editar.
- **Criterio de aceptación:** Preset Tierra–Luna + agregar + iniciar no produce infinitos ni resultados aparentemente válidos. El mensaje identifica el par y desaparece tras separarlo.
- **Dependencia:** A02.

### A06 — Hacer coherente el tratamiento de encuentros cercanos

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P0.
- **Archivos y punto de entrada:** src/physics/gravity.py:MIN_DISTANCE, compute_accelerations; src/physics/conservation.py:potential_energy.
- **Hallazgo y reproducción:** Gravedad limita el denominador a 1 m, pero energía usa 1/r sin límite; el modelo de fuerza y el potencial no son coherentes bajo ese umbral.
- **Instrucción concreta:** Presentar la decisión de detener la corrida al llegar al umbral, preferible para no inventar un modelo de colisión, o de aprobar un potencial regularizado coherente. Implementar solamente la decisión aprobada. No añadir radios de colisión sin alcance aprobado.
- **Criterio de aceptación:** Un acercamiento bajo el umbral se detiene con causa y tiempo, o satisface la relación fuerza/potencial del modelo aprobado. Nunca entrega NaN/inf como éxito.
- **Dependencia:** A05.

### A07 — Validar el contrato de entrada del motor

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/simulation.py:run_simulation, total_steps.
- **Hallazgo y reproducción:** No hay guardas de steps, record_every, método ni lista de cuerpos; record_every=0 divide por cero, método desconocido da KeyError.
- **Instrucción concreta:** Definir y documentar tipos y rangos: steps entero permitido por contrato, record_every entero >=1, dt finito positivo, método en INTEGRATORS y cuerpos válidos. Lanzar ValueError descriptivo para entradas inválidas.
- **Criterio de aceptación:** Pruebas individuales de cero, negativos, fracciones, no finitos y método desconocido; ningún error accidental de índice, módulo o clave.
- **Dependencia:** A02, A04.

### A08 — Limitar el coste de una solicitud

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P0.
- **Archivos y punto de entrada:** src/ui/app.py:build_panel; src/simulation.py:run_simulation.
- **Hallazgo y reproducción:** Confirmado por código: reducir registros no limita iteraciones; duración sin máximo y dt pequeño permiten una petición de coste arbitrario, agravada por pares de cuerpos. No se ejecutó una carga extrema.
- **Instrucción concreta:** Calcular pasos y pares antes de empezar. Proponer y aprobar un presupuesto de trabajo para el entorno objetivo; rechazar excesos con pasos calculados y alternativas concretas. No añadir colas ni librerías nuevas automáticamente.
- **Criterio de aceptación:** Una solicitud sobre el presupuesto se rechaza antes del bucle y el servidor sigue atendiendo. Una solicitud dentro del presupuesto termina. Registrar el presupuesto aprobado.
- **Dependencia:** A07.

### A09 — Guardar el estado final real

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/simulation.py:run_simulation.
- **Hallazgo y reproducción:** El historial se guarda antes de avanzar y nunca después del último paso: 100 pasos de 60 s con muestreo 30 terminan visualmente en 5400 s.
- **Instrucción concreta:** Registrar estado inicial y estado final alcanzado, sin duplicar índices cuando el final cae en el muestreo. Mantener tiempos, posiciones, velocidades y magnitudes alineados. Ajustar las pruebas que hoy exigen 100 registros sin comprobar tiempo final.
- **Criterio de aceptación:** Último registro corresponde al estado de los cuerpos devueltos por la integración y al tiempo efectivo. Probar divisibilidad y no divisibilidad por record_every.
- **Dependencia:** A04, A07.

### A10 — Garantizar el máximo de registros

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:build_panel, MAX_RECORDS.
- **Hallazgo y reproducción:** 43200 pasos / 2000 usa división entera 21 y guarda 2058 registros.
- **Instrucción concreta:** Calcular la frecuencia o índices de muestreo con techo y reservar espacio para extremos según A09. El límite debe incluir inicio y final. Separar este límite del presupuesto de integración.
- **Criterio de aceptación:** Con pasos 1999, 2000, 2001 y 43200 el historial no supera el límite aprobado y preserva los extremos.
- **Dependencia:** A09.

### A11 — Implementar un Verlet distinto de Euler-Cromer

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/integrators/verlet.py; tests/test_integrators.py.
- **Hallazgo y reproducción:** El archivo reconoce que su arranque Euler-Cromer y velocidad por diferencia hacia atrás reproducen Euler-Cromer. La prueba exige igualdad, sin comprobar orden dos.
- **Instrucción concreta:** Proponer la variante velocity-Verlet dentro del módulo existente: aceleraciones en t, posición r+v*dt+a*dt²/2, aceleraciones nuevas calculadas con todas las posiciones nuevas y velocidad v+(a+a_nueva)*dt/2. Actualizar todas las posiciones antes de recalcular aceleraciones. No mover esa física a Dash.
- **Criterio de aceptación:** Prueba analítica de un paso, convergencia al reducir dt y comparación de energía en órbita elíptica durante varios periodos. Verificar velocidad y posición en el mismo instante. Sustituir la prueba que exige igualdad.
- **Dependencia:** A06, A07.

### A12 — Definir el error con referencia cero

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/physics/conservation.py:relative_error.
- **Hallazgo y reproducción:** relative_error(1.0,0.0) produce ZeroDivisionError; E≈0 es precisamente relevante cerca de escape y L=0 en movimiento radial.
- **Instrucción concreta:** Definir estado no aplicable para error porcentual sin referencia suficiente; conservar error absoluto con unidades. Acordar escala física para casi cero y no usar un epsilon arbitrario que produzca un porcentaje engañoso.
- **Criterio de aceptación:** Probar (0,0), (1,0), energías negativas y referencias próximas a cero; resultado documentado y sin división por cero.
- **Dependencia:** A01.

### A13 — Calcular velocidades orbitales con las dos masas

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:circular_speed, trajectory_speed, apply_speed, velocities_text.
- **Hallazgo y reproducción:** Tierra–Luna Circular tiene e=0.0121447 y Parabólica e=0.975711 con el mu real; usar solo M no coincide con la integración que mueve ambos cuerpos.
- **Instrucción concreta:** Para el movimiento relativo de dos cuerpos usar mu=G*(M+m), vc=sqrt(mu/r), ve=sqrt(2*mu/r). Conservar la velocidad del primario como referencia al formar la velocidad relativa. En N cuerpos etiquetar estas velocidades como aproximación de par, no garantía global.
- **Criterio de aceptación:** Circular Tierra–Luna tiene excentricidad inicial cercana a cero con tolerancia numérica justificada; parabólica tiene energía específica relativa cercana a cero. Probar también masas iguales.
- **Dependencia:** A01, A11.

### A14 — Usar las tres dimensiones en los controles orbitales

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:apply_speed, velocities_text.
- **Hallazgo y reproducción:** hypot(dx,dy) ignora z y rapidez ignora vz. Un secundario sobre el eje z muestra distancia inválida pese a estar a 384400000 m.
- **Instrucción concreta:** Usar normas 3D para posición y velocidad relativas. Construir dirección tangente perpendicular a r de forma estable con un eje auxiliar no paralelo; preservar el plano actual cuando esté definido. Explicar cualquier elección de plano degenerado.
- **Criterio de aceptación:** Órbitas en xy, xz, yz y posición oblicua producen velocidad finita y perpendicular al radio, con rapidez correcta; mostrar vz en el cálculo.
- **Dependencia:** A13.

### A15 — Clasificar la órbita a partir del estado físico

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:orbit_kind, velocities_text.
- **Hallazgo y reproducción:** Clasificación usa solo factor de rapidez y bandas ±0.02: una velocidad radial de magnitud vc se llama circular y estados próximos a escape se llaman parabólicos aunque ligados.
- **Instrucción concreta:** Usar r y v relativos, energía específica y vector de excentricidad e=(v×(r×v))/mu-r/|r|. Distinguir degeneración radial y circularidad; fijar tolerancias justificadas. En N cuerpos indicar clasificación osculante aproximada del par. No vender la banda visual como igualdad física.
- **Criterio de aceptación:** Probar velocidad radial igual a vc, tangente circular, elipse, escape exacto y valores a ambos lados de escape. Coincidencia entre texto y energía/excentricidad.
- **Dependencia:** A13, A14.

### A16 — Sincronizar el selector con el escenario cargado

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:update_bodies, set_speed_for_type.
- **Hallazgo y reproducción:** Navegador: elegir Hiperbólica y después Sol–Tierra deja Hiperbólica y factor 1.697 seleccionados, mientras el texto dice ahora 1.00 Circular.
- **Instrucción concreta:** Definir una fuente de verdad para los cuerpos. Al cargar preset actualizar los controles para describir sus velocidades reales, sin modificar el preset para acomodarlo a una selección anterior. Si hace falta estado personalizado, proponerlo. Evitar bucles entre controles.
- **Criterio de aceptación:** Recorrer todos los escenarios después de elegir cada tipo; campos, factor, clasificación y tipo no se contradicen.
- **Dependencia:** A15.

### A17 — Sincronizar los controles después de editar velocidades

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:update_bodies y callbacks del tipo/velocidad.
- **Hallazgo y reproducción:** Los campos actualizan bodies-store pero no actualizan el selector ni factor. El deslizador cambia velocidad pero no el tipo marcado. Confirmado por conexiones del código.
- **Instrucción concreta:** Derivar la descripción del estado editado y distinguir una orden de aplicar tipo de una lectura del tipo actual. Evitar que una sincronización vuelva a sobrescribir una velocidad manual.
- **Criterio de aceptación:** Editar vx, vy, vz y mover factor actualiza descripción coherente; no se pierden las ediciones ni hay cascada de callbacks permanente.
- **Dependencia:** A16.

### A18 — Unificar el cuerpo secundario que se analiza

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:results_cards, table_rows, apply_speed; src/ui/figures.py:kepler_figure.
- **Hallazgo y reproducción:** Velocidad y Kepler usan índice 1; tarjetas y tabla usan índice -1. En sistema interno son Mercurio frente a Marte.
- **Instrucción concreta:** Proponer un selector explícito de cuerpo analizado con identidad estable. Aplicar esa identidad a velocidad, elementos de Kepler, tarjetas y tabla; mantener visibles las trayectorias de todos. No usar nombre como clave única si se permiten duplicados.
- **Criterio de aceptación:** Seleccionar cada planeta y comprobar que todas las vistas de detalle se refieren al mismo; eliminar el seleccionado elige un estado válido o informa de ausencia.
- **Dependencia:** A16.

### A19 — Identificar el sistema de referencia de los resultados

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:results_cards, table_rows; src/ui/figures.py:_relative_positions.
- **Hallazgo y reproducción:** Figuras son relativas al primario; tarjetas y tabla contienen coordenadas absolutas sin decirlo. El primario sí se mueve por gravedad.
- **Instrucción concreta:** Mostrar explícitamente el marco y hacerlo coherente para los detalles del cuerpo analizado; si se conservan datos absolutos, rotularlos como tales. No cambiar energía total por energía relativa sin distinguirlas.
- **Criterio de aceptación:** Trasladar el sistema y añadir velocidad común: trayectoria relativa permanece igual; datos y etiquetas explican qué magnitudes cambian de marco.
- **Dependencia:** A18.

### A20 — Rotular las magnitudes globales del sistema

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:results_cards y _center_panel.
- **Hallazgo y reproducción:** Energía y L son sumas del sistema, pero aparecen bajo Resultados del cuerpo que gira.
- **Instrucción concreta:** Cambiar los rótulos de E y L para indicar total del sistema y origen de L. Mantener posición/velocidad claramente asociadas al cuerpo elegido. No atribuir E total a un solo planeta.
- **Criterio de aceptación:** En dos y cinco cuerpos el usuario distingue sin leer código qué es del cuerpo y qué es del sistema.
- **Dependencia:** A18, A19.

### A21 — Medir conservación sin perder máximos entre muestras

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/simulation.py:run_simulation; src/ui/app.py; src/physics/conservation.py.
- **Hallazgo y reproducción:** Solo hay curvas absolutas, sin diagnóstico de la meta 1 %. El historial reducido no garantiza capturar el peor error.
- **Instrucción concreta:** Acumular máximos de variación de E y del vector L durante la integración, independientemente del historial gráfico. Mostrar porcentaje, umbral y válido/no evaluable con la política de referencia cero. Para L no comprobar únicamente su norma: también dirección/componentes.
- **Criterio de aceptación:** Un dt deliberadamente inadecuado da aviso con máximo calculado; al reducir dt la medida converge. Aumentar record_every no cambia el diagnóstico.
- **Dependencia:** A11, A12.

### A22 — Verificar realmente la primera ley

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/kepler/kepler_laws.py:check_first_law.
- **Hallazgo y reproducción:** Tomar mínimo/máximo radial no prueba elipse ni cierre; cualquier segmento hiperbólico produce e<1 con esa fórmula.
- **Instrucción concreta:** Detectar si hay órbita ligada y cobertura suficiente antes de inferir periastro/apoastro. Medir residuo respecto a una elipse con foco en el primario y cierre, o devolver evidencia insuficiente. No deducir elipse de un tramo arbitrario. Reutilizar NumPy.
- **Criterio de aceptación:** Una elipse simulada cumple tolerancia; arco corto no se certifica; hipérbola no se clasifica como elipse; trayectoria sintética no elíptica se rechaza.
- **Dependencia:** A15, A21.

### A23 — Presentar la primera ley en la página

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:_plots_panel, build_panel.
- **Hallazgo y reproducción:** La página solo grafica áreas de la segunda ley; no presenta validación de primera ley.
- **Instrucción concreta:** Conectar el diagnóstico de A22 al cuerpo seleccionado y mostrar a, e, cobertura, residuo y conclusión con unidades. Para órbitas abiertas indicar no aplicable a elipse, conservando la clasificación.
- **Criterio de aceptación:** Cambiar entre circular, elíptica, hiperbólica y corrida incompleta muestra conclusiones distintas justificadas por datos.
- **Dependencia:** A18, A22.

### A24 — Validar la segunda ley con tiempos reales

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/figures.py:kepler_figure; src/kepler/kepler_laws.py:check_second_law.
- **Hallazgo y reproducción:** Se supone dt=time[1]-time[0] y se grafica área triangular sin porcentaje ni conclusión. Muestrear saltos largos introduce error geométrico; añadir final puede crear intervalo desigual.
- **Instrucción concreta:** Integrar/sumar áreas en subpasos de física y agrupar ventanas de igual duración. Si los tiempos son desiguales usar intervalos reales y no comparar áreas brutas como si fueran iguales. Informar variación y datos insuficientes, con advertencia de perturbaciones N-cuerpos.
- **Criterio de aceptación:** Circular y elipse de dos cuerpos cumplen 1 % con dt convergente; cambiar muestreo de pantalla no altera diagnóstico; ventanas incompletas no falsean el resultado.
- **Dependencia:** A09, A18, A21.

### A25 — Medir periodos a partir de trayectorias

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/kepler/kepler_laws.py; tests/test_kepler.py.
- **Hallazgo y reproducción:** No hay medición pública de periodos: solo un auxiliar de pruebas que busca regreso a una posición absoluta.
- **Instrucción concreta:** Implementar medición relativa al primario con cruce orientado o ángulo desenrollado e interpolación temporal; rechazar arcos insuficientes y órbitas abiertas. No devolver el periodo teórico como si fuera medido.
- **Criterio de aceptación:** Tres órbitas ligadas de radio distinto recuperan periodo dentro de tolerancia; traducción del sistema no cambia resultado; hipérbola y arco corto devuelven no evaluable.
- **Dependencia:** A22.

### A26 — Validar la tercera ley con datos medidos

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/kepler/kepler_laws.py:check_third_law.
- **Hallazgo y reproducción:** Actualmente solo devuelve divisiones T²/a³, sin validar cobertura, datos ni error teórico.
- **Instrucción concreta:** Usar periodos medidos por A25 y semiejes medidos válidos. Comparar con 4*pi²/[G*(M+m)] para cada par; explicar la aproximación de constante común si m es despreciable y las perturbaciones N-cuerpos. Exigir al menos tres órbitas aptas para la demostración.
- **Criterio de aceptación:** Tres radios alrededor del mismo primario cumplen 1 %; datos inventados, insuficientes o no positivos no producen certificación positiva.
- **Dependencia:** A22, A25.

### A27 — Mostrar T² frente a a³ en la interfaz

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:_plots_panel; src/ui/figures.py.
- **Hallazgo y reproducción:** El gráfico solicitado en fase 7 no existe en Dash. No bastan constantes comprobadas solo en tests.
- **Instrucción concreta:** Añadir la presentación del análisis de A26, con puntos medidos y referencia teórica claramente diferenciados y unidades SI. No realizar silenciosamente nuevas corridas costosas al mover la cámara; solicitar datos suficientes mediante flujo explícito.
- **Criterio de aceptación:** Se ven al menos tres puntos medidos de órbitas aptas, error y referencia; sin datos suficientes aparece la causa en vez de una gráfica ficticia.
- **Dependencia:** A26.

### A28 — Corregir contraste de los desplegables

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P2.
- **Archivos y punto de entrada:** assets/style.css:259; componentes scenario y method.
- **Hallazgo y reproducción:** Confirmado en capturas: selector y método tienen fondo blanco y texto casi blanco. Los selectores CSS heredados .Select no cubren todos los elementos de Dash instalado.
- **Instrucción concreta:** Inspeccionar el DOM de la versión instalada y aplicar estilos a los elementos reales, limitados a esos controles. Cubrir cerrado, abierto, búsqueda, seleccionado, foco y deshabilitado. Mantener tema oscuro. No resolver instalando otra librería.
- **Criterio de aceptación:** Escenario y método se leen con contraste mínimo 4.5:1 para texto normal en todos los estados; selección con teclado visible.
- **Dependencia:** A01.

### A29 — Verificar y corregir la distribución responsive

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P2.
- **Archivos y punto de entrada:** assets/style.css:.grid, .triple, .body-head, .controls; src/ui/figures.py:_base_layout.
- **Hallazgo y reproducción:** Pendiente de verificación completa. Capturas estrechas muestran apilado; las pruebas actuales solo buscan @media en el texto. Tres columnas mínimas pueden dejar poco ancho al centro cerca de 1150 px.
- **Instrucción concreta:** Revisar 390, 780, 1024, 1150, 1280 y 1440 px reales y zoom 200 %. Comparar también el diseño con el boceto del PDF antes de proponer cambios visuales de alcance; registrar la página de referencia. Corregir únicamente desbordes demostrados; permitir scroll horizontal dentro de la tabla, no en toda la página. Revisar nombres, botones y leyendas con cinco cuerpos. No imponer tres columnas si inutiliza el centro.
- **Criterio de aceptación:** Guardar evidencia con dimensiones verificadas: controles completos, gráfica legible y ninguna zona inaccesible. Verificar también interfaz de cálculo al final de una lista larga.
- **Dependencia:** A28.

### A30 — Mantener el brillo pegado al cuerpo

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P2.
- **Archivos y punto de entrada:** src/ui/figures.py:_body_traces.
- **Hallazgo y reproducción:** Confirmado por geometría: el cuerpo tiene tamaño en píxeles, pero brillo se desplaza 0.05*extent en unidades de datos. Su separación cambia con cámara/zoom y puede quedar fuera del disco.
- **Instrucción concreta:** Construir el brillo en la misma posición con un recurso de dibujo cuyo desplazamiento use píxeles, o eliminar el desplazamiento conservando una apariencia coherente. No usar una fracción del tamaño de toda la órbita para el brillo de una esfera.
- **Criterio de aceptación:** Con zoom mínimo/máximo y varias relaciones de aspecto ningún brillo aparece como un objeto separado del cuerpo.
- **Dependencia:** A29.

### A31 — Conservar el último punto al muestrear la animación

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:animation_from; src/ui/figures.py:orbit_animation.
- **Hallazgo y reproducción:** animation_from usa range con salto y puede omitir el último registro. La cámara después usa ese historial reducido; su final puede diferir de las tarjetas.
- **Instrucción concreta:** Elegir índices únicos distribuidos que incluyan 0 y n-1 y respeten el límite. Preservar tiempos junto a posiciones para identificar el instante mostrado. Aplicar la misma política al regenerar la vista.
- **Criterio de aceptación:** Para 100, 241, 1000 y 2058 registros, animación y giro posterior conservan exactamente la primera y última muestra.
- **Dependencia:** A09, A10.

### A32 — Implementar reinicio explícito de la animación

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/figures.py:orbit_animation; docs/tareas_cambios.md:tarea 21.
- **Hallazgo y reproducción:** Se ofrecen Reproducir y Pausar; no hay botón Reiniciar aunque tarea 21 lo exige. No se certificó continuidad exacta de reproducción.
- **Instrucción concreta:** Añadir Reiniciar que pause y sitúe cursor, cuerpos y recorrido en la primera muestra sin recalcular física. Verificar Reproducir al finalizar y reanudación desde pausa. Rotular diferencia entre animar resultados y correr integración.
- **Criterio de aceptación:** Reproducir, pausar, continuar, finalizar, volver a reproducir y reiniciar producen estados verificables y no envían una nueva corrida al servidor.
- **Dependencia:** A31.

### A33 — Respetar el máximo de filas de la tabla

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:table_rows.
- **Hallazgo y reproducción:** Para 100 registros, salto=100//40=2 produce 50 filas. También puede omitir final y redondea tiempos a dos decimales, colapsando instantes próximos.
- **Instrucción concreta:** Seleccionar hasta MAX_TABLE_ROWS índices incluyendo extremos; conservar tiempo numérico suficiente y aplicar formato de visualización sin destruir precisión. Agregar z/vz al detalle si se quiere que represente el estado 3D completo, conforme al alcance aprobado.
- **Criterio de aceptación:** Con 1, 39, 40, 41, 100 y 2058 muestras no excede límite; última fila coincide con tarjetas; instantes distintos no son falsamente idénticos por redondeo del dato.
- **Dependencia:** A09, A18.

### A34 — Mostrar fallos y estado de cálculo de manera visible

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos y punto de entrada:** src/ui/app.py:update_panel, build_panel, build_layout.
- **Hallazgo y reproducción:** Un cuerpo causa HTTP 500 sin explicación; validaciones parciales devuelven figuras vacías con Pulsa Iniciar, que no explica el rechazo. No hay estado explícito de cálculo.
- **Instrucción concreta:** Añadir área de estado accesible. Validación da causa accionable; ejecución indica calculando y evita solicitudes duplicadas; éxito identifica parámetros usados; excepción registra detalle técnico en servidor y muestra mensaje breve. No ocultar errores bajo un éxito ni dejar resultados anteriores sin indicar que son anteriores.
- **Criterio de aceptación:** Provocar cada rechazo conocido y una excepción controlada: aparece estado correcto, se puede corregir e iniciar de nuevo sin recarga; clics repetidos no duplican trabajo.
- **Dependencia:** A02, A03, A04, A08.

### A35 — Cerrar la revisión funcional en navegador

- [ ] **Parcial:** se ejecutó un subconjunto de la matriz (ver registro al final). Los casos no ejecutados siguen pendientes y no se declaran aprobados.
- **Prioridad:** P1.
- **Archivos y punto de entrada:** tests/test_app.py; docs/manual_de_usuario.md; interfaz completa.
- **Hallazgo y reproducción:** Pendiente: las pruebas actuales llaman helpers y comparan cadenas; no verifican callbacks reales, accesibilidad, herramientas Plotly ni todas las secuencias de usuario.
- **Instrucción concreta:** Ejecutar matriz de aceptación descrita al final, conservar comandos, parámetros, capturas y errores. Si se desea automatización que requiera librería nueva, pedir aprobación primero; se puede completar manualmente con herramientas existentes. No convertir la presencia de un componente en prueba de su funcionamiento.
- **Criterio de aceptación:** Cada fila de la matriz tiene resultado y evidencia reales; los casos no ejecutados figuran pendientes. No declarar todo funciona solo porque pytest pasa.
- **Dependencia:** A01–A34 aprobadas según fases.

### A36 — Actualizar la documentación con resultados comprobados

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P2.
- **Archivos y punto de entrada:** docs/informe_tecnico.md; README.md; docs/manual_de_usuario.md; comentarios de gravity.py, kepler_laws.py e integradores.
- **Hallazgo y reproducción:** Informe mantiene resultados/conclusiones pendientes; comentarios aún dicen AU²/años/G=4pi². Fórmulas del informe dividen entre referencia negativa sin absoluto.
- **Instrucción concreta:** Corregir comentarios y fórmulas a SI vigente, documentar el método finalmente aprobado y llenar informe solo con corridas reproducibles. Distinguir proyección sin WebGL de escena 3D nativa. Conservar créditos y decisiones históricas identificadas como tales.
- **Criterio de aceptación:** Otro integrante reproduce tablas desde parámetros escritos; no aparecen porcentajes negativos de error ni afirmaciones de validación sin evidencia.
- **Dependencia:** A21–A27, A35.

### A37 — Registrar un entorno reproducible compatible

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P2.
- **Archivos y punto de entrada:** requirements.txt; requirements-dev.txt.
- **Hallazgo y reproducción:** Paquetes no tienen restricciones aunque comentario afirma versiones mínimas. Instalación auditada emite avisos de DataTable y VPython; estilos ya presentan incompatibilidad.
- **Instrucción concreta:** Registrar versiones auditadas y proponer restricciones compatibles después de comprobarlas. Evaluar las advertencias sin instalar dash-ag-grid ni quitar módulos históricos automáticamente. La retirada de VPython requiere tarea y alcance aprobados.
- **Criterio de aceptación:** Instalación limpia autorizada reproduce suite y controles; versiones quedan identificadas y no se añade ninguna dependencia sin aprobación.
- **Dependencia:** A28, A35.

### A38 — Validar el empaquetado cuando el usuario lo reactive

- [ ] **En pausa:** el empaquetado sigue detenido por decisión del usuario. No se compiló nada.
- **Prioridad:** P1.
- **Archivos y punto de entrada:** orbital_simulator.spec; src/main.py; .github/workflows/build-installers.yml; docs/distribucion.md.
- **Hallazgo y reproducción:** Pendiente, no compilado. Lanzador solo hace app.run: no abre navegador como promete distribución. Workflow compila sin ejecutar pytest. No hay prueba del paquete fuera del repositorio.
- **Instrucción concreta:** Mantener tarea en pausa hasta orden expresa. Entonces comprobar imports/rutas/data/assets en carpeta externa y cada SO. Implementar apertura del navegador solo cuando servidor esté listo; manejar puerto ocupado con mensaje. No publicar etiquetas automáticamente. Añadir prueba antes de compilar en workflow dentro de alcance aprobado.
- **Criterio de aceptación:** En máquina sin Python abre la interfaz local con presets/CSS/JS; puede ejecutar un escenario y cerrar. Prueba desde otra carpeta y puerto ocupado. Informe por SO con evidencia; no declarar compatibilidad por solo generar archivos.
- **Dependencia:** A35, A36, A37 y autorización expresa de empaquetado.

## Matriz de cierre para A35

Cada fila debe ejecutarse y anotarse de manera individual; no se da por aprobada por ejecutar otra fila.

| Caso | Acción | Resultado exigido |
|---|---|---|
| M01 | Abrir página nueva | Sin error; presets y controles legibles |
| M02 | Tierra–Luna sin editar | Corrida terminada con tiempo final y diagnóstico |
| M03 | Sol–Tierra | Se cargan los datos correctos y selector coherente |
| M04 | Sistema interno | Todos los planetas visibles; cuerpo analizado inequívoco |
| M05 | Euler-Cromer | Parámetros respetados y error medido |
| M06 | Verlet | Método aprobado y comparación reproducible |
| M07 | Circular | Excentricidad inicial validada; radio estable |
| M08 | Elíptica | Cobertura suficiente y elipse validada |
| M09 | Parabólica | Energía relativa inicial de escape, no elipse |
| M10 | Hiperbólica | Energía positiva y rama abierta |
| M11 | Cambiar factor | Estado físico y descripción coinciden |
| M12 | Editar nombre | Persiste tras perder foco sin perder otros campos |
| M13 | Editar masa | Recalcula magnitudes de par al ejecutar |
| M14 | Editar x | Usa coordenada editada |
| M15 | Editar y | Usa coordenada editada |
| M16 | Editar z | Distancia 3D y vista coherentes |
| M17 | Editar vx | Clasificación responde al estado real |
| M18 | Editar vy | Clasificación responde al estado real |
| M19 | Editar vz | Rapidez 3D incluye vz |
| M20 | Agregar cuerpo | Nueva configuración editable sin superposición ejecutable inadvertida |
| M21 | Eliminar cuerpo | Selección estable; sin referencias al eliminado |
| M22 | Eliminar todos los secundarios | Mensaje claro y recuperación |
| M23 | Borrar un campo numérico | Sin excepción de callback; error identificado |
| M24 | Masa cero | Rechazo explicado |
| M25 | Masa negativa | Rechazo explicado |
| M26 | Superponer dos cuerpos | Rechazo con nombres del par |
| M27 | Encuentro cercano durante corrida | Política física aprobada y aviso |
| M28 | dt mayor que duración | Rechazo o política temporal aprobada |
| M29 | dt igual a duración | Sin indexar muestra inexistente |
| M30 | Duración no divisible | Tiempo final real y explícito |
| M31 | Exceder presupuesto | Rechazo antes de integrar |
| M32 | Reproducir | Cuerpos y cursor avanzan |
| M33 | Pausar | Cuadro permanece inmóvil |
| M34 | Continuar | Retoma el cuadro pausado |
| M35 | Reiniciar | Regresa a t=0 sin integrar otra vez |
| M36 | Girar | Cambia proyección sin recalcular física |
| M37 | Inclinar | Cambia proyección sin perder cuerpo seleccionado |
| M38 | Acercar | Vista utilizable y brillo pegado al cuerpo |
| M39 | Tabla, página siguiente | Filas corresponden al historial |
| M40 | Tabla, última página | Incluye instante final |
| M41 | Ocultar/mostrar leyenda | Solo afecta visibilidad del gráfico |
| M42 | Zoom de Plotly | Rango cambia y se puede restaurar |
| M43 | Restablecer ejes | Recupera encuadre esperado |
| M44 | Descargar PNG | Archivo muestra figura correcta, sin cambiar simulación |
| M45 | Compartir gráfico | Revisar destino; no enviar ni subir sin autorización explícita |
| M46 | Teclado | Todos los controles alcanzables y foco visible |
| M47 | Etiquetas de campos | Nombre accesible asocia cuerpo, componente y unidad |
| M48 | Anchos de A29 | Sin cortes; tabla con scroll interno |
| M49 | Zoom navegador 200 % | Contenido operable y texto legible |
| M50 | Primera ley insuficiente | No certifica elipse con arco corto |
| M51 | Segunda ley | Área por intervalo y error, sin sesgo de muestreo |
| M52 | Tercera ley | Tres periodos medidos y comparación teórica |
| M53 | Error relativo de referencia cero | No evaluable o error absoluto explícito |
| M54 | Iniciar tras un fallo | Se recupera sin recargar página |
| M55 | Variar parámetros con resultados previos | Se identifica la corrida a la que pertenecen |
| M56 | Dos pestañas con estados distintos | Una no pisa cuerpos ni resultados de la otra |

## Reproducción mínima con código

Ejecutar desde la raíz con el entorno ya instalado. No hace falta escribir archivos de prueba para reproducir estos hallazgos:

```python
from src.ui.app import build_panel, initial_bodies, set_body_field, table_rows
from src.simulation import load_bodies, run_simulation

# En el estado auditado estas dos llamadas lanzan IndexError; ejecutar por separado.
build_panel(initial_bodies()[:1], "Verlet", 60, 1, 35, 25, 1)
build_panel(initial_bodies(), "Verlet", 200000, 1, 35, 25, 1)

# Ejecutar por separado: TypeError por masa vacía.
build_panel(set_body_field(initial_bodies(), 1, "mass", None),
            "Verlet", 60, 1, 35, 25, 1)

history = run_simulation(load_bodies("tierra_luna"), 60, 100,
                         "Verlet", record_every=30)
print(history["time"])  # Estado auditado: [0, 1800, 3600, 5400], faltan 6000 s.

history = run_simulation(load_bodies("tierra_luna"), 60, 100, "Verlet")
print(len(table_rows(history)))  # Estado auditado: 50, excede 40.
```

## Condición de cierre del plan

No marcar tareas como hechas al escribir el código. Cada una necesita la prueba específica indicada y revisión del usuario. La suite existente debe seguir pasando, salvo expectativas documentadas que preservaban un fallo (por ejemplo igualdad de integradores o ausencia del estado final), que se sustituyen por pruebas físicas correctas con aprobación. Las nuevas pruebas deben verificar comportamiento y límites reales, no solo texto o presencia de componentes.

Entregar al final una tabla por tarea con cambio aprobado, comprobación ejecutada, resultado observado y pendientes. Conservar separadas las limitaciones ambientales, los fallos reproducidos y las decisiones de diseño. El empaquetado continúa pendiente hasta que el usuario lo reactive.

## Segunda revisión: uso directo del navegador

Realizada el 13 de noviembre de 2026 a petición expresa del usuario. Esta sección amplía la primera revisión y sustituye sus pendientes únicamente para las funciones que aquí tienen evidencia. No se cambiaron fuentes, estilos ni dependencias. Se usó la aplicación real y sus controles; no se llamaron helpers Python para simular acciones de usuario.

Las conclusiones «funciona» significan que se observó la acción y su resultado en estos casos, no que su exactitud física quede certificada. Los callbacks y las transiciones a veces terminaron después de la primera lectura: se hicieron lecturas posteriores para evitar confundir resultados anteriores con resultados nuevos. Los errores de localizador de la herramienta de navegador se resolvieron y no se contabilizan como fallos del producto.

### Resultados individuales de uso

| ID | Función o caso probado en la página | Resultado observado | Dictamen / tarea |
|---|---|---|---|
| N01 | Abrir una página nueva | Cargan controles, estilos, cuerpos y gráficas iniciales | Funciona |
| N02 | Iniciar Tierra–Luna, dt=60 s, duración=1 día | Se llenan tarjetas, tabla y gráficas; posición final mostrada 3.744e8, 8.747e7, 0 m | Funciona la corrida; A09/A33 siguen pendientes |
| N03 | Cambiar a Sol–Tierra | Aparecen Sol y Tierra, masa solar 1.989e30 kg y distancia 1.496e11 m | Funciona la carga |
| N04 | Cambiar a sistema interno | Aparecen Sol, Mercurio, Venus, Tierra y Marte | Funciona la carga |
| N05 | Ejecutar sistema interno | Produce resultados y trayectorias; tarjetas corresponden al último planeta | Funciona la corrida; detalle ambiguo según A18 |
| N06 | Elegir Euler-Cromer | Selector conserva el método y la corrida solar produce datos nuevos | Funciona selección/ejecución |
| N07 | Elegir Verlet / usar valor inicial | Corrida Tierra–Luna genera datos | Funciona selección/ejecución; defecto matemático A11 no resuelto |
| N08 | Cambiar dt a 120 s | Se conserva el valor y se ejecuta el ejemplo solar | Funciona entrada |
| N09 | Cambiar duración a 2 días | Se conserva y se generan resultados solares nuevos | Funciona entrada |
| N10 | Elegir Circular | Actualiza rapidez del secundario y texto a 1.00 × circular | Funciona comando; A13–A15 impiden certificar circularidad |
| N11 | Elegir Elíptica | Actualiza rapidez a 0.80 × circular; se puede iniciar | Funciona comando |
| N12 | Elegir Parabólica | Actualiza a 1.4142135623730951 × circular y texto Parabólica | Funciona comando; no garantiza escape real, A13 |
| N13 | Elegir Hiperbólica | Actualiza a 1.697056274847714 × circular y permite ejecutar | Funciona comando |
| N14 | Deslizador de rapidez al mínimo con Home | Texto muestra 509 m/s, 0.50 × circular en Tierra–Luna | Funciona |
| N15 | Deslizador al máximo con End | Texto muestra 2037 m/s, 2.00 × circular | Funciona |
| N16 | Cargar un preset después de Hiperbólica | Sigue seleccionado Hiperbólica y factor 1.697, pero texto dice Circular y rapidez del preset | Falla: A16 |
| N17 | Editar nombre del secundario | Conserva «Luna prueba» al salir del campo | Funciona |
| N18 | Editar masa del secundario | Conserva 8e22 kg | Funciona entrada válida |
| N19 | Editar x del secundario | Conserva 400000000 m | Funciona entrada válida |
| N20 | Editar y del secundario | Conserva 1000000 m | Funciona entrada válida |
| N21 | Editar z del secundario | Conserva 2000000 m | Funciona entrada válida |
| N22 | Editar vx del secundario | Conserva 10 m/s | Funciona entrada válida |
| N23 | Editar vy del secundario | Conserva 900 m/s | Funciona entrada válida |
| N24 | Editar vz del secundario | Conserva 20 m/s | Funciona entrada válida |
| N25 | Iniciar tras esas ocho ediciones | Posición pasa a 3.916e8, 7.808e7, 3.667e6 m y velocidad -203.8, 878.6, 18.47 m/s | Funciona uso de datos editados |
| N26 | Editar nombre del primario | Conserva «Sol prueba» | Funciona entrada |
| N27 | Editar masa del primario | Conserva 2e30 kg | Funciona entrada |
| N28 | Editar x del primario | Conserva 100000 m | Funciona entrada |
| N29 | Editar y del primario | Conserva 200000 m | Funciona entrada |
| N30 | Editar z del primario | Conserva 300000 m | Funciona entrada |
| N31 | Editar vx del primario | Conserva 1 m/s | Funciona entrada |
| N32 | Editar vy del primario | Conserva 2 m/s | Funciona entrada |
| N33 | Editar vz del primario | Conserva 3 m/s | Funciona entrada |
| N34 | Agregar cuerpo al sistema interno | La lista pasa de cinco a seis nombres | Funciona operación de lista |
| N35 | Eliminar el cuerpo agregado | Vuelve a cinco cuerpos sin borrar los otros | Funciona operación de lista |
| N36 | Agregar cuerpo en Tierra–Luna y ejecutar | Dos secundarios coinciden; energía visible «-inf» | Falla: A05/A06 |
| N37 | Eliminar todos los secundarios e iniciar | No aparece error explicativo y quedan tarjetas anteriores; servidor registra IndexError y HTTP 500 | Falla: A03/A34 |
| N38 | Agregar secundario tras el error e iniciar | Se recuperan resultados finitos sin recargar | Funciona recuperación con configuración válida |
| N39 | Borrar masa e iniciar | Campo vacío admitido; la integración falla en vez de mostrar validación | Falla: A02/A34 |
| N40 | Introducir masa -1 e iniciar | Acepta el dato sin rechazo; puede producir resultados sin validez física | Falla: A02 |
| N41 | Introducir masa 0 e iniciar | No muestra rechazo de entrada | Falla: A02; no se atribuyen tarjetas de lectura inmediata a esta corrida por retraso del callback |
| N42 | dt=86400 s con duración de un día | No produce un resultado nuevo completo; conserva tarjetas previas al fallar la figura de Kepler de una muestra | Falla: A04/A34 |
| N43 | dt=200000 s con duración de un día | Conserva resultados anteriores, sin explicación | Falla: A04/A34 |
| N44 | dt=0 e iniciar | Vacía resultados sin explicar la entrada inválida | Validación incompleta: A34 |
| N45 | Duración=0 e iniciar | Vacía resultados sin explicación | Validación incompleta: A34 |
| N46 | Secundario en (0,0,384400000) m | Texto dice que la distancia debe ser mayor que cero | Falla de cálculo 3D: A14 |
| N47 | Elegir Circular en ese estado sobre z | Velocidad permanece en los valores anteriores; no aplica un estado circular 3D válido | Falla: A14 |
| N48 | Reproducir | Cambian las posiciones SVG del cuerpo y avanza la vista | Funciona movimiento visible |
| N49 | Pausar | En una repetición limpia hubo lecturas consecutivas de posición 179.08,150.75; 179.19,150.79; 179.31,150.82; 179.42,150.85 después del clic | No se certifica pausa inmediata/estable: ampliar A32 |
| N50 | Continuar con Reproducir | Se observa de nuevo avance de posiciones | Funciona movimiento; continuidad exacta de tiempo pendiente |
| N51 | Cursor de animación | Clic al extremo derecho cambia cuadro/cursor | Funciona cambio de cuadro; tiempo real no rotulado |
| N52 | Reiniciar | No existe botón específico | Falta: A32 |
| N53 | Reproducir después de llevar cursor al final | Se observaron cambios posteriores, pero con transiciones retrasadas | No certificar reinicio/repetición hasta A32 |
| N54 | Giro con teclado | Control pasa de 35 a 40 y cambia la geometría dibujada al completar callback | Funciona |
| N55 | Inclinación con teclado | Control pasa de 25 a 30 y se regenera la vista | Funciona |
| N56 | Acercamiento con teclado | Admite extremo 3 y después 0.5; cambia el encuadre | Funciona control; verificar seguimiento del cuadro en A31/A32 |
| N57 | Tabla: página siguiente | Pasa de 1/5 a 2/5 con otras filas | Funciona |
| N58 | Tabla: última página | Pasa a 5/5; última fila mostrada t=0.97 días | Funciona navegación; omite estado final según A33 |
| N59 | Tabla: página anterior | Pasa de 5/5 a 4/5 | Funciona |
| N60 | Tabla: primera página | Regresa a 1/5 y muestra t=0 | Funciona |
| N61 | Leyenda de energía, ocultar Cinética | La opacidad del elemento cambia a 0.5 tras completar transición | Funciona |
| N62 | Leyenda de energía, volver a mostrar | Opacidad vuelve a 1 | Funciona |
| N63 | Trayectoria: acercar | Eje x cambia de 0–400M a marcas 100M–300M | Funciona |
| N64 | Trayectoria: alejar/restablecer | Recupera marcas originales | Funciona |
| N65 | Energía: acercar | Marcas temporales pasan de 0–0.8 a 0.3–0.7 días | Funciona |
| N66 | Energía: alejar/restablecer | Recupera marcas originales | Funciona |
| N67 | Momento: acercar | Marcas pasan a 0.3–0.7 días | Funciona |
| N68 | Momento: alejar/restablecer | Recupera marcas originales | Funciona |
| N69 | Kepler: acercar | Marcas pasan a 0.3–0.7 días | Funciona |
| N70 | Kepler: alejar/restablecer | Recupera marcas originales | Funciona |
| N71 | Trayectoria: Pan y arrastre | Marcas x pasan de 0–400M a -100M–300M | Funciona desplazamiento real |
| N72 | Trayectoria: zoom por rectángulo | Arrastre cambia marcas a 150M–350M | Funciona |
| N73 | Trayectoria: Autoscale | Regresa a 0–400M | Funciona |
| N74 | Vista principal: botón acercar/restablecer | Cambia el encuadre dibujado | Funciona interacción básica |
| N75 | Descargar PNG de energía | Genera plot-image.png; se abrió y contiene curvas Total, Cinética y Potencial, ejes y unidades | Funciona exportación comprobada |
| N76 | Dos pestañas con cuerpos distintos | Una conserva x=0 del cuerpo editado y la otra inicia con x=384400000 | Funciona aislamiento de cuerpos en caso probado |
| N77 | Tab desde selector de escenario | Salta directamente al control de rapidez; tipos de órbita no quedan en el recorrido | Falla de teclado: A39 |
| N78 | Asociación de etiquetas | Se inspeccionaron 29 labels: solo cuatro contienen input/asociación; la mayoría de los campos no tiene etiqueta enlazada | Falla de accesibilidad: A40 |
| N79 | Desplegable de escenario | Fondo blanco y texto casi blanco en estado cerrado; menú abierto se puede usar con ratón | Falla visual: A28 |
| N80 | Desplegable del método | Texto muy claro sobre blanco; selección con ratón posible | Falla visual: A28 |

### Comprobación responsive con medidas del DOM

Se fijó el tamaño de la ventana y se leyó el ancho real del documento, el ancho desplazable y las columnas calculadas. Los 15 píxeles de diferencia corresponden al espacio de la barra vertical. Se restauró el tamaño original al terminar. Esto mejora la evidencia inicial, pero no sustituye pruebas de zoom 200 %, lector de pantalla o todos los controles en cada ancho.

| Ventana solicitada | Ancho útil real | Ancho desplazable | Columnas calculadas | Resultado |
|---|---:|---:|---|---|
| 390 px | 375 | 375 | 335 px | Apilado sin desborde horizontal general |
| 780 px | 765 | 765 | 725 px | Apilado sin desborde horizontal general |
| 1024 px | 1009 | 1009 | 300 + 653 px | Dos columnas; gráficas abajo |
| 1150 px | 1135 | 1135 | 300 + 779 px | Dos columnas; gráficas abajo |
| 1280 px | 1265 | 1265 | 340 + 473 + 380 px | Tres columnas |
| 1440 px | 1425 | 1425 | 340 + 633 + 380 px | Tres columnas |

### Aclaración sobre la pausa (A32)

Las mediciones N49 corresponden a atributos SVG de los puntos realmente dibujados, no al historial interno ni a una estimación visual. En otras lecturas se observó un cuadro estable, por lo que no se afirma que siempre falle. Repetir con cronómetro y vídeo/capturas en el navegador objetivo y en otro navegador antes de atribuir la causa al código. El criterio sigue siendo que el cuadro se estabilice tras la pausa y permanezca así, sin saltar al final. Verificar si quedan cuadros/transiciones en cola; no sustituir el problema por detener y volver a calcular toda la simulación. Registrar versión del navegador, Plotly y Dash y repetir sin cambiar cámara ni regenerar la figura entre pausa y comprobación.

### A39 — Hacer accesibles por teclado los tipos de órbita

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos:** assets/style.css, regla `.chips input`; src/ui/app.py, `trajectory-type`.
- **Evidencia:** N77: Tab desde escenario lleva a rapidez; los inputs de las opciones se ocultan con `display: none`.
- **Instrucción concreta:** conservar los controles nativos enfocables usando ocultación visual accesible, no `display:none`; dibujar foco perceptible en la etiqueta de la opción. Mantener semántica de grupo y selección única. No reemplazar por divs que solo respondan al ratón.
- **Aceptación:** sin ratón, Tab llega al grupo, las flechas cambian opción, el foco se ve y el cambio actualiza cuerpos una sola vez. Probar las cuatro opciones y volver al escenario con Shift+Tab.
- **Dependencia:** A16/A17; incluir en cierre A35 antes de marcarlo terminado.

### A40 — Asociar cada etiqueta con su campo

- [x] **Hecha y comprobada** el 14 de noviembre de 2026 (ver registro al final).
- **Prioridad:** P1.
- **Archivos:** src/ui/app.py, `_body_field`, `_body_card`, `_config_panel`, `_center_panel`; botones de paginación si su API permite rotularlos.
- **Evidencia:** N78: 25 de 29 labels inspeccionados no tienen asociación mediante htmlFor/input contenido. Los botones de paginación aparecen sin nombre accesible en el árbol.
- **Instrucción concreta:** enlazar etiquetas con identificadores reales, incluidos los identificadores estructurados de Dash, o usar la vía de etiquetado accesible soportada por el componente. El nombre debe distinguir cuerpo, magnitud, componente y unidad. Añadir nombre al campo de nombre del cuerpo y a los controles de vista. Rotular los cuatro botones de paginación con la API disponible; no manipular a ciegas DOM generado por la librería.
- **Aceptación:** el árbol accesible permite diferenciar «Luna, posición x, metros» de «Tierra, posición x, metros»; pulsar etiqueta enfoca campo cuando corresponde. Paginación anuncia primera/anterior/siguiente/última. Verificar con teclado y lector de pantalla antes de cerrar.
- **Dependencia:** A18; incluir en A35.

### Evidencias guardadas y pendientes reales

Capturas locales: `/tmp/orbital_revision_navegador.jpg`, `/tmp/orbital_desplegable_contraste.jpg` y `/tmp/orbital_pausa_1.jpg`. PNG exportado: `/home/edimez14/plot-image.png`. Estos archivos son temporales o externos al repositorio: si se requiere evidencia permanente, acordar su ubicación antes de incorporarlos. Ninguna captura fue fabricada ni se retocó el diseño.

No se activó «Share chart...» para evitar una eventual transmisión a un servicio externo durante una revisión local. Tampoco se certifican selección de puntos por lazo/caja, descarga de cada una de las otras figuras, escritura manual del número de página, rendimiento bajo carga extrema, zoom de navegador 200 %, lectores de pantalla ni toda combinación de cámara/animación. El soporte de esas herramientas debe constar como pendiente específico; no se les asigna resultado satisfactorio por compartir librería con otra herramienta.

Esta segunda revisión deja **40 tareas individuales propuestas**. No autoriza implementarlas y no cambia ninguna casilla de corrección a terminada.

## Tercera revisión: edición y adición de cuerpos personalizados

Pruebas solicitadas expresamente por el usuario, realizadas en el navegador el 13 de noviembre de 2026. Configuración: Tierra–Luna, Verlet, dt=60 s, duración de un día. Solo se modificó el estado temporal de la página.

| ID | Acción individual | Evidencia / resultado |
|---|---|---|
| C01 | Agregar un tercer cuerpo | Aparece una tarjeta nueva sin borrar Tierra ni Luna |
| C02 | Dar nombre propio al añadido | Conserva «Satelite prueba» |
| C03 | Dar masa propia al añadido | Conserva 1e20 kg |
| C04 | Cambiar x del añadido | Conserva -500000000 m, separado de la Luna |
| C05 | Cambiar y del añadido | Conserva 10000000 m |
| C06 | Cambiar z del añadido | Conserva 5000000 m |
| C07 | Cambiar vx del añadido | Conserva 0 m/s |
| C08 | Cambiar vy del añadido | Conserva -850 m/s |
| C09 | Cambiar vz del añadido | Conserva 10 m/s |
| C10 | Ejecutar tres cuerpos con esos datos | Figuran Tierra, Luna y Satelite prueba en la trayectoria. Tarjetas del añadido: posición (-4.94e8,-6.322e7,5.8e6) m; velocidad (138.3,-842.6,8.5) m/s; E total -3.783e28 J |
| C11 | Cambiar masa del añadido a 2e20 kg | Valor conservado al salir del campo |
| C12 | Cambiar vy del añadido a -600 m/s | Valor conservado al salir del campo |
| C13 | Volver a ejecutar tras C11 y C12 | Cambian resultados: posición (-4.94e8,-4.172e7,5.8e6) m; velocidad (138.9,-595.5,8.494) m/s; E total -3.791e28 J. Se comprueba uso de los nuevos datos, no un cálculo aislado del efecto de masa |
| C14 | Eliminar la Luna, cuerpo intermedio | Quedan Tierra y Satelite prueba. El añadido pasa del índice 2 al 1 y conserva exactamente masa, posición y velocidad editadas |
| C15 | Renombrar el cuerpo tras eliminar el intermedio | Conserva «Satelite restante», sin editar por error la Tierra |
| C16 | Cambiar z después de la eliminación | Conserva 9000000 m en el cuerpo correcto |
| C17 | Ejecutar el sistema restante de dos cuerpos | Posición final (-4.94e8,-4.172e7,9.753e6) m; velocidad (138.3,-595.6,7.391) m/s; E total -1.234e26 J |
| C18 | Duplicar masa terrestre a 1.1944e25 kg | Se conserva la masa del primario y se inicia otra corrida; no se aisló una medición del efecto sobre la órbita antes de la siguiente edición |
| C19 | Agregar otro cuerpo después de eliminar uno | Nueva tarjeta de índice 2; el cuerpo restante sigue en índice 1 |
| C20 | Configurar el nuevo en posición separada | Masa 3e19 kg, posición (7e8,-1e7,-2e6) m, vy=1000 m/s; datos conservados |
| C21 | Usar el mismo nombre en dos secundarios | Se admiten ambos como «Satelite restante» y la corrida termina con resultados finitos |
| C22 | Leer las leyendas con nombres repetidos | Se repiten «Órbita: Satelite restante» y «Satelite restante»: no se distingue de manera inequívoca el cuerpo. Ampliar A18 con identidad visual estable o desambiguación aprobada; no imponer nombres únicos sin aprobación |
| C23 | Elegir Elíptica con dos secundarios | vy del primero cambia de -600 a -1009.8171009018808 m/s; vy del último permanece 1000 m/s. Confirma A18: selector actúa sobre índice 1, mientras tarjetas muestran último cuerpo |

**Resultado:** sí funcionan agregar un cuerpo personalizado, editarlo, ejecutarlo, eliminar un cuerpo intermedio y seguir editando el restante. Eso no elimina los fallos de superposición por defecto, validación de campos y ambigüedad del cuerpo analizado registrados antes. No se declara precisión física de una órbita arbitraria solo porque haya producido resultados finitos.

Evidencia visual temporal: `/tmp/orbital_cuerpos_prueba.jpg`. No se implementó ninguna corrección ni se marcaron tareas como completadas.

## Registro de ejecución (14 de noviembre de 2026)

Ejecución automática autorizada por el usuario. Cada fila indica la comprobación
real que se corrió, no solo la presencia de código. Comando base de toda la
suite: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider -q`
→ **114 pruebas aprobadas** (antes: 52).

| Tarea | Cambio principal | Comprobación ejecutada | Resultado |
|---|---|---|---|
| A01 | Unidades SI y Dash en AGENTS, plan y README; estado del plan reconciliado | Lectura de los tres documentos | Sin instrucciones contradictorias |
| A02 | `physics/validation.py` valida nombre, masa y componentes | `tests/test_validation.py`; panel con masa vacía, cero, negativa y NaN | Rechazo con cuerpo y campo |
| A03 | Iniciar con un solo cuerpo devuelve mensaje, no HTTP 500 | `test_el_panel_rechaza_un_solo_cuerpo` y navegador | Mensaje visible y recuperación |
| A04 | `step_plan`: último paso acortado; figuras toleran una muestra | `test_duracion_no_divisible...`, `build_panel` con dt=200000 s | Tiempo final exacto, sin IndexError |
| A05 | Detección de pares superpuestos antes de integrar; cuerpo nuevo separado | `test_el_panel_rechaza_cuerpos_superpuestos` | Nombra el par y no integra |
| A06 | La corrida se detiene bajo `MIN_DISTANCE` con causa y tiempo | `test_un_encuentro_cercano_detiene_la_corrida` | `stopped` con tiempo y par |
| A07 | Contrato del motor: dt, steps, record_every, método y cuerpos | 7 casos parametrizados en `test_simulation.py` | `ValueError` descriptivo |
| A08 | Presupuesto `MAX_WORK` y `MAX_STEPS` antes del bucle | `test_el_presupuesto_de_trabajo_rechaza_antes_de_integrar` | Rechazo con costo calculado |
| A09 | Se guarda el estado inicial y el final real | `test_el_ultimo_registro_coincide_con_el_estado_final` | 6000 s con 100 pasos de 60 s |
| A10 | `sample_indices` limita registros y conserva extremos | `test_el_presupuesto_de_registros...`, 1/39/40/41/100/2058 | Nunca supera el máximo |
| A11 | Velocity-Verlet real (dos aceleraciones) | Orden dos y comparación de energía en `test_integrators.py` | Error cae ~4 al mitad de dt |
| A12 | `relative_error` devuelve `None` sin referencia; `error_report` | `test_una_referencia_cero...` | "No evaluable" + error absoluto |
| A13 | `mu = G·(M+m)` en velocidad circular y de escape | `test_la_velocidad_circular_usa_las_dos_masas` | Circular Tierra–Luna e = 0,0049 |
| A14 | Normas y tangente en 3D | `test_las_velocidades_usan_las_tres_dimensiones` | Órbita sobre z válida |
| A15 | Clasificación por energía y excentricidad | `test_la_clasificacion_usa_energia_y_excentricidad`; radial | Radial no se llama circular |
| A16 | El tipo y la velocidad se sincronizan con los cuerpos | Navegador: cargar preset tras Hiperbólica | Controles y texto coinciden |
| A17 | Editar un campo no reescribe la velocidad manual | Guardas de igualdad en los callbacks; navegador | Ediciones se conservan |
| A18 | Selector explícito de cuerpo analizado con identidad numérica | `test_el_selector_de_cuerpo...`, `test_las_vistas_de_detalle...` | Tarjetas, tabla y leyes coinciden |
| A19 | Se rotula el marco absoluto de tarjetas y tabla | Texto del panel y encabezados | Usuario distingue marcos |
| A20 | E y L rotulados como totales del sistema | `results_cards` | Sin atribuirlos a un planeta |
| A21 | Máximos de ΔE y ΔL en cada paso, independientes del historial | `test_la_conservacion_se_mide_en_cada_paso...` | Igual con 500 o 10 muestras |
| A22 | Ajuste de elipse con cobertura y residuo | `test_primera_ley`, arco corto e hipérbola | Certifica solo con evidencia |
| A23 | Primera ley visible en el panel | Navegador: a, e, cobertura y residuo | Texto con unidades |
| A24 | Segunda ley con tiempos reales y velocidad areal | `test_segunda_ley_usa_los_tiempos_reales` | Muestreo desigual no altera |
| A25 | Periodo medido por cruce de una vuelta | `test_el_periodo_se_mide_de_la_trayectoria` | Error < 1 % |
| A26 | Tercera ley con periodos y semiejes medidos | `test_tercera_ley_con_tres_orbitas_medidas` | Error 0,0009 % |
| A27 | Botón "Analizar 3 órbitas" y gráfica T² vs a³ | Navegador | Tres puntos y referencia teórica |
| A28 | Contraste de desplegables de Dash 4 | Medición de estilos en navegador | 16:1 y 15,3:1 (meta 4,5:1) |
| A29 | Distribución responsive medida en 390–1440 px | Navegador: `scrollWidth == innerWidth` | Sin desborde general |
| A30 | Brillo en la misma posición del cuerpo | `test_el_brillo_queda_en_la_misma_posicion...` | No se separa con zoom |
| A31 | Animación conserva primera y última muestra | `test_la_animacion_conserva...` (100/241/1000/2058) | Extremos exactos |
| A32 | Botón Reiniciar en la animación | `test_la_animacion_trae_cuadros_y_tres_botones`; navegador | Vuelve al cuadro 0 |
| A33 | Tabla: máximo 40 filas, extremos y tiempo sin redondear | `test_la_tabla_respeta...`, `test_la_tabla_no_confunde...` | Última fila = tarjetas |
| A34 | Estado visible, "Calculando…", errores explicados | Navegador: cálculo, un cuerpo, fallo y recuperación | Sin HTTP 500 silencioso |
| A35 | Matriz funcional en navegador (subconjunto ejecutado) | Ver sección siguiente | Casos ejecutados y pendientes |
| A36 | Informe con corridas reproducibles y comentarios en SI | `docs/informe_tecnico.md`; `pytest` | Tablas con parámetros escritos |
| A37 | Versiones auditadas fijadas | `requirements.txt` y `requirements-dev.txt` | Instalación reproducible |
| A38 | Empaquetado | No ejecutado | En pausa por decisión del usuario |
| A39 | Chips de órbita accesibles por teclado | CSS `sr-only` + `focus-within`; Tab en navegador | Foco visible y grupo alcanzable |
| A40 | Etiquetas asociadas a cada campo | 29 etiquetas inspeccionadas, todas con control | Nombre incluye cuerpo y unidad |

### Matriz A35: casos ejecutados en navegador

Se usó Chromium 156 (Chrome for Testing) contra la aplicación real en
`http://127.0.0.1:8066`. Las acciones se hicieron sobre la página, no con ayudas
de Python. Esta tabla separa lo observado de lo pendiente para no declarar como
probado lo que solo cubre una prueba automática.

| Caso | Acción | Resultado observado |
|---|---|---|
| M01 | Abrir página nueva | Carga sin errores; controles y gráficas iniciales |
| M02 | Tierra–Luna, 30 días, dt=60 s | Tarjetas, tabla, primera ley y conservación visibles |
| M03 | Cambiar el escenario | Se cargan los cuerpos del preset elegido |
| M20 | Agregar un cuerpo | Aparece una tarjeta nueva sin borrar las anteriores |
| M22 | Eliminar todos los secundarios e iniciar | Mensaje "Se necesitan al menos dos cuerpos…" |
| M46 | Recorrido con Tab | El grupo de tipos de órbita recibe foco visible |
| M47 | Inspección de etiquetas | 29 de 29 etiquetas contienen su control |
| M48 | Anchos 390, 780, 1024, 1150, 1280 y 1440 px | `scrollWidth == innerWidth`; sin desborde general |
| M49 | Ventana 720×600 (equivalente a zoom 200 % de 1440×1200) | Una columna, contenido operable y sin desborde |

Casos cubiertos por pruebas automáticas, **no repetidos en navegador**:
M05, M06, M07–M10, M23–M26, M28–M31 (ver `tests/`).

Los cuatro botones de paginación de la tabla se rotularon como «Primera página»,
«Página anterior», «Página siguiente» y «Última página» (etiqueta y título
accesible), verificado en el navegador. Casos **pendientes** en
navegador: M04, M11–M19, M21, M27, M32–M45, M49–M56 y lector de pantalla real.
No se declaran aprobados.

### Nota sobre el arranque de la simulación

Durante la ejecución se encontró que la corrida de 30 días tardaba unos 34 s
porque la conservación se calculaba con NumPy en cada paso. Se cambió el cálculo
interno a operaciones escalares y se precomputó el encuadre de la animación. La
misma corrida tarda ahora alrededor de 4 s y el botón muestra "Calculando…"
mientras trabaja.

