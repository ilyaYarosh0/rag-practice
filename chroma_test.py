import chromadb
from ner import generate_metadata

client = chromadb.HttpClient(host='localhost', port=8000)

try:
    client.delete_collection(name="world_info_full")
except Exception:
    pass

collection = client.create_collection(name="world_info_full", metadata={"hnsw:space": "cosine"})

splitted_text = [
# Страна 1 (France)
"This territory is located in Western Europe and features diverse landscapes ranging from the coastal plains in the north to the majestic Alpine mountain ranges. It borders the Atlantic Ocean to the west and the Mediterranean Sea to the south. The official national tongue, French, is celebrated for its melodic flow and widespread influence in international diplomacy. Gastronomy here focuses on seasonal ingredients, exquisite cheeses, and fine wines, maintaining traditional techniques like slow braising. The country is a founding member of the European Union and plays a key role in global aerospace engineering.",
# Страна 2 (Germany)
"Situated in Central Europe, the terrain spans from the sandy Baltic and North Sea coasts through rolling central uplands to the jagged peaks of the Alps. The primary tongue, German, is known for its complex grammar and its role as a major medium for classical philosophy. The culinary tradition emphasizes hearty portions of roasted meats, diverse bread varieties, and a world-renowned culture of beer brewing. As a leading industrial power, it is famous for automotive manufacturing and precision engineering within the Eurozone.",
# Страна 3 (Russia)
"The region encompasses the world's largest territory, stretching across the continents of Europe and Asia, including vast Siberian forests and the Ural Mountains. It is bounded by the Arctic Ocean to the north and the Pacific Ocean to the east. The primary Slavic language uses the Cyrillic alphabet, serving as a vital lingual bridge across Northern Asia. Local food features warming staples like beet soup, savory dumplings, and buckwheat porridge. The nation holds significant global reserves of natural gas and mineral resources.",
# Страна 4 (China)
"This massive territory in East Asia includes the arid Gobi Desert, fertile eastern river basins, and the high Himalayan plateau along its southern borders. It faces the Pacific Ocean to the east and south-east. The official speech utilizes a logographic writing system where thousands of intricate characters represent specific concepts. Cooking is defined by regional diversity, mastering flavors through techniques like stir-frying and steaming. With a history spanning millennia, it currently stands as a global leader in electronics and renewable energy production."
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
        
        raw_ner = generate_metadata(sentence)
        chunk_meta ={
            "page": page_number,
            "chunk_number": chunk_number,
            "global_index": len(final_chunks) - 1
        }
        chunk_meta.update(raw_ner)
        final_metadatas.append(chunk_meta)

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

    filter_input = input("\nВведите фильтр в формате 'Ключ:Значение' (например, Continents:Europe): ")
    where_condition= None

    if filter_input.strip():
        parts= filter_input.split(":")
        if len(parts) ==2:
            filter_key = parts[0].strip()
            filter_value = parts[1].strip()
            where_condition = {filter_key: {"$contains": filter_value}}

    user_query = input("\nТвой запрос (или 'exit'): ")
    
    if user_query.lower() in ['выход', 'exit', 'quit']:
        break

    results = collection.query(
        query_texts=[user_query],
        # n_results=len(sentence),
        n_results= 10,
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