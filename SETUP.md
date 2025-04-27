Självklart! Här kommer den **översatta svenska versionen** av installationsguiden för din workshop:

---

## 🛠️ AI Agent Workshop – Installationsguide (lokal uppsättning)

Välkommen till **AI Agent Workshop**! Under workshopen kommer du att bygga lokala, integritetsvänliga AI-agenter med hjälp av öppna verktyg och modeller – helt utan moln.

Förbered din dator i förväg enligt stegen nedan så att du är redo att komma igång direkt. Vi kommer gå igenom dessa steg på plats men med tanke på att vi är många och vill undvika hög belastning av nätverk behöver vi ladda ner modellerna innan).

---

### TLDR

Jag har förberett två skript som sätter upp allt man behöver för denna workshopen, har man förinstallerat docker kommer dessa installeras i docker. annars lokalt på sin dator. Först ladda ner repot: [https://github.com/jolin1337/ai-agent-workshop-202505.git]() lokalt på din dator där du vill utföra experimentet.

```bash
# Windows
> ./setup.windows.sh
# Linux
> ./setup.linux.sh
```

När workshopen är klar eller man vill ta bort allt kan man köra följande skript.

```bash
# Windows
> ./cleanup.windows.sh
# Linux
> ./cleanup.linux.sh
```

Nedan följer mer detaljerade instruktioner om man vill förstå vad skripten gör.

### ✅ Systemkrav

#### 💻 Rekommenderad utrustning

- **Processor**: Fyrkärnig Intel/AMD eller Apple Silicon (M1/M2/M3)
- **RAM**: Minst 16 GB (8 GB fungerar med lättare modeller)
- **Diskutrymme**: Minst 15–20 GB ledigt
- **GPU**: Valfritt (NVIDIA kan ge bättre prestanda, men är inte nödvändigt)

---

### ⚙️ Nödvändig programvara

#### 1. Docker (är det vi kommer använda för Ollama & ev. openwebui dessa verktyg går även att installera via deras hemsidor separat istället och då behöver ni inte docker heller)

- Ladda ner och installera från: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- Starta Docker och se till att det körs i bakgrunden

---

### 📦 Python-miljö med `uv`

Vi använder [`uv`](https://github.com/astral-sh/uv) – en snabbare och mer modern Python-hanterare än `pip`.

#### 1. Installera `uv`

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

#### 2. Klona workshopens GitHub-repo om detta inte redan gjorts

```bash
git clone https://github.com/jolin1337/ai-agent-workshop-202505.git
cd ai-agent-workshop-202505
```

#### 3. Installera beroenden

```bash
uv sync
uv install
```

**4. Ollama tjänsten**

- Pulla ner docker instansen eller installera direct från: [https://ollama.com/download](https://ollama.com/download)
- Kort kommandot för att installera ollama är: `curl -fsSL https://ollama.com/install.sh | sh`
- Verifiera installationen (se längre ner i instruktionerna)

```
docker compose pull ollama
```

**2. Open Webui (enbart introduktion/första delen av workshopen)**

- Pulla ner docker instansen eller installera direct från: [https://docs.openwebui.com/#manual-installation](https://docs.openwebui.com/#manual-installation)
- Verifiera installationen (se längre ner i instruktionerna)

```
docker compose pull open-webui
```

### 🧠 Ladda ner modeller i förväg (viktigaste steget innan workshopen)

Kör följande kommandon i terminalen för att ladda ner modellerna (lägg till en prefix `docker compose run --rm ollama` för varje kommando nedan om ni installerat via docker):

```
# Lätt modell – snabb och stabil
ollama run llama3.2:1b

# Lite kraftigare modell – om din dator klarar det
ollama run llama3.2:3b

# (Valfritt) Kodspecialiserad modell – större och vassare
ollama run qwen2.5-coder:7b
```

💾 Varje modell är cirka 3–7 GB. Se till att du laddar ner dem i god tid över ett stabilt nätverk.

---

### ✅ Testa att allt fungerar

Kör följande kommando för ollama:

```bash
docker compose up –d ollama
# eller utan docker
ollama serve

curl http://localhost:11434/api/tags
```

Kör följande kommando för open webui:

```bash
docker compose up –d open-webui
```

Om du får ett svar från curl kommandot med en lista av de modellerna du angivit ovan är du redo med ollama! Kommer du till en inloggningsida när du går in på [http://localhost:8080](http://localhost:8080/) i din webläsare på samma dator är du redo med open webui!

---

### 🛟 Behöver du hjälp?

Vi har en kort teknisk uppstartsstund i början av workshopen. Men ju mer du förberett innan, desto mer hinner du bygga under sessionen.
