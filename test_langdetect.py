
# Pruebas de uso de langdetect. Se determinó no usarlo ya que puede fallar para preguntas cortas (por ejemplo caso 2).

# Text                                | Detected  
# --------------------------------------------------
# Who is Zara?                        | en        
# What did Emma decide to do?         | pt        
# Hello world                         | en        
# Quien es Zara?                      | es

from langdetect import detect

def test_language_detection():
    test_cases = [
        # English
        "Who is Zara?",
        "What did Emma decide to do?",
        "Hello world",
        
        # Spanish
        "Quien es Zara?",
        "¿Quién es Zara?", # With punctuation
        "Hola mundo",
        
        # Portuguese
        "Quem é Zara?",
        "Como você está?",
        
        # Ambiguous / Short
        "Zara",
        "No",
        "Si",
    ]

    print(f"{'Text':<35} | {'Detected':<10}")
    print("-" * 50)

    for text in test_cases:
        try:
            lang = detect(text)
            print(f"{text:<35} | {lang:<10}")
        except Exception as e:
            print(f"{text:<35} | Error: {e}")

if __name__ == "__main__":
    try:
        test_language_detection()
    except ImportError:
        print("Error: langdetect not installed. Please run: pip install langdetect")
