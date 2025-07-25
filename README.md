# voice-rag-assistant

🧠 Voice RAG Assistant (TR + EN)

Bir sesli AI asistanı:

Gerçek zamanlı konuşma tanıma (Türkçe ve İngilizce)

GPT ile sohbet hafızası

Wikipedia (RAG) bağlam enjeksiyonu

Halüsinasyon kontrolü

Dil değiştirme (TR/EN)

Hata yakalama ve günlükleme

=========================
PROJE YAPISI

voice-rag-assistant/

main.py # Ana uygulama (klasik döngü)

main_modular.py # LangGraph orchestrator girişi

runner.py # Alternatif LangGraph başlatıcı

README.txt # Bu dosya!

requirements.txt # Bağımlılıklar

logs/

assistant.log # Log dosyası

nodes/

gpt_node.py

rag_node.py

hallucination_node.py

transcribe_node.py

speak_node.py

command_node.py

langchain_rag_node.py # (ileri) LangChain RAG

a2a_orchestration.py # (ileri) Çoklu-agent orchestration

orchestration/

voice_graph.py # LangGraph orchestration

api.py # (ileri) FastAPI REST API

... # (Opsiyonel) testler, özel KB, vb.

=========================
KURULUM ve KULLANIM

Gereksinimleri kur:
pip install -r requirements.txt

OpenAI API anahtarını tanımla:
export OPENAI_API_KEY=your_openai_key_here

Klasik Modu Başlat:
python main.py

Asistan seni karşılar, seni dinler, yanıtlar ve döngüye girer.
Çıkmak için "çık", "quit" de veya Ctrl+C’ye bas.

İleri Kullanım:

LangGraph Modüler Akış:
python main_modular.py
veya
python runner.py

REST API (FastAPI):
uvicorn api:app --reload
Sonra POST ile http://localhost:8000/ask adresine istek gönderebilirsin.

LangChain RAG:
Kullanım örneği nodes/langchain_rag_node.py içinde.

Çoklu Agent (A2A) Orchestration:
Kullanım örneği nodes/a2a_orchestration.py içinde.

=========================
Kullanılabilir Komutlar

Türkçe Komut	İngilizce Komut	Açıklama
yardım	help	Komutları listele
çık / çıkış	quit / exit	Programdan çık
dili değiştir	switch language	TR/EN arasında geçiş
sıfırla	reset	Sohbet geçmişini temizle
İngilizceye geç	switch to English	İngilizceye geçiş yap
Türkçeye geç	switch to Turkish	Türkçeye geçiş yap 

=========================
ÖZELLİKLER

Tamamen sesli döngü

GPT ile sohbet geçmişi

Wikipedia bağlam enjeksiyonu (RAG)

Halüsinasyon önleme (bağlama göre kontrol)

Dinamik dil değişimi (TR/EN)

Hafıza sıfırlama

Loglar logs/ klasörüne kaydedilir

=========================
GEREKSİNİMLER

openai
speechrecognition
pyttsx3
gtts
playsound
wikipedia
langgraph
langchain
fastapi
uvicorn

(Mikrofon/ses hatası alırsan: pyaudio veya simpleaudio kur.)

=========================
TÜRKÇE KISA ÖZET

Python uygulaması, konuşmanı GPT ile cevaplar, Wikipedia bilgisiyle destekler ve halüsinasyonları önler.
TR ve EN destekler.
Ana dosya: main.py
LangGraph, LangChain ve REST API desteği de mevcut.

=========================
GELİŞMİŞ MİMARİLER (Advanced)

LangGraph Orchestration:
Her işlem (dinle, komut, rag, gpt, kontrol, seslendir) bir node’dur.
Akış:
[Transcribe] → [Command?] → [RAG] → [GPT] → [Hallucination] → [Speak] → ↩
orchestration/voice_graph.py ve nodes/ dosyalarında yönetilir.

LangChain Hybrid RAG (Retriever + LLM):
nodes/langchain_rag_node.py
LangChain retriever (Wikipedia, özel DB) ile gelişmiş RAG.

FastAPI REST API:
uvicorn api:app --reload
/ask endpoint’i ile web/mobil uygulama entegrasyonu.

Çoklu Agent (A2A) Orchestration:
nodes/a2a_orchestration.py (ör: FactAgent + ChatAgent)
Çoklu agent ile kurumsal AI workflow’a altyapı.

Hibrit Akış: LangGraph + LangChain:
LangChain node’ları LangGraph içinde tanımlayabilirsin.
Örnek:
from nodes.langchain_rag_node import LangChainRAGNode

=========================
YAKINDA / FİKİRLER

WebSocket, Streamlit, React tabanlı canlı UI

Whisper veya daha iyi sesli yazıya çeviri

Özel bilgi tabanı (FAISS, PDF vs.)

HuggingFace LLM fallback / offline mod

Gerçek zamanlı halüsinasyon skoru/görselleştirme

Çoklu agent (A2A, MCP) mimariler

LangGraph + LangChain hibrit orchestrasyon

Daha fazla dil desteği!

=========================
PROJE AKIŞI (ŞEMA/AKIŞ)

TranscribeNode -> CommandNode -> (Komut değilse) -> RAGNode -> GPTNode -> HallucinationNode -> SpeakNode -> başa dön
(Çıkış komutuysa -> END)

=========================
Katkı ve İletişim

Issues ve pull request’ler açıktır.

Gelişmiş entegrasyon için kodlara bak veya iletişime geç.

Özel kurumsal akış, konnektör veya yeni agent? Temasa geç!

=========================
© 2024
MIT Lisansı ile dağıtılır.

