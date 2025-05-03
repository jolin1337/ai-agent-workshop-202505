# AI Agent Workshop

Välkommen till **AI Agent Workshop**!

Under denna workshop kommer vi att bygga lokala AI-agenter som kan kommunicera, resonera och utföra uppgifter genom olika verktyg och moduler. Du kommer att få praktisk erfarenhet av hur man sätter upp agenter på sin egen maskin med hjälp av moderna LLMs och lokala verktyg.

---

## Syfte

- Förstå hur agentflöden fungerar
- Lära dig koppla agenter till externa verktyg (sökmotor, RAG, kodverktyg)
- Bygga multi-agent system som kan resonera och samarbeta
- Arbeta lokalt utan molntjänster

---

## Förberedelser innan workshop

1. **Följ installationsguiden** som bifogats i `SETUP.md` eller i PDF-form.
2. **Installera och starta Ollama** på din dator.
3. **Ladda ner modeller**:
   - `llama3:1b` eller `llama3:3b`
   - (Valfritt) `qwen2.5-coder:7b` för avancerad kodförståelse.

Notera att vi rekommenderar att du laddar ner modellerna i förväg på grund av begränsad nätverkskapacitet på plats.

---

## Innehåll

- Kort introduktion till agenter och agentarkitektur
- Genomgång av basflöde för multi-agent system
- Bygga en agent som använder:
  - Sökverktyg (DuckDuckGo via API)
  - RAG-modul för dokumenthämtning och validering
- Live-kodning och gemensamma övningar

---

## Teknikstack

- **Python 3.11+** (hanteras via `uv`)
- **Ollama** för lokala modeller
- **Open-webui** för tester av modell + RAG
- **AutoGen** för autonoma agenter
- **Crawl4AI** för skrapa bolagsverket
- **AutoRag** för att utvärdera parametrar för din RAG modell

---

## Kontakt

Vid frågor innan workshoppen:

- Kontaktperson: Johannes Lindén
- E-post: [johannes.linden@kvadrat.se]

Vi ses snart och ser fram emot att bygga tillsammans! 🚀
