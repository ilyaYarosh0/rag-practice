DEFAULT_DICTIONARY = {
    "Continents": ["Europe", "Asia", "Western Europe", "Central Europe", "East Asia", "Northern Asia"],
    "Water bodies": ["Atlantic Ocean", "Pacific Ocean", "Arctic Ocean", "Mediterranean Sea", "Baltic Sea", "North Sea"],
    "Geography": ["Alps", "Himalayan", "Ural Mountains", "Siberian", "Gobi Desert"]
}

# for i, text in enumerate(splitted_text):
#     sentences = [s.strip() for s in text.split('.') if s.strip()]
#     chunk_meta = {}
#     metadata.append(chunk_meta)
#     lower_text = text.lower()

#     for key, value in ner.items():
#         for word in value:
#             lower_word = word.lower()
#             if lower_word in lower_text:
#                 chunk_meta.setdefault(key, []).append(word)

def generate_metadata(text, ner_dict=DEFAULT_DICTIONARY):
    chunk_meta = {}
    lower_text = text.lower()

    for key, value in ner_dict.items():
        for word in value:
            lower_word = word.lower()
            if lower_word in lower_text:
                chunk_meta.setdefault(key, []).append(word)
    return chunk_meta