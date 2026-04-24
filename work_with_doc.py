import docx
import hashlib

def get_full_text(file_path):
    doc = docx.Document(file_path)
    # Собираем текст каждого абзаца в список и склеиваем через \n
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

    chunks = []

    if len(text) <= chunk_size:
        chunks.append(text)
        return chunks
    
    for i, sep in enumerate(separators):
        if sep in text:
            raw_text = text.split(sep)
            all_fragments=[]
            for splitted_text in raw_text:
                all_fragments.extend(recursive_chunking(splitted_text, chunk_size, overlap_pct, separators[i+1:]))         
            curent_len =0
            curent_doc = []
            for f in all_fragments:

                if curent_len + len(f) + len(sep) > chunk_size:
                    chunks.append(sep.join(curent_doc))

                    overlap_size =int(curent_len*overlap_pct)
                    while curent_len > overlap_size:
                        removed = curent_doc.pop(0)
                        curent_len-= len(removed)
                        if curent_doc:
                            curent_len -=len(sep)
                if curent_doc:
                    curent_len +=len(sep)
                curent_doc.append(f)
                curent_len += len(f)
            
            if curent_doc:
                chunks.append(sep.join(curent_doc))
            
            return chunks

    return [text[:chunk_size]]

#path = r'C:\Users\user\Documents\A_dinner_party.docx'
path = r'receipts.docx'

raw_text = get_full_text(path)
chunks = recursive_chunking(raw_text)
# result= parse_doc_to_paragraph_chunks(path)
# for chunk in result:
#     print(f"Document ID: {result[0]['document_id']}")
#     print(f"Paragraph ID: {chunk['paragraph_id']}")
#     print(f"Content: {chunk['text']}")
print(f"ОБРАБОТКА ФАЙЛА: {path}")
print(f"Общая длина текста: {len(raw_text)} симв.")
print(f"Количество созданных чанков: {len(chunks)}")
print("=" * 50)

for i, chunk_text in enumerate(chunks):
    print(f"ЧАНК #{i + 1} | Размер: {len(chunk_text)} симв.")
    print("-" * 30)
    print(chunk_text) # Сам текст чанка
    print("=" * 50)