// código nuevo edizon
// a11y.js — Mejoras de teclado para los desplegables de Dash 4.
//
// Qué hace: el desplegable de Dash 4 se dibuja como un botón con tabindex -1,
// así que el teclado no puede llegar a él. Este archivo le devuelve el foco y le
// pone un nombre accesible tomado de su etiqueta visible.
//
// Por qué existe: la tarea A39 exige que todos los controles se alcancen con Tab
// y la tarea A40 que cada control tenga nombre. Se hace sobre las clases reales
// del DOM ya inspeccionado, no a ciegas.
//
// Cómo cambiarlo: si Dash cambia el nombre de la clase, ajustar el selector.

(function () {
    "use strict";

    function labelFor(button) {
        if (!button.id) {
            return null;
        }
        return document.querySelector('label[for="' + button.id + '"]');
    }

    function enhance(button) {
        if (button.getAttribute("tabindex") !== "0") {
            button.setAttribute("tabindex", "0");
        }
        var label = labelFor(button);
        if (label) {
            var value = button.querySelector(".dash-dropdown-value-item");
            var text = label.textContent.trim();
            if (value && value.textContent.trim()) {
                text = text + ": " + value.textContent.trim();
            }
            button.setAttribute("aria-label", text);
            // aria-labelledby gana sobre aria-label; se retira para que el
            // nombre incluya el campo y no solo el valor elegido.
            button.removeAttribute("aria-labelledby");
        }
    }

    // Botones de paginación de la tabla: Dash los dibuja solo con un icono.
    // Se rotulan por su clase estable (tarea A40).
    var PAGINATION_NAMES = {
        "first-page": "Primera página",
        "previous-page": "Página anterior",
        "next-page": "Página siguiente",
        "last-page": "Última página"
    };

    function enhancePagination() {
        Object.keys(PAGINATION_NAMES).forEach(function (className) {
            document.querySelectorAll("button." + className).forEach(function (button) {
                if (button.getAttribute("aria-label") !== PAGINATION_NAMES[className]) {
                    button.setAttribute("aria-label", PAGINATION_NAMES[className]);
                    button.title = PAGINATION_NAMES[className];
                }
            });
        });
    }

    function enhanceAll() {
        document.querySelectorAll("button.dash-dropdown").forEach(enhance);
        enhancePagination();
    }

    function start() {
        enhanceAll();
        var observer = new MutationObserver(enhanceAll);
        observer.observe(document.body, { childList: true, subtree: true, characterData: true });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start);
    } else {
        start();
    }
})();
