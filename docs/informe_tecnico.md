# código nuevo edizon
# Informe Técnico — Simulador Orbital y Leyes de Kepler

Documento de resultados del proyecto. Solo se escriben cifras obtenidas con
corridas reproducibles en el entorno del repositorio.

## 1. Introducción

El simulador predice el movimiento orbital a partir de condiciones iniciales.
Relaciona una ley física continua (gravitación universal) con un procedimiento
numérico paso a paso (Euler-Cromer o velocity-Verlet) y comprueba el resultado con
magnitudes medibles: conservación de energía y momento angular, y las tres leyes
de Kepler.

## 2. Marco teórico

- Ley de Gravitación Universal y Segunda Ley de Newton.
- Energía mecánica: E = K + U, con U = -G·m_i·m_j/r_ij.
- Momento angular: L = Σ r_i × (m_i·v_i).
- Integración numérica: Euler-Cromer y velocity-Verlet.
- Leyes de Kepler: elipse con foco, áreas iguales y T² ∝ a³.

## 3. Metodología

- Unidades internas: SI (m, kg, s); la interfaz muestra el tiempo en días.
- Métodos: Euler-Cromer y velocity-Verlet, ambos con paso `dt` configurable.
- Escenarios: Tierra–Luna, Sol–Tierra y sistema solar interno, más cuerpos
  agregados o editados por el usuario.
- Duración: si no es múltiplo de `dt`, el último paso se acorta para integrar
  exactamente el tiempo pedido.
- Tolerancia objetivo: 1 % en la variación de E y L y en las leyes de Kepler.
- La conservación se mide en cada paso de la integración, no solo en las muestras
  que se dibujan.

## 4. Resultados

Corrida de referencia: **Tierra–Luna**, `dt = 60 s`, duración **30 días**
(2.592.000 s), 43.200 pasos, historial limitado a 2.000 muestras.

| Método | Variación máxima de E | Variación máxima de L | Estado |
|---|---:|---:|---|
| Euler-Cromer | 8,10 × 10⁻⁵ % | 9,43 × 10⁻¹³ % | Cumple 1 % |
| velocity-Verlet | 1,28 × 10⁻⁸ % | 9,43 × 10⁻¹³ % | Cumple 1 % |

Primera ley (misma corrida, cuerpo analizado: Luna):

| Magnitud | Valor medido |
|---|---:|
| Semieje mayor `a` | 3,825 × 10⁸ m |
| Excentricidad `e` | 0,0049 |
| Cobertura angular | 398° |
| Residuo del ajuste | 1,0 × 10⁻¹⁰ (fracción de `a`) |
| Conclusión | Elipse válida |

Segunda ley (misma corrida): velocidad areal media constante; variación máxima
**1,39 × 10⁻⁵ %** (meta 1 %). El cálculo usa los tiempos reales de cada muestra,
así que cambiar el muestreo de la pantalla no altera el diagnóstico.

Tercera ley (tres órbitas circulares alrededor de la Tierra, radios 0,6, 1,0 y
1,5 veces el radio lunar):

| Constante T²/a³ (s²/m³) | Valor |
|---|---:|
| Órbita 1 | 9,7846002444 × 10⁻¹⁴ |
| Órbita 2 | 9,7846002445 × 10⁻¹⁴ |
| Órbita 3 | 9,7846002445 × 10⁻¹⁴ |
| Teórica 4π²/[G·(M+m)] | 9,7846896646 × 10⁻¹⁴ |
| Error máximo | 0,0009 % (meta 1 %) |

En el caso llamado parabólico, la velocidad aplicada corresponde al escape del par
(`v = √(2·G·(M+m)/r)`), así que su energía específica relativa es cero. El estado
se clasifica por energía y vector de excentricidad, no por una banda de rapidez.

## 5. Análisis de error

El error relativo de una magnitud X se calcula con el valor absoluto de la
referencia, para que funcione igual con energías negativas:

    Error = |X_sim - X_ref| / |X_ref| × 100 %

Para conservación se usa la variación respecto al valor inicial:

    ΔX(t) = |X(t) - X(0)| / |X(0)| × 100 %

Si la referencia es cero (por ejemplo una energía cercana al escape, o un momento
angular nulo en movimiento radial), el porcentaje no está definido: la interfaz
muestra **"no evaluable"** y el error absoluto en sus unidades. No se usa un
epsilon arbitrario que produzca un porcentaje engañoso.

## 6. Conclusiones

- Los dos integradores conservan energía y momento angular muy por debajo del 1 %
  en la corrida de referencia; velocity-Verlet es más preciso que Euler-Cromer con
  el mismo paso.
- La primera ley se comprueba con un ajuste de elipse y cobertura de casi una
  vuelta completa; un arco corto no se certifica.
- La segunda ley se comprueba con velocidad areal y tiempos reales.
- La tercera ley se comprueba con tres periodos medidos y se compara con la
  referencia teórica que incluye las dos masas.
- Estas cifras no prueban todos los parámetros posibles. Un `dt` demasiado grande
  produce un aviso de conservación y un acercamiento por debajo del mínimo detiene
  la corrida con causa y tiempo, en lugar de devolver un infinito como éxito.

## 7. Limitaciones

- No se validó el empaquetado (PyInstaller) porque está en pausa por decisión del
  usuario.
- No se certifican Windows ni macOS desde este entorno Linux.
- No se probaron lectores de pantalla reales; sí la estructura de etiquetas y el
  recorrido con teclado.
- El módulo histórico de VPython sigue instalado pero la interfaz no lo usa.

## 8. Referencias

Ver sección 10 de `docs/Pre-Proyecto Grupo 6.pdf`. El detalle de correcciones y
su evidencia está en `docs/auditoria_y_plan_de_correccion.md`.
