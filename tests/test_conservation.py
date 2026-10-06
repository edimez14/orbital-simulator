# código nuevo edizon
"""test_conservation.py — Pruebas de conservación de energía y momento angular.

¿Para qué sirve?
    Verificar que `physics/conservation.py` calcula bien la energia mecanica y el
    momento angular, y que el integrador los conserva dentro de la tolerancia.

¿Por qué existe?
    Es el criterio objetivo para validar el metodo numerico. Si energia o momento
    angular se disparan, el integrador o la gravedad estan mal.

¿Qué contendrá? (aún sin implementar)
    - Prueba de energia cinetica, potencial y total en un caso conocido.
    - Prueba del momento angular en una orbita circular.
    - Comprobacion de que la variacion relativa se mantiene <= 1 %.

¿Cómo ejecutarlo? (cuando este implementado)
    pytest tests/test_conservation.py

¿Cómo modificarlo?
    Cambiar la tolerancia en un solo lugar y documentar por que.
"""
