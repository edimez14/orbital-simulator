# Graph Report - orbital-simulator  (2026-11-14)

## Corpus Check
- Corpus is ~35,014 words - fits in a single context window. You may not need a graph.

## Summary
- 409 nodes · 822 edges · 32 communities (18 shown, 14 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21
- Community 22
- Community 24
- Community 31

## God Nodes (most connected - your core abstractions)
1. `Body` - 31 edges
2. `run_simulation()` - 25 edges
3. `step()` - 19 edges
4. `load_bodies()` - 19 edges
5. `build_panel()` - 18 edges
6. `orbit_animation()` - 13 edges
7. `mechanical_energy()` - 12 edges
8. `_orbit_view()` - 12 edges
9. `escape_velocity()` - 11 edges
10. `initial_bodies()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `test_mas_masa_mayor_escape()` --calls--> `escape_velocity()`  [INFERRED]
  tests/test_controls.py → src/physics/gravity.py
- `test_velocidad_de_escape_conocida()` --calls--> `escape_velocity()`  [INFERRED]
  tests/test_controls.py → src/physics/gravity.py
- `test_orbita_circular_conserva_energia_y_momento()` --calls--> `step()`  [EXTRACTED]
  tests/test_conservation.py → src/integrators/euler_cromer.py
- `test_orbita_circular_se_cierra()` --calls--> `step()`  [EXTRACTED]
  tests/test_integrators.py → src/integrators/euler_cromer.py
- `_orbita_relativa()` --calls--> `step()`  [EXTRACTED]
  tests/test_kepler.py → src/integrators/euler_cromer.py

## Import Cycles
- None detected.

## Communities (32 total, 14 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (20): animation_from(), build_panel(), _empty_figure(), update_panel(), _add_body(), _base_layout(), _body_color(), _body_traces() (+12 more)

### Community 1 - "Community 1"
Cohesion: 0.13
Nodes (12): relative_error(), plot_angular_momentum(), plot_energy(), plot_swept_area(), plot_third_law(), _save(), test_variacion_relativa(), _revisar() (+4 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (10): add_body_to(), apply_speed(), apply_trajectory(), circular_speed(), remove_body_at(), set_body_field(), trajectory_speed(), update_bodies() (+2 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (12): _body_card(), _body_field(), build_layout(), _center_panel(), _config_panel(), _header(), _plots_panel(), render_bodies() (+4 more)

### Community 4 - "Community 4"
Cohesion: 0.15
Nodes (6): step(), Body, test_radio_casi_constante_y_orbita_cerrada(), test_orbita_eliptica(), test_trayectoria_hiperbolica_escapa(), test_guarda_los_datos_iniciales()

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (6): convertir_markdown_a_pdf(), encontrar_fuente(), limpiar_celdas(), main(), project_root(), test_el_estilo_se_adapta_a_pantallas_pequenas()

### Community 6 - "Community 6"
Cohesion: 0.16
Nodes (8): angular_momentum(), kinetic_energy(), mechanical_energy(), potential_energy(), test_energia_cinetica(), test_energia_potencial(), test_momento_angular(), test_orbita_circular_conserva_energia_y_momento()

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (20): runs-on, steps, strategy, jobs, build, os, name, on (+12 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (7): create_scene(), _create_sphere(), _draw_axes(), _draw_stars(), update(), test_mas_masa_mayor_escape(), test_velocidad_de_escape_conocida()

### Community 9 - "Community 9"
Cohesion: 0.16
Nodes (9): load_bodies(), run_simulation(), orbit_figure(), test_la_animacion_dibuja_solo_el_recorrido_recorrido(), test_la_animacion_trae_cuadros_y_botones(), test_la_vista_de_la_orbita_no_usa_webgl(), test_la_vista_mantiene_el_acercamiento_entre_cuadros(), test_la_vista_trae_ejes_estrellas_orbita_y_cuerpos() (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.16
Nodes (8): body_to_dict(), dict_to_body(), initial_bodies(), test_con_datos_invalidos_el_panel_queda_vacio(), test_el_texto_de_velocidades_menciona_la_de_escape(), test_elegir_escenario_carga_sus_cuerpos(), test_iniciar_usa_los_cuerpos_del_panel(), test_los_cuerpos_del_panel_van_y_vuelven()

### Community 11 - "Community 11"
Cohesion: 0.18
Nodes (7): _sistema(), test_distinto_paso_cambia_el_resultado(), test_el_historial_guarda_tiempo_energia_momento_y_posiciones(), test_guardar_cada_ciertos_pasos_reduce_el_historial(), test_la_energia_se_conserva_con_los_dos_metodos(), test_la_energia_total_es_cinetica_mas_potencial(), _variacion_maxima()

### Community 12 - "Community 12"
Cohesion: 0.22
Nodes (6): check_first_law(), _orbita_relativa(), _periodo_circular(), test_primera_ley(), test_segunda_ley(), test_tercera_ley()

### Community 13 - "Community 13"
Cohesion: 0.21
Nodes (4): compute_accelerations(), _sol_y_tierra(), test_aceleracion_coincide_con_el_calculo_a_mano(), test_la_fuerza_atrae()

### Community 14 - "Community 14"
Cohesion: 0.20
Nodes (6): step(), _error_maximo_de_energia(), _sistema_tierra(), test_orbita_circular_se_cierra(), test_verlet_avanza_el_estado(), test_verlet_conserva_la_energia_igual_que_euler_cromer()

### Community 15 - "Community 15"
Cohesion: 0.16
Nodes (7): _card(), results_cards(), _short(), _short_vector(), table_rows(), test_las_tarjetas_y_la_tabla_coinciden_con_las_graficas(), test_las_tarjetas_y_la_tabla_se_llenan()

### Community 17 - "Community 17"
Cohesion: 0.20
Nodes (5): escape_velocity(), orbit_kind(), show_velocities(), velocities_text(), test_el_tipo_de_orbita_sale_de_la_velocidad()

### Community 18 - "Community 18"
Cohesion: 0.29
Nodes (3): check_second_law(), check_third_law(), swept_area()

## Knowledge Gaps
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Body` connect `Community 4` to `Community 2`, `Community 6`, `Community 9`, `Community 10`, `Community 11`, `Community 12`, `Community 13`, `Community 14`, `Community 28`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08773784355179703 - nodes in this community are weakly interconnected._
- **Why does `escape_velocity()` connect `Community 17` to `Community 2`, `Community 8`, `Community 10`, `Community 12`, `Community 13`, `Community 16`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.12807881773399016 - nodes in this community are weakly interconnected._
- **Why does `run_simulation()` connect `Community 9` to `Community 0`, `Community 2`, `Community 6`, `Community 10`, `Community 11`, `Community 12`, `Community 15`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._