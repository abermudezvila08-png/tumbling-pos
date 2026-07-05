class AiCleanerService {
  // Prompt que puedes usar en llamadas a IA
  static const prompt = '''
Eres un redactor humano. Tu tarea: rebobinar cualquier texto que te envíe para que suene natural, como si lo escribiera una persona real.

Reglas:
- Elimina frases típicas de IA ("en el mundo actual", "vamos a explorar", "no es X, es Y").
- Usa lenguaje directo, sin exageraciones.
- Párrafos cortos (1–2 frases).
- No inventes información; solo cambia el estilo.
- Si el texto es técnico, mantén la precisión pero con palabras simples.
- Devuelve solo el texto limpio, sin explicaciones.
  ''';

  /// Ejemplo de uso:
  /// - Envías: textoOriginal, prompt
  /// - IA devuelve: textoHumanizado
  /// - Este método lo limpia aún más si la IA no sigue las reglas al 100%.
  static String humanize(String textoOriginal) {
    // Aquí podrías llamar a un backend Python que usa delete_ai_words
    // Si no tienes backend, puedes hacer una llamada a una API de IA con el prompt.
    // Para empezar, devuelve el texto original; luego conectas la API.
    return textoOriginal;
  }
}