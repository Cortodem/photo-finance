# CHANGES

## Alcance
- Revision enfocada en ./backend como MVP.

## Faltantes detectados
- Falta backend/.env.example, referenciado en backend/README.md.
- Falta backend/ejemplo_uso.py, referenciado en backend/README.md.
- Faltan backend/extractors/__init__.py, backend/storage/__init__.py y backend/test/__init__.py si se desea tratarlos como paquetes (el README los lista).
- El README describe la raiz como pdf_extractor/, pero en este repo la raiz funcional es backend/.
- El script backend/runt_test.py indica ejecutar run_tests.py; el nombre real del archivo es runt_test.py.
- No hay carpetas de ejemplo pdfs/ ni output_json/ (se crean en runtime, pero no hay datos de muestra).
