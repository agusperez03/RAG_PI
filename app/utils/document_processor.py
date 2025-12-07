import os
import uuid
from pypdf import PdfReader
import re


def extract_text_from_pdf(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return ""

    content = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text() or ""
            content += text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

    # Limpiar el texto
    # Reemplazar múltiples saltos de línea por un espacio
    content = content.replace('\n', ' ')
    
    # Reemplazar múltiples espacios por uno solo
    content = ' '.join(content.split())
    
    return content.strip()


def split_into_paragraphs(text):
    import re
    
    # Encontrar todas las posiciones de ":"
    colon_positions = [m.start() for m in re.finditer(r':', text)]
    
    if not colon_positions:
        # Si no hay ":", devolver el texto completo
        return [text] if text.strip() else []
    
    split_positions = []
    
    for colon_pos in colon_positions:
        # Buscar el último "." antes de este ":"
        text_before_colon = text[:colon_pos]
        last_dot_pos = text_before_colon.rfind('.')
        
        if last_dot_pos != -1:
            # Agregar la posición justo después del punto
            split_positions.append(last_dot_pos + 1)
    
    # Eliminar duplicados y ordenar
    split_positions = sorted(set(split_positions))
    
    if not split_positions:
        return [text] if text.strip() else []
    
    paragraphs = []
    
    # Agregar el primer párrafo si hay contenido antes del primer split
    if split_positions[0] > 0:
        first_part = text[:split_positions[0]].strip()
        if first_part:
            paragraphs.append(first_part)
    
    # Dividir en los puntos encontrados
    for i, start in enumerate(split_positions):
        end = split_positions[i + 1] if i + 1 < len(split_positions) else len(text)
        paragraph = text[start:end].strip()
        if paragraph:
            paragraphs.append(paragraph)
    
    return paragraphs

def process_document():
    file_path = "data/Document.pdf"
    text = extract_text_from_pdf(file_path)

    if not text.strip():
        print("Document content is empty.")
        return []

    paragraphs = split_into_paragraphs(text)

    chunks = []
    for i, paragraph in enumerate(paragraphs):
        chunk = {
            "id": str(uuid.uuid4()),
            "content": paragraph,
            "language": "es",
            "title": f"Parrafo_{i+1}"
        }
        chunks.append(chunk)

    return chunks

def store_chunks():
    from app.services.vector_store import get_collection
    from app.services.embeddings import get_embeddings_cohere

    chunks = process_document()
    if not chunks:
        print("No chunks to store.")
        return

    # -----------------------------------------
    # 🔍 Imprimir los chunks antes de embeddings
    # -----------------------------------------
    print("\n===== CHUNKS GENERADOS =====")
    for i, c in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ---")
        print(f"ID: {c['id']}")
        print(f"Título: {c['title']}")
        print(f"Idioma: {c['language']}")
        print("Contenido:")
        print(c["content"])
    print("\n===== FIN CHUNKS =====\n")
    # -----------------------------------------

    collection = get_collection()
    embedder = get_embeddings_cohere()

    ids = [c["id"] for c in chunks]
    documents = [c["content"] for c in chunks]
    metadatas = [{"title": c["title"], "language": c["language"]} for c in chunks]

    embeddings = embedder.embed_documents(documents)

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB.")


if __name__ == "__main__":
    store_chunks()
