---
type: community
cohesion: 0.15
members: 23
---

# Community 4

**Cohesion:** 0.15 - loosely connected
**Members:** 23 nodes

## Members
- [[Avanza el estado del sistema un paso `dt` con Euler-Cromer. Recibe bodies …]] - rationale - src/integrators/euler_cromer.py
- [[Body]] - code - src/physics/bodies.py
- [[Con v = 0.8·v_c a = 1.1e11 m y e = 0.36 (dentro del 1 %).]] - rationale - tests/scenarios/test_scenario_elliptical.py
- [[Con v = 1.2·v_escape la distancia crece sin volver y E ≥ 0.]] - rationale - tests/scenarios/test_scenario_hyperbolic.py
- [[Con v = v_c el radio varía menos del 1 % y la órbita se cierra.]] - rationale - tests/scenarios/test_scenario_circular.py
- [[Escenario de prueba trayectoria hiperbólica. ¿Para qué sirve Comprobar que…]] - rationale - tests/scenarios/test_scenario_hyperbolic.py
- [[Escenario de prueba órbita circular. ¿Para qué sirve Comprobar que con una…]] - rationale - tests/scenarios/test_scenario_circular.py
- [[Escenario de prueba órbita elíptica. ¿Para qué sirve Comprobar que con una…]] - rationale - tests/scenarios/test_scenario_elliptical.py
- [[Un cuerpo celeste su masa, posición y velocidad actuales.]] - rationale - src/physics/bodies.py
- [[bodies.py]] - code - src/physics/bodies.py
- [[bodies.py — Define qué es un cuerpo celeste. ¿Para qué sirve Representar un…]] - rationale - src/physics/bodies.py
- [[euler_cromer.py]] - code - src/integrators/euler_cromer.py
- [[euler_cromer.py — Integrador de Euler-Cromer. ¿Para qué sirve Avanzar el…]] - rationale - src/integrators/euler_cromer.py
- [[step()]] - code - src/integrators/euler_cromer.py
- [[test_bodies.py]] - code - tests/test_bodies.py
- [[test_bodies.py — Pruebas de la clase `Body`. ¿Para qué sirve Comprobar que un…]] - rationale - tests/test_bodies.py
- [[test_guarda_los_datos_iniciales()]] - code - tests/test_bodies.py
- [[test_orbita_eliptica()]] - code - tests/scenarios/test_scenario_elliptical.py
- [[test_radio_casi_constante_y_orbita_cerrada()]] - code - tests/scenarios/test_scenario_circular.py
- [[test_scenario_circular.py]] - code - tests/scenarios/test_scenario_circular.py
- [[test_scenario_elliptical.py]] - code - tests/scenarios/test_scenario_elliptical.py
- [[test_scenario_hyperbolic.py]] - code - tests/scenarios/test_scenario_hyperbolic.py
- [[test_trayectoria_hiperbolica_escapa()]] - code - tests/scenarios/test_scenario_hyperbolic.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_4
SORT file.name ASC
```

## Connections to other communities
- 17 edges to [[_COMMUNITY_Community 12]]
- 16 edges to [[_COMMUNITY_Community 6]]
- 11 edges to [[_COMMUNITY_Community 13]]
- 7 edges to [[_COMMUNITY_Community 14]]
- 4 edges to [[_COMMUNITY_Community 10]]
- 3 edges to [[_COMMUNITY_Community 11]]
- 2 edges to [[_COMMUNITY_Community 2]]
- 1 edge to [[_COMMUNITY_Community 28]]
- 1 edge to [[_COMMUNITY_Community 9]]

## Top bridge nodes
- [[Body]] - degree 31, connects to 9 communities
- [[bodies.py]] - degree 15, connects to 7 communities
- [[step()]] - degree 19, connects to 4 communities
- [[euler_cromer.py]] - degree 12, connects to 4 communities
- [[test_scenario_hyperbolic.py]] - degree 10, connects to 3 communities