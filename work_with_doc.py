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

def recursive_chunking(text, chunk_size=500, overlap_pct=0.1,separators=None):
    if separators is None:
        separators = ["\n\n", "\n", " ", ""]

    if len(text) <= chunk_size:
        return [text]
    
    for i, sep in enumerate(separators):
        if sep in text:
            raw_text = text.split(sep)
            curent_len = 0
            curent_doc = []
            chunks = []
            
            for f in raw_text:
                # Если фрагмент больше лимита, обрабатываем его рекурсивно отдельно
                if len(f) > chunk_size:
                    # Сбрасываем накопленную очередь перед вставкой рекурсивных чанков
                    if curent_doc:
                        chunks.append(sep.join(curent_doc))
                        curent_doc = []
                        curent_len = 0
                    
                    # Готовые чанки добавляем напрямую в массив, без повторного join
                    chunks.extend(recursive_chunking(f, chunk_size, overlap_pct, separators[i+1:]))
                    continue

                if curent_len + len(f) + len(sep) > chunk_size:
                    full_chunk = sep.join(curent_doc)
                    chunks.append(full_chunk)

                    overlap_size =int(curent_len*overlap_pct)
                    
                    words = full_chunk.split(" ")
                    tail_words = []
                    tail_len = 0
                    for word in reversed(words):
                        word_len = len(word) + (1 if tail_words else 0)
                        if tail_len + word_len > overlap_size and tail_words:
                            break
                        tail_words.insert(0, word)
                        tail_len +=word_len
                    overlap_text = " ".join(tail_words)

                    curent_doc = [overlap_text] if overlap_text else []
                    curent_len = len(overlap_text)

                if curent_doc:
                    curent_len +=len(sep)
                curent_doc.append(f)
                curent_len += len(f)
            
            if curent_doc:
                chunks.append(sep.join(curent_doc))
            
            return chunks

    return [text[:chunk_size]]

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
#chunks = recursive_chunking(raw_text)
chunks = recursive_chunking(raw_text)

print(f"ОБРАБОТКА ФАЙЛА: {path}")
print(f"Общая длина текста: {len(raw_text)} симв.")
print(f"Количество созданных чанков: {len(chunks)}")
print("=" * 50)

for i, chunk_text in enumerate(chunks):
    print(f"ЧАНК #{i + 1} | Размер: {len(chunk_text)} симв.")
    print("-" * 30)
    print(chunk_text)
    print("=" * 50)