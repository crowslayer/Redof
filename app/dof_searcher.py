# pdf_searcher.py
import os
import pathlib
import fitz

class DofSearcher:
    def __init__(self, term, search_path, match_type='contains'):
        self.term = term.lower()
        self.search_path = search_path
        self.match_type = match_type
        self.results = []

    def search(self):
        for root, _, files in os.walk(self.search_path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    file_path = pathlib.Path(root) / file
                    try:
                        with fitz.open(file_path) as doc:
                            pub_info = self.get_num_dof(doc.load_page(0).get_text())
                            for page_num, page in enumerate(doc, start=1):
                                blocks = page.get_text("blocks")
                                for b in blocks:
                                    paragraph = b[4].strip()
                                    lower_paragraph = paragraph.lower()

                                    if self.match(lower_paragraph):
                                        self.results.append({
                                            'name': file_path.stem,
                                            'path': str(file_path.absolute()),
                                            'page': page_num,
                                            'paragraph': paragraph,
                                            'num': pub_info.get("num_dof", ""),
                                            'date': pub_info.get("date_pub", "")
                                        })
                    except Exception as e:
                        print(f"⚠️ Error leyendo PDF {file_path}: {e}")

        return self.results

    def match(self, text):
        return (
            (self.match_type == 'contains' and self.term in text) or
            (self.match_type == 'startswith' and text.startswith(self.term)) or
            (self.match_type == 'endswith' and text.endswith(self.term))
        )

    def get_num_dof(self, page):
        lines = page.replace('�', '').split('\n')
        return {
            "date_pub": lines[0] if len(lines) > 0 else "",
            "num_dof": lines[2] if len(lines) > 2 else ""
        }
