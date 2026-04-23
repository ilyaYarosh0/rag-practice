import docx
import hashlib

def get_file_hash(file_path):
    #"""Генерирует уникальный ID на основе содержимого файла."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Читаем файл блоками, чтобы не забивать память
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def parse_doc_to_paragraph_chunks(file_path):
    doc_id = get_file_hash(file_path)
    doc = docx.Document(file_path)

    chunks=[]
    paragraph_counter = 0

    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()

        if not text:
            continue
        paragraph_counter +=1

        chunk_data = {
            "document_id": doc_id,
            "paragraph_id": f"{doc_id}_{paragraph_counter}",
            "text": text,
            "metadata":{
                "source_file": file_path,
                "paragraph_index": i
            }
        }
        chunks.append(chunk_data)
    return chunks

path = r'C:\Users\user\Documents\A_dinner_party.docx'

result= parse_doc_to_paragraph_chunks(path)

print(f"Document ID: {result[0]['document_id']}")
print(f"First Paragraph ID: {result[0]['paragraph_id']}")
print(f"Content: {result[0]['text']}")