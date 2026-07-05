from typing import List

# Vocabulario prohibido por estilo IA (lista resumida pero funcional)
BANNED_WORDS = [
    "delve", "realm", "harness", "unlock", "tapestry", "paradigm",
    "cutting-edge", "revolutionize", "intricate", "intricacies",
    "showcasing", "crucial", "pivotal", "surpass", "meticulously",
    "vibrant", "unparalleled", "underscore", "leverage", "synergy",
    "innovative", "game-changer", "testament", "commendable",
    "meticulous", "highlight", "emphasize", "boast", "groundbreaking",
    "align", "foster", "showcase", "enhance", "holistic", "garner",
    "accentuate", "pioneering", "trailblazing", "unleash", "versatile",
    "transformative", "redefine", "seamless", "optimize", "scalable",
    "robust", "breakthrough", "empower", "streamline", "frictionless",
    "elevate", "adaptive", "effortless", "data-driven", "insightful",
    "proactive", "mission-critical", "visionary", "disruptive",
    "reimagine", "unprecedented", "intuitive", "leading-edge",
    "synergize", "democratize", "accelerate", "state-of-the-art",
    "dynamic", "immersive", "predictive", "transparent", "proprietary",
    "integrated", "plug-and-play", "turnkey", "future-proof",
    "paradigm-shifting", "supercharge", "enduring", "interplay",
    "valuable", "captivate",
    # Versiones en español populares
    "innovador", "revolucionario", "optimizar", "transformador",
    "sinergia", "clave", "pivotal", "crítico", "detallar", "explorar",
    "desgranar", "inmerse", "ecosistema", "impulsar", "potenciar",
    "alinear", "facilitar", "promover", "maximizar", "robusto",
    "ágil", "eficiente", "escalable", "sin paralelo", "vibrante"
]

# Frases de relleno típicas de IA
BANNED_OPENINGS = [
    "en el mundo actual",
    "es importante destacar",
    "es importante señalar",
    "vale la pena mencionar",
    "vamos a explorar",
    "vamos a desgranar",
    "vamos a profundizar",
    "en conclusión",
    "en resumen",
    "a continuación",
    "sin duda",
    "cabe señalar",
    "como hemos visto",
    "partiendo de esta base",
]

BANNED_TRANSITIONS = [
    "además",
    "por otro lado",
    "en otro orden de cosas",
    "no obstante",
    "con todo",
    "a fin de cuentas",
    "en última instancia",
]

BANNED_PATTERNS = [
    # Reencuadres negativos (prohibido: "no es X, es Y")
    r"no es (.*), (es|son) (.*?)",
    r"no se trata de (.*), (se trata de|es) (.*?)",
    r"no solo (.*), (también|pero también) (.*?)",
    r"no es solo (.*), (es|también) (.*?)",
    r"olvida (.*), (enfócate en|concentra en) (.*?)",
    r"deja (.*), (piensa en|enfócate en) (.*?)",
]


def delete_ai_words(text: str) -> str:
    """
    Reescribe un texto para que suene humano y elimina patrones típicos de IA.
    Entrada: str
    Salida: str humanizado.
    """
    if not text or not text.strip():
        return text

    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = clean_line(line)
        if line and not is_filler_line(line):
            cleaned_lines.append(line)

    # Reunir líneas, pero sin perder saltos de párrafo importantes
    result = "
".join(cleaned_lines)

    # Eliminar reencuadres negativos (no es X, es Y → es Y)
    result = remove_negative_parallelism(result)

    # Ajustar ritmos: evitar párrafos de una sola línea si no son necesarios
    result = normalize_paragraphs(result)

    return result.strip()


def clean_line(line: str) -> str:
    """Aplica reglas básicas de una línea."""
    original = line

    # Eliminar palabras prohibidas (con sustitución por versión simple si es posible)
    for word in BANNED_WORDS:
        if word in line.lower():
            # Sustituir por versión simple o eliminar adjetivo
            line = line.replace(word, "")
            line = line.replace(word.capitalize(), "")

    # Eliminar frases de relleno
    for phrase in BANNED_OPENINGS:
        if phrase in line.lower():
            line = line.lower().replace(phrase, "")

    for phrase in BANNED_TRANSITIONS:
        if phrase in line.lower():
            line = line.lower().replace(phrase, "")

    # Simplificar verbos inflados:
    # "sirve como" → "es"
    # "representa" → "es"
    # "ofrece" → "tiene" / "da"
    line = line.replace("sirve como", "es")
    line = line.replace("sirven como", "son")
    line = line.replace("representa", "es")
    line = line.replace("representan", "son")
    line = line.replace("ofrece", "tiene")
    line = line.replace("ofrecen", "tienen")
    line = line.replace("busca", "quier")
    line = line.replace("buscan", "quieren")
    line = line.replace("apunta a", "va a")
    line = line.replace("apuntan a", "van a")

    # Eliminar construcciones “no es X, es Y” dentro de la línea
    # (se hace más completo en remove_negative_parallelism)

    return line.strip()


def is_filler_line(line: str) -> bool:
    """Devuelve True si la línea es casi solo relleno."""
    if not line:
        return True
    # Si solo tiene frases de relleno o está muy vacía
    lower = line.lower()
    for phrase in BANNED_OPENINGS:
        if lower == phrase:
            return True
    return len(line.strip()) < 5


def remove_negative_parallelism(text: str) -> str:
    """
    Elimina patrones tipo:
      "no es X, es Y" → "es Y"
      "no se trata de X, se trata de Y" → "se trata de Y"
    Manteniendo el significado.
    """
    import re

    patterns = [
        r"no es (.*), (es|son) (.*?)",
        r"no es una (.*), (es|son) (.*?)",
        r"no se trata de (.*), (se trata de|es) (.*?)",
        r"no solo (.*), (también|pero también) (.*?)",
        r"no es solo (.*), (es|también) (.*?)",
        r"olvida (.*), (enfócate en|concentra en) (.*?)",
        r"deja (.*), (piensa en|enfócate en) (.*?)",
    ]

    for pat in patterns:
        text = re.sub(pat, lambda m: m.group(3) if m.group(3) else m.group(2), text, flags=re.IGNORECASE)

    return text


def normalize_paragraphs(text: str) -> str:
    """
    Evita párrafos de una sola línea muy corta si no son necesarios.
    """
    paragraphs = text.split("

")
    cleaned = []

    for p in paragraphs:
        lines = [l.strip() for l in p.splitlines() if l.strip()]
        if len(lines) == 1 and len(lines[0]) < 60:
            # Intenta unir con el siguiente párrafo si existe
            if len(cleaned) > 0:
                cleaned[-1] = cleaned[-1] + " " + lines[0]
                continue
        cleaned.append("
".join(lines))

    return "

".join(cleaned)
