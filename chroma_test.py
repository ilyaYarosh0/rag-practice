import chromadb

client = chromadb.HttpClient(host='localhost', port=8000)

try:
    client.delete_collection(name="world_info_full")
except Exception:
    pass

collection = client.create_collection(name="world_info_full", metadata={"hnsw:space": "cosine"})

splitted_text = [
        "This territory features diverse landscapes ranging from the coastal plains in the north and west to the majestic Alpine mountain ranges. The official national tongue is celebrated for its melodic flow, distinct pronunciation, and widespread influence within the sphere of international diplomacy. Gastronomy here focuses on seasonal ingredients, exquisite cheeses, fine wines, and traditional techniques like slow braising or crafting delicate puff pastries.",
        "The terrain spans from the sandy Baltic and North Sea coasts through rolling central uplands to the jagged peaks of the Alps. The primary tongue is known for its complex grammar, compound words, and its role as a major medium for classical philosophy. The culinary tradition emphasizes hearty portions of roasted meats, diverse bread varieties, fermented cabbage, and a world-renowned culture of beer brewing.",
        "The region encompasses the world's largest territory, including vast Siberian forests, the Ural Mountains, and diverse climates stretching across two continents. The primary Slavic language uses the Cyrillic alphabet, serving as a vital lingual bridge across Northern Asia and parts of Eastern Europe. Local food features warming staples like beet soup, savory dumplings, buckwheat porridge, and preserved vegetables essential for surviving the long winters.",
        "The massive territory includes the arid Gobi Desert, fertile eastern river basins, and the high Himalayan plateau along its southern borders. The official speech utilizes a logographic writing system where thousands of intricate characters represent specific concepts rather than individual phonetic sounds. Cooking is defined by regional diversity, mastering the balance of flavors through techniques like stir-frying, steaming, and use of aromatic spices."
    ]

final_chunks = []
final_metadatas = []
final_ids = []

for i, text in enumerate(splitted_text):
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    page_number = i + 1 
    
    for j, sentence in enumerate(sentences):
        final_chunks.append(sentence + ".")
        
        chunk_number = j + 1 
        
        # Метаданные только на основе номеров
        final_metadatas.append({
            "page": page_number,
            "chunk_number": chunk_number,
            "global_index": len(final_chunks) - 1
        })
        
        # Генерация ID: page1_1, page1_2... page4_3
        final_ids.append(f"page{page_number}_{chunk_number}")

print(f"Всего чанков: {len(final_chunks)}\n")
for i in range(len(final_chunks)):
    print(f"ID: {final_ids[i]} | Мета: {final_metadatas[i]}")
    print(f"Текст: {final_chunks[i]}\n")

collection.add(
    documents=final_chunks, 
    metadatas=final_metadatas,
    ids=final_ids
)

while True:


    filter_input = input("\nВведите номер чанка для фильтрации или нажмите Enter чтобы пропустить: ")
    where_condition = None

    if filter_input.strip():
        try:
            chunk_num = int(filter_input.strip())
            where_condition = {"chunk_number": chunk_num}
        except ValueError:
            print("Ошибка: введено не число. Поиск будет выполнен по всем чанкам")
            where_condition = None
    
    user_query = input("\nТвой запрос (или 'exit'): ")
    
    if user_query.lower() in ['выход', 'exit', 'quit']:
        break

    results = collection.query(
        query_texts=[user_query],
        n_results=len(sentence),
        where = where_condition, 
        include=["documents", "distances", "metadatas"] 
    )

    print("\n--- РЕЙТИНГ ОТВЕТОВ (Дистанция) ---")
    
    for i in range(len(results['ids'][0])):
        chunk_id = results['ids'][0][i] 
        distance = results['distances'][0][i]
        metadata = results['metadatas'][0][i]
        
        page_val = metadata.get('page', 'N/A')
        chunk_val = metadata.get('chunk_number', 'N/A')
        
        print(f"{i+1}. ID: {chunk_id} | Мета: [Номер страны {page_val}, Чанк {chunk_val}] | Дистанция: {distance:.4f}")