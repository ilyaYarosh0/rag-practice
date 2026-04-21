import chromadb
from ner import generate_metadata
import re

client = chromadb.HttpClient(host='localhost', port=8000)

try:
    client.delete_collection(name="world_info_full")
except Exception:
    pass

collection = client.create_collection(name="world_info_full", metadata={"hnsw:space": "cosine"})

splitted_text = [
# Страна 1 (France)
"This territory is located in Western Europe and features diverse landscapes ranging from the coastal plains in the north to the majestic Alpine mountain ranges. It borders the Atlantic Ocean to the west and the Mediterranean Sea to the south. The official national tongue, French, is celebrated for its melodic flow and widespread influence in international diplomacy. Gastronomy here focuses on seasonal ingredients, exquisite cheeses, and fine wines, maintaining traditional techniques like slow braising. The country is a founding member of the European Union and plays a key role in global aerospace engineering. [France]",
# Страна 2 (Germany)
"Situated in Central Europe, the terrain spans from the sandy Baltic and North Sea coasts through rolling central uplands to the jagged peaks of the Alps. The primary tongue, German, is known for its complex grammar and its role as a major medium for classical philosophy. The culinary tradition emphasizes hearty portions of roasted meats, diverse bread varieties, and a world-renowned culture of beer brewing. As a leading industrial power, it is famous for automotive manufacturing and precision engineering within the Eurozone. [Germany]",
# Страна 3 (Russia)
"The region encompasses the world's largest territory, stretching across the continents of Europe and Asia, including vast Siberian forests and the Ural Mountains. It is bounded by the Arctic Ocean to the north and the Pacific Ocean to the east. The primary Slavic language uses the Cyrillic alphabet, serving as a vital lingual bridge across Northern Asia. Local food features warming staples like beet soup, savory dumplings, and buckwheat porridge. The nation holds significant global reserves of natural gas and mineral resources. [Russia]",
# Страна 4 (China)
"This massive territory in East Asia includes the arid Gobi Desert, fertile eastern river basins, and the high Himalayan plateau along its southern borders. It faces the Pacific Ocean to the east and south-east. The official speech utilizes a logographic writing system where thousands of intricate characters represent specific concepts. Cooking is defined by regional diversity, mastering flavors through techniques like stir-frying and steaming. With a history spanning millennia, it currently stands as a global leader in electronics and renewable energy production. [China]",
# Страна 5 (Spain)
"Located on the Iberian Peninsula in Southwestern Europe, the landscape ranges from the high plateaus of the Meseta Central to the sunny Mediterranean coasts. It is bordered by the Atlantic Ocean to the west and the Mediterranean Sea to the east and south. The primary tongue, Spanish, is a global Romance language celebrated for its phonetic rhythm and vast literature. The culinary tradition highlights vibrant flavors with dishes like paella, cured meats, and an array of tapas. The nation is a major global tourism destination and a leading producer of renewable energy, particularly wind and solar. [Spain]",
# Страна 6 (Belgium)
"Situated in Western Europe, the terrain consists of flat coastal plains in the northwest, rolling hills in the center, and the rugged Ardennes forest in the southeast. It borders the North Sea to the northwest. The region is distinctly multilingual, with Dutch, French, and German serving as official tongues reflecting its cultural crossroads. Gastronomy here is world-renowned for its artisanal chocolates, double-fried frites, and a vast, complex beer culture. The nation serves as the de facto capital of the European Union, hosting major international political institutions. [Belgium]",
# Страна 7 (Switzerland)
"This landlocked territory in Central Europe is famous for its dramatic Alpine peaks, crystal-clear glacial lakes, and rolling central plateau. It shares borders with major European neighbors but maintains no direct access to the sea. The country recognizes four official languages—German, French, Italian, and Romansh—creating a highly diverse linguistic landscape. Local food features rich, dairy-heavy staples like cheese fondue, raclette, and premium milk chocolate. Historically committed to political neutrality, it is a global hub for private banking, diplomacy, and pharmaceutical innovation. [Switzerland]",
# Страна 8 (Italy)
"Located in Southern Europe, this boot-shaped peninsula features the towering Alps in the north and the rugged Apennine mountains running down its center. It is surrounded by the Mediterranean, Tyrrhenian, Ionian, and Adriatic seas. The official language, Italian, is a melodic Romance tongue deeply intertwined with the history of classical music and Renaissance art. Cooking is celebrated globally for its regional diversity, emphasizing high-quality olive oil, fresh pastas, and wood-fired pizzas. The country boasts the highest number of UNESCO World Heritage sites and is a leader in luxury fashion and automotive design. [Italy]",
# Страна 9 (Luxembourg)
"This small landlocked territory in Western Europe features dense forests and rolling hills in the north, giving way to the fertile valleys of the Gutland region in the south. It is completely surrounded by its larger European neighbors. The population is heavily trilingual, seamlessly switching between Luxembourgish, French, and German in daily life. Gastronomy reflects a blend of hearty Germanic portions and refined French techniques, featuring dishes like smoked pork collar with broad beans. Despite its size, the nation holds one of the world's highest GDPs per capita and is a premier global financial center. [Luxembourg]",
# Страна 10 (Netherlands)
"Positioned in Western Europe, the geography is uniquely flat, with a significant portion of its land meticulously reclaimed from the sea and protected by complex dykes. It borders the North Sea to the west and north. The primary language, Dutch, is a West Germanic tongue known for its distinctive guttural sounds and straightforward grammar. The culinary tradition focuses on hearty dairy products, particularly Gouda and Edam cheeses, alongside cured fish and sweet stroopwafels. The nation is an agricultural powerhouse, standing as the world's second-largest exporter of food despite its small size, and is highly advanced in water management. [Netherlands]",
# Страна 11 (Denmark)
"This Nordic territory consists of the Jutland peninsula and an archipelago of over 400 islands, featuring flat, arable land and sandy coastlines. It serves as a bridge between Central Europe and the Scandinavian Peninsula, bounded by the Baltic and North Seas. The official tongue, Danish, is a North Germanic language characterized by its soft pronunciation and unique vowels. Local food emphasizes open-faced rye bread sandwiches, pickled herring, and high-quality pork products. The country is recognized globally for its high standard of living, minimalist design, and pioneering wind turbine industry. [Denmark]",
# Страна 12 (Poland)
"Situated in Central Europe, the landscape transitions from the sandy beaches of the Baltic coast in the north to the rugged Tatra Mountains in the south. It faces the Baltic Sea to the north. The primary language is Polish, a West Slavic tongue famous for its complex consonant clusters and rich literary heritage. Gastronomy features hearty, comforting dishes such as pierogi dumplings, smoked sausages, and rich hunter's stews. With a rapidly growing economy, it serves as a crucial manufacturing and technology hub within the European Union. [Poland]",
# Страна 13 (Czechia)
"This landlocked nation in Central Europe is characterized by a basin of rolling hills surrounded by low mountains, including the Krkonoše range. It is bordered by its European neighbors on all sides and has no ocean coastline. The official language, Czech, is a West Slavic tongue noted for its unique consonant sounds and historical ties to the Bohemian kingdom. The culinary tradition revolves around rich gravies, roasted pork, bread dumplings, and the birthplace of Pilsner-style beer. It has a strong industrial heritage, particularly in automotive manufacturing and precision machinery. [Czechia]",
# Страна 14 (Austria)
"Located in the heart of Central Europe, the terrain is highly mountainous, dominated by the Eastern Alps, giving way to the Danube river basin in the northeast. This landlocked country shares its borders with eight European nations. The primary tongue, a distinct variety of standard German, is the medium for a rich history of classical music and psychoanalysis. Local food highlights refined pastries, breaded veal cutlets, and a sophisticated coffee house culture. The nation is a prosperous social market economy, known for its high quality of life and specialized engineering sectors. [Austria]",
# Страна 15 (Norway)
"This elongated territory on the Scandinavian Peninsula features a rugged, mountainous interior and a deeply indented coastline carved by spectacular fjords. It borders the North Atlantic Ocean and the Barents Sea, extending well above the Arctic Circle. The official language, Norwegian, has two distinct written forms and is mutually intelligible with its Scandinavian neighbors. Cooking relies heavily on maritime bounty, featuring salmon, cured cod, and traditional flatbreads. The country is a global leader in sustainable energy, powered almost entirely by hydroelectricity, while managing vast sovereign wealth from offshore oil. [Norway]",
# Страна 16 (Finland)
"Situated in Northern Europe, the landscape is heavily forested and dotted with tens of thousands of lakes, shaped extensively by Ice Age glaciers. It faces the Gulf of Bothnia to the west and the Gulf of Finland to the south. The primary language, Finnish, belongs to the Finno-Ugric family, making it completely distinct from most other European tongues. The culinary tradition focuses on foraging and hunting, highlighting reindeer meat, wild berries, and hearty rye breads. The nation is renowned for its high-quality education system, advanced telecommunications, and sauna culture. [Finland]",
# Страна 17 (Estonia)
"This northernmost Baltic state features a low-lying, flat terrain covered by dense forests, wetlands, and over two thousand islands along its coast. It is bounded by the Baltic Sea to the west and the Gulf of Finland to the north. The official tongue, Estonian, is a Finno-Ugric language closely related to Finnish, known for its complex vowel system. Local food is simple and seasonal, focusing on black bread, pork, root vegetables, and dairy. The country is a global pioneer in digital governance, boasting a highly advanced e-society and a booming tech startup ecosystem. [Estonia]",
# Страна 18 (Latvia)
"Located in Northern Europe on the eastern shores of the Baltic Sea, the geography is primarily composed of fertile, low-lying plains and expansive, ancient forests. It features a long coastline along the Baltic Sea and the Gulf of Riga. The primary language, Latvian, is one of only two surviving Baltic languages, retaining many archaic features of early Indo-European speech. Gastronomy emphasizes earthy flavors, featuring dishes made from grey peas, smoked fish, and wild mushrooms. The nation serves as a significant transit and logistics hub in the Baltic region, heavily investing in green technology. [Latvia]",
# Страна 19 (Lithuania)
"This southernmost Baltic state is characterized by a landscape of gently rolling hills, numerous small lakes, and a short but distinct sandy coastline. It borders the Baltic Sea to the west. The official tongue, Lithuanian, is the most conservative living Indo-European language, highly valued by linguists for its ancient grammatical structures. The culinary tradition is famously potato-centric, highlighted by the stuffed potato dumplings known as cepelinai, alongside cold beet soup. The country has a rapidly growing economy with strong sectors in biotechnology and laser manufacturing. [Lithuania]",
# Страна 20 (Belarus)
"This landlocked territory in Eastern Europe is predominantly flat, featuring extensive marshlands, primeval forests, and thousands of lakes and rivers. It is surrounded entirely by its European and Eurasian neighbors. The nation is officially bilingual, utilizing both Belarusian and Russian, which share Cyrillic roots but maintain distinct cultural identities. Local food is heavily reliant on the potato, offering dishes like draniki potato pancakes, accompanied by pork and thick sour cream. The economy is largely state-controlled, focusing on heavy machinery, tractor manufacturing, and agricultural exports. [Belarus]",
# Страна 21 (Ukraine)
"Located in Eastern Europe, the terrain consists mostly of fertile plains and steppes, with the Carpathian Mountains rising in the extreme west. It boasts a significant southern coastline along the Black Sea and the Sea of Azov. The primary language, Ukrainian, is an East Slavic tongue written in the Cyrillic alphabet, celebrated for its melodic and lyrical qualities. Cooking centers around the iconic borsch, accompanied by garlic rolls, stuffed cabbage leaves, and a variety of dumplings. Traditionally known as the breadbasket of Europe, it is a major global exporter of grain and sunflower oil. [Ukraine]",
# Страна 22 (Kazakhstan)
"This massive transcontinental territory in Central Asia and Eastern Europe features a diverse landscape of vast steppes, arid deserts, and towering snow-capped mountains in the southeast. It is the world's largest landlocked country, though it borders the inland Caspian Sea to the west. The official languages include Kazakh, a Turkic tongue, alongside Russian, serving as an important bridge across the Eurasian steppe. Gastronomy is rooted in nomadic traditions, featuring boiled mutton, horse meat sausages, and fermented mare's milk. The nation possesses vast natural wealth, particularly in uranium, oil, and mineral resources. [Kazakhstan]",
# Страна 23 (Mongolia)
"Situated in East Asia, this landlocked expanse is defined by the vast, arid Gobi Desert in the south and sweeping, high-altitude grassy steppes to the north. It is entirely wedged between two massive neighbors and has no access to the ocean. The primary language, Mongolian, utilizes a Cyrillic script and reflects a deep, enduring nomadic cultural heritage. The culinary tradition is protein-heavy to endure harsh winters, focusing almost exclusively on mutton, dairy products, and traditional meat-filled dumplings. The economy relies heavily on herding and the extensive mining of copper, coal, and gold. [Mongolia]",
# Страна 24 (North Korea)
"This territory occupies the northern half of the Korean Peninsula in East Asia, featuring a landscape dominated by rugged, forested mountains and deep, narrow valleys. It is bounded by the Korea Bay and the Yellow Sea to the west, and the Sea of Japan to the east. The official tongue, Korean, uses the Chosŏn'gŭl alphabet, prioritizing linguistic purity by avoiding foreign loan words. Local food features spicy fermented vegetables like kimchi, cold buckwheat noodles, and rice as a dietary staple. Operating under a highly centralized, isolationist planned economy, it focuses heavily on military development and heavy industry. [North Korea]",
# Страна 25 (Vietnam)
"Located in Southeast Asia, the geography is defined by a long, S-shaped coastline, lush river deltas in the north and south, and central forested highlands. It faces the South China Sea to the east and south. The primary language, Vietnamese, is a tonal Austroasiatic tongue that uses a Latin-based alphabet heavily modified with diacritics. The culinary tradition is globally revered for its fresh herbs, delicate balance of salty, sweet, sour, and spicy flavors, and iconic noodle soups. The nation has emerged as one of the fastest-growing economies in Asia, excelling in electronics manufacturing and textile exports. [Vietnam]",
# Страна 26 (Laos)
"This landlocked territory in Southeast Asia is heavily mountainous and thickly forested, bisected by the vital Mekong River. It shares borders with five neighboring countries but lacks any coastal access. The official language, Lao, is a tonal Kra-Dai tongue closely related to Thai, utilizing its own distinct script. Gastronomy revolves around sticky rice, pungent fermented fish sauces, and spicy green papaya salads. The nation is investing heavily in hydroelectric dams along its rivers, aiming to become the primary energy exporter of the region. [Laos]",
# Страна 27 (Myanmar)
"Located in Southeast Asia, the landscape ranges from northern mountainous regions to dense central jungles and the fertile Irrawaddy River delta. It boasts a long western coastline along the Andaman Sea and the Bay of Bengal. The official tongue, Burmese, is a Sino-Tibetan language written in a distinct, circular script developed from ancient Brahmic writing. Local food features robust curries, fermented tea leaf salads, and heavily incorporates fish paste and rice. The country is resource-rich, holding significant reserves of jade, natural gas, and precious teak timber. [Myanmar]",
# Страна 28 (India)
"This vast subcontinent in South Asia features the towering Himalayas in the north, the arid Thar Desert in the west, and fertile plains fed by major rivers. It is surrounded by the Indian Ocean on the south, the Arabian Sea on the west, and the Bay of Bengal on the east. The nation is exceptionally linguistically diverse, with Hindi and English serving as the primary official languages among dozens of recognized regional tongues. Cooking is incredibly diverse, mastering the use of complex spice blends in rich curries, flatbreads, and extensive vegetarian traditions. It is the world's most populous democracy and a major global powerhouse in information technology and pharmaceuticals. [India]",
# Страна 29 (Nepal)
"Situated in South Asia, this landlocked nation is defined by its dramatic elevation changes, culminating in the highest peaks of the Himalayas, including Mount Everest. It is wedged tightly between two massive Asian neighbors. The primary language, Nepali, is an Indo-Aryan tongue written in the Devanagari script, uniting dozens of distinct ethnic groups. The culinary tradition focuses on hearty, nourishing staples like dal bhat (lentil soup and rice) and savory momo dumplings. The economy is heavily reliant on international tourism, mountaineering expeditions, and foreign remittances. [Nepal]",
# Страна 30 (Bhutan)
"This small, landlocked territory in South Asia sits high in the eastern Himalayas, characterized by steep mountains and deep valleys. It is buffered entirely between its massive northern and southern neighbors. The official language, Dzongkha, is a Sino-Tibetan tongue related to Tibetan, reflecting the region's deep Buddhist heritage. The culinary tradition is famously spicy, with chili peppers treated as a main vegetable rather than a seasoning, especially in the national dish of ema datshi. The nation is globally unique for prioritizing Gross National Happiness over gross domestic product and maintaining a carbon-negative footprint. [Bhutan]",
# Страна 31 (Pakistan)
"Located in South Asia, the terrain spans from the coastal mangroves of the south to the towering, glaciated peaks of the Karakoram range in the north. It faces the Arabian Sea to the south. The official languages are Urdu and English, serving as unifying tongues across a highly diverse landscape of regional ethnicities. Cooking features rich, heavily spiced meat curries, tandoori-baked flatbreads, and aromatic biryanis. The country is a major geopolitical player in the region, possessing nuclear capabilities and a massive textile export industry. [Pakistan]",
# Страна 32 (Kyrgyzstan)
"Situated in Central Asia, the landscape is almost entirely mountainous, defined by the breathtaking peaks and high-altitude lakes of the Tian Shan range. It is completely landlocked, surrounded by vast Eurasian neighbors. The official tongues include Kyrgyz, a Turkic language, alongside Russian, preserving the legacy of nomadic storytelling and epics. The culinary tradition is meat-centric, featuring beshbarmak (boiled meat and noodles), fermented mare's milk, and savory fried dough. The nation is known for its vibrant nomadic traditions and is increasingly developing its eco-tourism sector. [Kyrgyzstan]"
]

