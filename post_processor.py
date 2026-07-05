from .delete_ai_words import delete_ai_words


def post_process_ai_output(text: str) -> str:
    """
    Última capa de limpieza para cualquier salida de IA.
    Aplica las mismas reglas de delete_ai_words.
    """
    return delete_ai_words(text)
