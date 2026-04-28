import docx
import hashlib

def get_full_text(file_path):
    doc = docx.Document(file_path)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return full_text

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
    buf_paragraph = ""

    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        print(f"{i} {para.text}\n\n")
        if len(text) !=0:
            buf_paragraph += text + " "
        else:
            if buf_paragraph.strip():
                paragraph_counter +=1

                chunk_data = {
                    "document_id": doc_id,
                    "paragraph_id": f"{doc_id}_{paragraph_counter}",
                    "text": buf_paragraph,
                    "metadata":{
                        "source_file": file_path,
                        "paragraph_index": i
                    }
                }
                chunks.append(chunk_data)
                buf_paragraph = ""

    if buf_paragraph.strip():
                paragraph_counter +=1

                chunk_data = {
                    "document_id": doc_id,
                    "paragraph_id": f"{doc_id}_{paragraph_counter}",
                    "text": buf_paragraph,
                    "metadata":{
                        "source_file": file_path,
                        "paragraph_index": i
                    }
                }
                chunks.append(chunk_data)
    return chunks


def _split_to_atoms(text, chunk_size, separators):

    if len(text) <= chunk_size or not separators:
        return [text]
    
    sep = separators[0]
    if sep not in text:
        return _split_to_atoms(text, chunk_size, separators[1:])
    
    parts = text.split(sep)
    atoms = []
    for p in parts:
        if len(p) > chunk_size:
            atoms.extend(_split_to_atoms(p, chunk_size, separators[1:]))
        elif p.strip():
            atoms.append(p + sep)
    return atoms

def get_chunks(text, chunk_size=500, overlap_pct=0.2):
    separators = ["\n\n", "\n", ". ", " ", ""]
    overlap_size = int(chunk_size * overlap_pct)

    atoms = _split_to_atoms(text, chunk_size, separators)
    
    chunks = []
    current_chunk = ""
    
    for atom in atoms:
        if len(current_chunk) + len(atom) <= chunk_size:
            current_chunk += atom
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            raw_ov = current_chunk[-overlap_size:]

            break_point = -1
            for s in ["\n", " ", "."]:
                pos = raw_ov.find(s)
                if pos != -1 and (break_point == -1 or pos < break_point):
                    break_point = pos
            
            overlap_text = raw_ov[break_point:].lstrip() if break_point != -1 else raw_ov
            current_chunk = overlap_text + atom

    if current_chunk:
        last_str = current_chunk.strip()
        if chunks and len(last_str) < (chunk_size * 0.25):
            chunks[-1] = chunks[-1] + "\n" + last_str
        else:
            chunks.append(last_str)
            
    return chunks


def get_metadata_for_recursive_chunking(raw_text, chunk_size=500, overlap_pct=0.1,separators=None):

    raw_chunks = recursive_chunking(
        text=raw_text, 
        chunk_size=chunk_size, 
        overlap_pct=overlap_pct, 
        separators=separators
        )
    
    final_chunk = []
    for i, chunk_text in enumerate(raw_chunks):

        pass

    return final_chunk
#path = r'C:\Users\user\Documents\A_dinner_party.docx'
path = r'Kursach.docx'

raw_text = get_full_text(path)

chunks = get_chunks(raw_text)

print(f"ОБРАБОТКА ФАЙЛА: {path}")
print(f"Общая длина текста: {len(raw_text)} симв.")
print(f"Количество созданных чанков: {len(chunks)}")
print("=" * 50)

for i, chunk_text in enumerate(chunks):
    print(f"ЧАНК #{i + 1} | Размер: {len(chunk_text)} симв.")
    print("-" * 30)
    print(chunk_text)
    print("=" * 50)