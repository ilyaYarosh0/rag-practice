import chromadb

client = chromadb.HttpClient(host='localhost', port=8000)

try:
    client.delete_collection(name="world_info_full")
except Exception:
    pass

collection = client.create_collection(name="world_info_full", metadata={"hnsw:space": "cosine"})
splitted_text = "This territory features diverse landscapes ranging from the coastal plains in the north and west to the majestic Alpine mountain ranges. The official national tongue is celebrated for its melodic flow, distinct pronunciation, and widespread influence within the sphere of international diplomacy. Gastronomy here focuses on seasonal ingredients, exquisite cheeses, fine wines, and traditional techniques like slow braising or crafting delicate puff pastries. The terrain spans from the sandy Baltic and North Sea coasts through rolling central uplands to the jagged peaks of the Alps. The primary tongue is known for its complex grammar, compound words, and its role as a major medium for classical philosophy. The culinary tradition emphasizes hearty portions of roasted meats, diverse bread varieties, fermented cabbage, and a world-renowned culture of beer brewing. The region encompasses the world's largest territory, including vast Siberian forests, the Ural Mountains, and diverse climates stretching across two continents. The primary Slavic language uses the Cyrillic alphabet, serving as a vital lingual bridge across Northern Asia and parts of Eastern Europe. Local food features warming staples like beet soup, savory dumplings, buckwheat porridge, and preserved vegetables essential for surviving the long winters. The massive territory includes the arid Gobi Desert, fertile eastern river basins, and the high Himalayan plateau along its southern borders. The official speech utilizes a logographic writing system where thousands of intricate characters represent specific concepts rather than individual phonetic sounds. Cooking is defined by regional diversity, mastering the balance of flavors through techniques like stir-frying, steaming, and use of aromatic spices.".split(".") 
#dotted_text = ".".join(splitted_text)
splitted_text += [
        "This territory features diverse landscapes ranging from the coastal plains in the north and west to the majestic Alpine mountain ranges. The official national tongue is celebrated for its melodic flow, distinct pronunciation, and widespread influence within the sphere of international diplomacy. Gastronomy here focuses on seasonal ingredients, exquisite cheeses, fine wines, and traditional techniques like slow braising or crafting delicate puff pastries.",
        "The terrain spans from the sandy Baltic and North Sea coasts through rolling central uplands to the jagged peaks of the Alps. The primary tongue is known for its complex grammar, compound words, and its role as a major medium for classical philosophy. The culinary tradition emphasizes hearty portions of roasted meats, diverse bread varieties, fermented cabbage, and a world-renowned culture of beer brewing.",
        "The region encompasses the world's largest territory, including vast Siberian forests, the Ural Mountains, and diverse climates stretching across two continents. The primary Slavic language uses the Cyrillic alphabet, serving as a vital lingual bridge across Northern Asia and parts of Eastern Europe. Local food features warming staples like beet soup, savory dumplings, buckwheat porridge, and preserved vegetables essential for surviving the long winters.",
        "The massive territory includes the arid Gobi Desert, fertile eastern river basins, and the high Himalayan plateau along its southern borders. The official speech utilizes a logographic writing system where thousands of intricate characters represent specific concepts rather than individual phonetic sounds. Cooking is defined by regional diversity, mastering the balance of flavors through techniques like stir-frying, steaming, and use of aromatic spices."
    ]
print(f"lol: ({len(splitted_text)}")
for i in range(0,len(splitted_text)):
    print(f"#{i}: {splitted_text[i]}")
collection.add(
      documents= splitted_text, 
     
    # metadatas=[
    #     {"country": "France"}, 
    #     {"country": "Germany"},
    #     {"country": "Germany_geo"}, 
    #     {"country": "Germany_language"}, 
    #     {"country": "Germany_food"},  
    #     {"country": "Russian"},
    #     {"country": "China"},
    #     {"country": "Full_Dotted_text"}
    #     ],

    ids= [str(i) for i in range(len(splitted_text))]
    #["fr", "de", "de_geo", "de_language", "de_food", "rus", "chi", "full_txt"]
)

while True:
    user_query = input("\nТвой запрос (или 'exit'): ")
    
    if user_query.lower() in ['выход', 'exit', 'quit']:
        break

    results = collection.query(
        query_texts=[user_query],
        n_results=len(splitted_text), 
        include=["documents", "distances"] 
    )

    print("\n--- РЕЙТИНГ ВСЕХ СТРАН (Дистанция) ---")
    
    # ИЗМЕНЕНИЕ 2: Выводим циклом дистанцию до каждой страны
    for i in range(len(results['ids'][0])):
        chunk_id = results['ids'][0][i] 
        distance = results['distances'][0][i]
        
        print(f"{i+1}. Чанк №{chunk_id}: {distance:.4f}")
