# 🌍 Autonomous Travel & Packing Concierge Agent (Week 6)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Google Gemini API](https://img.shields.io/badge/Gemini-Function%20Calling-orange.svg)](https://ai.google.dev/)
[![Open-Meteo](https://img.shields.io/badge/Weather-Open--Meteo%20API-green.svg)](https://open-meteo.com/)
[![Wikipedia Knowledge](https://img.shields.io/badge/Activities-Wikipedia%20API-lightgrey.svg)](https://www.wikipedia.org/)

An autonomous, multi-tool **ReAct (Reasoning + Acting) Agent** built for the AWS AI/ML Mentorship Program. 

This repository provides the project in **three flexible formats**:
1. **Interactive Jupyter Notebook (`Week_06_Build_AI_Agent.ipynb`)**: For Google Colab submission and step-by-step interactive testing.
2. **Standalone Python Script (`week_06_build_ai_agent.py`)**: A self-contained, single-file script containing the entire agent pipeline.
3. **Modular CLI Architecture (`main.py` + `src/`)**: A clean production layout separating tools, prompt schemas, and the agent loop.

---

## 🌟 Key Highlights & Engineering Features

- **Dynamic Autonomous Planning (ReAct)**: Implements an explicit `Thought -> Action -> Observation -> Final Output` decision loop governed by `MAX_STEPS = 6` to avoid runaway execution.
- **Zero Hardcoding (Global Coverage)**:
  - **Live Geocoding**: Uses the Open-Meteo Geocoding API to dynamically resolve coordinates (latitude/longitude), country, and region for *any* place on Earth.
  - **Real-Time Forecasts**: Queries live temperatures, precipitation probabilities, and climate conditions up to 14 days without API keys.
  - **Live Sights & Activities**: Queries Wikipedia Knowledge Search API to extract real attractions, relaxation spots, nature reserves, and wellness centers.
- **Multi-Goal Reasoning**: Intelligently balances multi-phase trips (e.g., 2 weeks of corporate meetings + 3 days of tropical leisure & spa refreshment).
- **Strict User-Intent Adherence**: Only activates tools explicitly required by the user's prompt (e.g., skips tourist activities if the user only requests packing gear).
- **Security & Safety Guardrails**:
  - Parameter clamping on trip durations ($1 \le \text{days} \le 14$).
  - Path traversal protection on file exports (`os.path.basename`) to prevent malicious directory escaping.
- **Zero-Dependency Networking**: Built with standard library `urllib.request`—100% portable across Windows, Linux, macOS, and Google Colab with zero C++ compilation hurdles.

---

## 📂 Project Structure

```text
Week-6 Build AI Agent/
├── .env.example                 # Template for environment configuration
├── .gitignore                   # Protects secrets (.env) and Python cache
├── requirements.txt             # Project dependencies (pydantic, python-dotenv)
├── Week_06_Build_AI_Agent.ipynb # Google Colab & Jupyter Notebook
├── week_06_build_ai_agent.py    # Self-contained, single-file agent script
├── main.py                      # Modular CLI entry point (interactive & argument support)
├── src/
│   ├── __init__.py              # Package marker
│   ├── tools.py                 # Geocoding, Open-Meteo weather, Wikipedia search, & file writer
│   ├── prompts.py               # OpenAPI tool function declarations & system instructions
│   └── agent.py                 # ReAct loop, tool dispatcher, error handler & model fallback
└── README.md                    # Complete project documentation
```

*(Note: `.env` is kept private and hidden by `.gitignore` to prevent API key leakage.)*

---

## 🛠️ The Agent's Toolbox

| Tool | Source / API | Purpose | Parameter Guardrails |
| :--- | :--- | :--- | :--- |
| `get_weather_forecast` | Open-Meteo REST API | Resolves coordinates dynamically & fetches temperature highs/lows + rain probabilities. | Clamped between 1 and 14 days. |
| `get_city_activities` | Wikipedia Knowledge Search | Finds real attractions, spas, parks, and cultural sights by theme. | Clamped between 1 and 7 days. |
| `save_travel_plan` | Local Filesystem | Exports comprehensive, formatted Markdown documents to `outputs/`. | Path traversal neutralization (`os.path.basename`). |

---

## ⚡ How to Run

### Method 1: Interactive CLI (Modular App)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your API key:**
   ```bash
   cp .env.example .env
   ```
   *(Add your `GEMINI_API_KEY` inside `.env`)*

3. **Run the interactive menu:**
   ```bash
   python main.py
   ```

   Or pass queries directly via the command line:
   ```bash
   python main.py "Going to Arba Minch for a 2-day weekend getaway by the lake. Suggest activities and what to bring."
   ```

---

### Method 2: Single-File Python Script

Run the self-contained script directly:
```bash
python week_06_build_ai_agent.py
```

---

### Method 3: Google Colab / Jupyter Notebook

1. Open `Week_06_Build_AI_Agent.ipynb` in [Google Colab](https://colab.research.google.com).
2. Add your secret key in the Colab **Secrets (🔑)** tab under `GEMINI_API_KEY` and enable **Notebook access**.
3. Run the notebook to see the ReAct loop and rendered travel guide inline.

---

## 🧪 Verified Execution Logs

### Scenario 1: Bangkok 2-Week Corporate + 3-Day Refreshment
```text
🎯 USER REQUEST: I am going to bangkok tomorrow to attend a business meeting for 2 weeks, 
so give me what should I pack and plan a refreshment idea after the meeting for the last three days.

🔄 [Step 1/6] Agent reasoning...
🛠️  Action: get_city_activities({"theme": "refreshment", "num_days": 3, "city": "Bangkok"})
👀 Observation: success (Found Chao Phraya River cruise, wellness spas, Lumpini Park)

🔄 [Step 2/6] Agent reasoning...
🛠️  Action: get_weather_forecast({"days": 7, "city": "Bangkok"})
👀 Observation: success (Highs ~35°C, Lows ~26°C, tropical humidity)

🔄 [Step 3/6] Agent reasoning...
🛠️  Action: save_travel_plan({"filename": "bangkok_business_and_refreshment_plan.md"})
👀 Observation: success (Saved to outputs/bangkok_business_and_refreshment_plan.md)

🔄 [Step 4/6] Agent reasoning...
✅ Mission complete (Powered by gemini-flash-lite-latest)!
```

### Scenario 2: Beijing Anime & Tech Shopping (Auto-Corrected Typo)
```text
🎯 USER REQUEST: I am going to Bejing for 5 days of anime and tech shopping. What should I pack?

🔄 [Step 1/6] Agent reasoning...
🛠️  Action: get_city_activities({"city": "Beijing", "theme": "anime and tech shopping"})
👀 Observation: success (Discovered Zhongguancun 'Silicon Valley' and Joy City pop-up hubs)

🔄 [Step 2/6] Agent reasoning...
🛠️  Action: get_weather_forecast({"city": "Beijing", "days": 5})
👀 Observation: success (Highs 6°C–12°C, sub-zero lows down to -2°C)

🔄 [Step 3/6] Agent reasoning...
🛠️  Action: save_travel_plan({"filename": "beijing_anime_tech_shopping_plan.md"})
👀 Observation: success (Included thermal base layers, Type A/I adapters, and WeChat/Alipay setup)

🔄 [Step 4/6] Agent reasoning...
✅ Mission complete!
```

---

## 🔒 Security & Best Practices
- **Protected Secrets**: `.gitignore` prevents `.env` or credential leakage to GitHub.
- **Defensive Error Handling**: Automatic fallback routing ensures seamless operation even during cloud traffic spikes.
- **Offline / Degraded Operation**: Gracefully catches tool network errors and synthesizes regional climate guidance without crashing.

---

## 👨‍💻 Author
Built by a Software Engineering student at **Addis Ababa Science and Technology University (AASTU)** as part of the **AWS AI/ML Mentorship Program**.