final_chunks = []
final_metadatas = []
final_ids = []

for i, text in enumerate(splitted_text):
    #Find country name
    match = "Unknown"
    match = re.search(r"\[(.*?)\]$", text)
    if match:
        country = match.group(1)
    clean_text = re.sub(r"\[(.*?)\]", "", text).strip()

    sentences = [s.strip() for s in clean_text.split('.') if s.strip()]
    
    page_number = i + 1 
    
    for j, sentence in enumerate(sentences):
        final_chunks.append(sentence + ".")
        
        chunk_number = j + 1 
        
        raw_ner = generate_metadata(sentence)
        chunk_meta ={
            "country": [country],
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

    # filter_input = input("\nВведите номер чанка для фильтрации или нажмите Enter чтобы пропустить: ")
    # where_condition = None

    # if filter_input.strip():
    #     try:
    #         chunk_num = int(filter_input.strip())
    #         where_condition = {"chunk_number": chunk_num}
    #     except ValueError:
    #         print("Ошибка: введено не число. Поиск будет выполнен по всем чанкам")
    #         where_condition = None

    raw_input = input("\nВведите фильтр в формате 'Ключ:Значение, Ключ:Значение' (например, Continents:Europe): ")
    where_condition= None
    condition_query_list= []
    if raw_input.strip():
        splitted_input = raw_input.split(",")
        for filter_input in splitted_input: 
            parts= filter_input.split(":")
            if len(parts) ==2:
                filter_key = parts[0].strip()
                filter_value = parts[1].strip()
                condition_query_list.append({filter_key: {"$contains": filter_value}})
        if len(condition_query_list) == 1:
            where_condition = condition_query_list[0]
        elif len(condition_query_list) > 1:
            where_condition = {"$and": condition_query_list}

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
        
        chunk_val = metadata.get('chunk_number', 'N/A')
        country = metadata.get("country", "N/A")
        
        print(f"{i+1}. ID: {chunk_id} | Мета: [Имя страны {country}, Чанк {chunk_val}] | Дистанция: {distance:.4f}")