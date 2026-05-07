import docx
from typing import Iterable, Generator

class DocxLoader:
    """The class is only responsible for reading the file and outputting paragraphs one at a time."""
    def lazy_loader(self, file_path:str):
        doc = docx.Document(file_path)

        for i, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            if not text:
                continue

            last_char = text[-1]
            if last_char in ".!?»\"":
                text += "\n"
            else:
                text += " "
            
            yield {
                "text": text,
                "paragraph_num": i+1
            }

class TextSplitter:
    """Cutting and gluing text into chunks."""

    def __init__(self, chunk_size: int= 500, overlap_pct: float = 0.2, separators: list[str] = None):
        self.chunk_size = chunk_size
        self.overlap_pct = overlap_pct
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def _split_to_atoms(self, text: str, current_separators: list[str]) -> list[str]:
        """Recursively splits a string into indivisible elements."""

        if len(text) <= self.chunk_size or not current_separators:
            return [text]
        
        sep = current_separators[0]
        if sep not in text:
            return self._split_to_atoms(text, current_separators[1:])
        
        parts = text.split(sep)
        atoms = []
        for p in parts:
            if len(p) > self.chunk_size:
                atoms.extend(self._split_to_atoms(p, current_separators[1:]))
            elif p.strip():
                atoms.append(p + sep)
        return atoms
    
    def chunk_stream(self, node_stream: Iterable[dict]):
        """Public method: accepts a stream of paragraphs, returns a stream of chunks."""
        current_chunk = ""
        current_start_para = None
        overlap_size = int(self.chunk_size * self.overlap_pct)
        for node in node_stream:
            text = node["text"]

            if current_start_para is None:
                current_start_para = node["paragraph_num"]
            
            atoms = self._split_to_atoms(text, self.separators)
            for atom in atoms:
                if len(current_chunk)+ len(atom) <= self.chunk_size:
                    current_chunk += atom
                else:
                    if current_chunk:
                        yield {
                            "chunk_text": current_chunk.strip(),
                            "start_paragraph": current_start_para
                        }
                    if overlap_size == 0:
                        overlap_text = ""
                    else:
                        raw_ov = current_chunk[-overlap_size:]
                        break_point = -1
                        for s in ["\n", " ", "."]:
                            pos = raw_ov.find(s)
                            if pos != -1 and (break_point == -1 or pos < break_point):
                                break_point = pos
                        overlap_text = raw_ov[break_point:].lstrip() if break_point != -1 else raw_ov
                    current_chunk = overlap_text + atom
                    current_start_para = node["paragraph_num"]
        if current_chunk:
            yield {
                "chunk_text": current_chunk.strip(),
                "start_paragraph": current_start_para
                        }






if __name__ == "__main__":
    # Этот блок выполнится только если запустить этот файл напрямую.
    # Здесь мы не трогаем БД и метаданные, просто смотрим как работает труба.

    test_file = r"Kursach.docx"  # Подставь свой файл

    # 1. Инициализируем наши независимые классы
    loader = DocxLoader()
    splitter = TextSplitter(chunk_size=500, overlap_pct=0.2, separators=["\n\n", "\n", ". ", " ", ""])

    # 2. Создаем потоки (данные еще не загружены в память!)
    paragraph_generator = loader.lazy_loader(test_file)
    chunk_generator = splitter.chunk_stream(paragraph_generator)

    # 3. Вытягиваем данные по одному чанку и печатаем для дебага
    print("Начинаем потоковую обработку...\n" + "-"*40)

    for i, chunk in enumerate(chunk_generator, 1):
        print(f"ЧАНК №{i} (Начат с абзаца: {chunk['start_paragraph']})")
        print(f"Длина: {len(chunk['chunk_text'])} символов")
        print(f"Текст:\n{chunk['chunk_text']}")
        print("-" * 40)