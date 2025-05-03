# 🛠️ AI Agent Workshop – Snabbstartguide

Välkommen till **AI Agent Workshop**! Här sätter vi snabbt upp lokala AI-agenter utan molntjänster.

---

## ✅ Systemkrav

- **Processor**: Intel/AMD fyrkärnig eller Apple Silicon
- **RAM**: Minst 8–16 GB
- **Diskutrymme**: Minst 15 GB fritt

---

## ⚙️ Installera nödvändiga verktyg

### 1. Installera `uv` (Python-hanterare)

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

### 2. Klona workshop-repot

```bash
git clone https://github.com/jolin1337/ai-agent-workshop-202505.git
cd ai-agent-workshop-202505
```

### 3. Installera Python-beroenden

```bash
uv sync
cd ingest
uv sync
cd -
```

---

## 🧠 Installera och starta Ollama lokalt

### 1. Installera Ollama

- Ladda ner från: [https://ollama.com/download](https://ollama.com/download)

### 2. Starta Ollama

Starta Ollama via applikationen eller via terminal:

```bash
ollama serve
```

Alternativt kan du köra min docker compose fil (om du installerat docker på din maskin)

```
docker compose up -d ollama
```

Ollama körs nu i bakgrunden och är redo att ta emot förfrågningar.

---

## 📥 Förbered modeller i Ollama

Ladda ner modeller i förväg:

```bash
# Lättvikt – snabb och effektiv
ollama run llama3.2:1b

# Starkare modell (om din dator klarar det)
ollama run llama3.2:3b

# (Valfritt) Avancerad kodningsmodell
ollama run qwen2.5-coder:7b
```

> 💾 Modellerna är 3–7 GB styck. Se till att du laddar ner dem innan workshopen.

---

## ✅ Testa Ollama

```bash
ollama run llama3.2:1b
```

Om du får ett svar från modellen är allt redo!

---

Vi hjälper till på plats om något strular – men ju mer du förberett desto mer kan du fokusera på att bygga!
