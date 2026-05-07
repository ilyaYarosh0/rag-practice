from datasets import load_dataset
import chromadb
from ner import generate_metadata, get_fixed_chunks
import re
from work_with_doc import process_folder

FOLDER_PATH = r'./Files'

client = chromadb.HttpClient(host='localhost', port=8000)

client.delete_collection(name = "world_info_full")

collection = client.get_or_create_collection(
    name="world_info_full",
    metadata={"hnsw:space": "cosine"}
)

if collection.count() ==0:
    print("База пуста. Начинаю загрузку документов...")
    documents, metadatas, ids = process_folder(FOLDER_PATH, 50, 0)
    collection.add(documents=documents, metadatas=metadatas, ids=ids)
else: 
    print(f"База готова. В коллекции уже {collection.count()} записей.")

while True:

    # filter_input = input("\nВведите номер чанка для фильтрации или нажмите Enter чтобы пропустить: ")
    # where_condition = None

    # if filter_input.strip():
    #     try:
    #         chunk_num = int(filter_input.strip())
    #         where_condition = {"chunk_number": chunk_num}
    #     except ValueError:
    #         print("Ошибка: введено не число. Поиск будет выполнен по всем чанкам")
    #         where_condition = None

    # raw_input = input("\nВведите фильтр в формате Ключ:Значение, Ключ:Значение ")
    # where_condition= None
    # condition_query_list= []
    # if raw_input.strip():
    #     splitted_input = raw_input.split(",")
    #     for filter_input in splitted_input: 
    #         parts= filter_input.split(":")
    #         if len(parts) ==2:
    #             filter_key = parts[0].strip()
    #             filter_value = parts[1].strip()
    #             condition_query_list.append({filter_key: {"$contains": filter_value}})
    #     if len(condition_query_list) == 1:
    #         where_condition = condition_query_list[0]
    #     elif len(condition_query_list) > 1:
    #         where_condition = {"$and": condition_query_list}

    user_query = input("\nТвой запрос (или 'exit'): ")
    
    if user_query.lower() in ['выход', 'exit', 'quit']:
        break

    results = collection.query(
        query_texts=[user_query],
        n_results= 5,
        #where = where_condition, 
        include=["documents", "distances", "metadatas"] 
    )

    print("\n--- РЕЙТИНГ ОТВЕТОВ (Сходимость) ---")
    
    for i in range(len(results['ids'][0])):
        chunk_id = results['ids'][0][i] 
        distance = results['distances'][0][i]
        metadata = results['metadatas'][0][i]
        
        similarity = 1 - distance
        
        source_file = metadata.get("source_file", "Unknown")
        start_para = metadata.get("start_paragraph", "N/A")
        doc_id = metadata.get("doc_id", "N/A")

        # Получаем текст конкретного чанка для текущей итерации
        chunk_text = results['documents'][0][i]

        print(f"{i+1}. ID: {chunk_id}")
        print(f"   Сходимость: {similarity:.4f}")
        print(f"   Файл: {source_file} | Параграф: {start_para} | DocID: {doc_id}")
        
        # Печатаем только нужный текст
        print(f"   Текст: {chunk_text}") 
        print("-" * 30)