# Anti-Patterns

## 1) Skills sin contrato de salida

Problema: respuestas ambiguas y no auditables.
Correccion: definir formato de salida, criterios de aceptacion y checklist final.

## 2) Agentes con demasiadas skills activas sin priorizacion

Problema: respuestas incoherentes o contradictorias.
Correccion: usar seleccion por dominio + limite maximo + modo `hybrid` controlado.

## 3) Cambios grandes sin benchmark/regression

Problema: mejoras locales rompen comportamientos previos.
Correccion: ejecutar `make quality` antes de merge.

## 4) Versionado manual inconsistente

Problema: historial de cambios opaco.
Correccion: usar `semantic_version_manager.py` + bundle release automatizado.

## 5) Prompts sin base logica

Problema: alucinaciones y pasos sin sentido.
Correccion: foundations de matematicas/programacion en skill y agent metadata.
