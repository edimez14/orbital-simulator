<!-- código nuevo edizon -->
# Pruebas de escenarios

Este folder agrupa las **pruebas de escenarios físicos** del simulador. Un
escenario es una configuración inicial concreta (masa, radio y velocidad) que debe
producir un tipo de órbita conocido.

## Diferencia con las pruebas unitarias

| Tipo      | Ubicación           | Qué comprueba |
|-----------|---------------------|---------------|
| Unitaria  | `tests/test_*.py`   | Una función aislada (gravedad, integrador, conservación, Kepler). |
| Escenario | `tests/scenarios/`  | El sistema completo produce la órbita esperada. |

Las unitarias verifican **piezas**. Los escenarios verifican el **todo**.

## Escenarios previstos (PDF sección 5.2)

1. **Circular**   — velocidad tangencial igual a la velocidad circular.
2. **Elíptica**   — velocidad menor que la circular y menor que la de escape.
3. **Hiperbólica** — velocidad mayor que la velocidad de escape.

## Paquetes

Todo se ejecuta con **pytest** (mismo framework para unitarias y escenarios),
más `pytest-cov` para cobertura. Están en `requirements-dev.txt`.

## Cómo ejecutar (cuando estén implementados)

```bash
pip install -r requirements-dev.txt
pytest                        # todas las pruebas
pytest tests/scenarios        # solo los escenarios
pytest --cov=src              # con cobertura
```

## Cómo agregar un escenario

1. Crear un archivo `test_scenario_<nombre>.py` en este folder.
2. Definir las condiciones iniciales (masa, radio, velocidad).
3. Simular y comparar contra el resultado teórico dentro de la tolerancia.
