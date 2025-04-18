import os
import openai
import difflib
from PyPDF2 import PdfReader


class SimplePDFChatBot:
    def __init__(self, api_key, pdf_path):
        self.api_key = api_key
        self.pdf_path = pdf_path
        self.chunks = []
        self._prepare_chunks()

    def _prepare_chunks(self):
        if not os.path.exists(self.pdf_path):
            print(f"❌ File not found at: {self.pdf_path}")
            raise FileNotFoundError("PDF not found.")
        
        reader = PdfReader("/Users/gulkapoor/Downloads/python_handbook.pdf")  
        raw_text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content: 
                raw_text += content

        # Basic manual chunking by paragraphs
        self.chunks = raw_text.split("\n\n") 

    def _find_most_relevant_chunk(self, question):
        # Uses difflib for basic fuzzy matching (not embeddings)
        scored_chunks = sorted(
            self.chunks,
            key=lambda c: difflib.SequenceMatcher(None, c.lower(), question.lower()).ratio(),
            reverse=True
        )
        return scored_chunks[:2]  # top 2 relevant chunks

    def ask(self, question):
        relevant_chunks = self._find_most_relevant_chunk(question)
        context = "\n".join(relevant_chunks)
        prompt = f"Answer the question based on this context:\n{context}\n\nQuestion: {question}\nAnswer:"

        try:
            openai.api_key = self.api_key  #  API key here
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[OpenAI Error] {str(e)}"


if __name__ == "__main__":
    import getpass

    print("== Simple PDF Chatbot ==")
    api_key = getpass.getpass("Enter your OpenAI API Key: ").strip()
    pdf_path = input("Enter PDF path: ").strip().strip('"')

    bot = SimplePDFChatBot(api_key, pdf_path)
    print("\nStart chatting! Type 'exit' to quit.\n")

    while True:
        q = input("You: ")
        if q.lower() in {"exit", "quit"}:
            print("Bye!")
            break
        answer = bot.ask(q)
        print("Bot:", answer, "\n")


