# AI Cleaner – Uso en español

## ¿Qué es?

Un módulo que limpia textos generados por IA para que suenan humanos:
- Elimina frases típicas de IA.
- Evita reencuadres (“no es X, es Y”).
- Usa lenguaje directo y párrafos cortos.

## Componentes

- `delete_ai_words.py`: función principal en Python.
- `post_processor.py`: capa final para cualquier pipeline de IA.
- `ai_cleaner_service.dart`: servicio para Flutter.
- `ai_cleaner_prompt.txt`: prompt para usar con IAs.

## Uso en Python

```python
from ai_cleaner.delete_ai_words import delete_ai_words

texto_original = "En el mundo actual es importante destacar que..."
texto_humano = delete_ai_words(texto_original)