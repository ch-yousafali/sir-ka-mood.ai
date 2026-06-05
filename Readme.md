
readme_content = """# Sir Kamood - Sir Ne Marks Kaise Diye?

> The official conspiracy theory generator for desi students who survived differential equations.

---

## What is this?

Sir Kamood is a dark-themed web app where students enter their exam marks and get **one AI-generated conspiracy theory** about why their professor gave them those marks. Funny, personal, and Urdu-English mixed (Roman Urdu). It also generates formal appeal letters with the student's name, roll number, and department (CHEP).

Built with Flask + OpenRouter AI. Apple-inspired clean UI. Zero emojis.

---

## Features

### Conspiracy Analyzer
- Enter your subject, marks obtained, and marks expected
- AI generates **ONE personalized conspiracy theory** based on your marks range:
  - **0-9**: Extreme Disaster (Sir's life completely fell apart)
  - **10-19**: Biwi Ka Badla (Sir got destroyed at home)
  - **20-29**: Petrol Price Trauma (economic depression hits marks)
  - **30-39**: Cricket Match Curse (team lost, you pay)
  - **40-49**: Chai Mein Cheeni Kam (morning ruined = marks ruined)
  - **50-54**: Neend Poori Nahi Hui (sleepy Sir checking papers)
  - **55-59**: WhatsApp Distraction (family group drama)
  - **60-64**: Lunch Break Pe Tha (hungry and rushing)
  - **65-69**: Biryani Wali Khushi (amazing food = amazing marks)
  - **70-74**: Cricket Jeet Gaya (team won, everyone wins)
  - **75-79**: Sunday Ka Mood (weekend vibes on a weekday)
  - **80-84**: Chai Pilayi Thi (you brought him tea)
  - **85-89**: Favorite Student Theory (teacher's pet confirmed)
  - **90-94**: Sir Ne Khud Solve Kia (he did the paper for you)
  - **95-100**: University Ka Future Star (the chosen one)
- Each theory type has **5 random sub-variations** — every click gives a unique response
- **Disclaimer** added to every response: "This is purely for fun..."

### Appeal Letter Generator
- Enter your **name** and **roll number** (custom, not hardcoded)
- Generates a professional email to request mark review
- Displays student info card with **Department: CHEP** badge
- Copy to clipboard or send via email (mailto link)
- Sir Atif Sultan tease included

### UI/UX
- Dark mode (slate/black theme) with red accents
- Apple.com inspired clean typography (Inter font)
- Glassmorphism cards with subtle noise texture
- Typewriter effect for AI responses
- Confetti animation for marks >= 50
- Sad face animation for marks < 50
- Mobile responsive
- No emojis anywhere

### Share Features
- Copy result to clipboard
- Share on WhatsApp with pre-formatted text
- Generate unique shareable URL (base64 encoded)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Browser (Chrome/Firefox/Safari)                      │  │
│  │  • Single Page App (vanilla HTML/CSS/JS)              │  │
│  │  • Dark theme with glassmorphism cards                │  │
│  │  • Typewriter animation for AI text                   │  │
│  │  • Canvas confetti + SVG sad face animations          │  │
│  │  • Clipboard API + WhatsApp share + mailto links      │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/JSON
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      FLASK BACKEND                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  app.py (Python 3)                                    │  │
│  │  • Route handlers: /, /api/test, /api/conspiracy      │  │
│  │    /api/appeal                                        │  │
│  │  • Theory type selector (15 marks ranges)             │  │
│  │  • Random sub-variation picker (5 per type)           │  │
│  │  • AI prompt builder (system + user prompts)          │  │
│  │  • Fallback chain: OpenRouter → DeepSeek → Mock       │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌────────────────────────┴────────────────────────────┐    │
│  │              AI Provider Layer                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │    │
│  │  │ OpenRouter  │  │  DeepSeek   │  │   Mock    │  │    │
│  │  │ (Primary)   │→ │  (Backup)   │→ │ (Offline) │  │    │
│  │  │ Free: 200/d │  │ $5 credits  │  │ Unlimited │  │    │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                 │
│  ┌────────────────────────┴────────────────────────────┐    │
│  │              Environment & Config                   │    │
│  │  • .env: OPENROUTER_API_KEY, DEEPSEEK_API_KEY       │    │
│  │  • python-dotenv for local dev                      │    │
│  │  • Vercel env vars for production                   │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User enters marks ──→ Frontend POST /api/conspiracy ──→ Flask backend
                                                           │
                                                           ▼
                                              Theory type selector
                                              (marks → 1 of 15 types)
                                                           │
                                                           ▼
                                              Random sub-variation picker
                                              (1 of 5 seed ideas)
                                                           │
                                                           ▼
                                              AI prompt builder
                                              (system prompt + user prompt)
                                                           │
                                                           ▼
                                              OpenRouter API call
                                              (unique seed each time)
                                                           │
                                              ┌────────────┴────────────┐
                                              │                         │
                                              ▼                         ▼
                                           Success                   Fail
                                              │                         │
                                              ▼                         ▼
                                         AI response              DeepSeek?
                                              │                    (if key exists)
                                              │                         │
                                              │              ┌──────────┴──────────┐
                                              │              │                   │
                                              │           Success             Fail
                                              │              │                   │
                                              │              ▼                   ▼
                                              │         AI response         Mock fallback
                                              │         (unique)            (pre-written template
                                              │                             with user data inserted)
                                              │                             │
                                              └──────────────┬──────────────┘
                                                             │
                                                             ▼
                                              Response + Disclaimer
                                                             │
                                                             ▼
                                              Frontend typewriter display
```

### Key Design Decisions

| Decision | Reason |
|----------|--------|
| **Single HTML file** | No build step, no bundler, deploy anywhere |
| **Vanilla JS** | No framework overhead, instant load |
| **Flask (not FastAPI)** | Simple, proven, easy Vercel deployment |
| **OpenRouter primary** | Free tier, no credit card, access to Llama/Mistral |
| **15 marks ranges** | Granular humor — 44 vs 48 get different vibes |
| **5 sub-variations each** | 75 seed ideas = 75+ unique theory directions |
| **Random seed per request** | OpenRouter generates different text every time |
| **Mock fallback chain** | App never breaks, works offline, zero downtime |
| **Disclaimer on every response** | Legal/social safety, sets fun tone |
| **No emojis** | Clean Apple aesthetic, professional look |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask (Python) |
| AI API | OpenRouter (free tier: 200 requests/day) |
| Frontend | HTML/CSS/JS (vanilla, no frameworks) |
| Fonts | Inter (Google Fonts) |
| Deployment | Vercel |

---

## Project Structure

```
sir-kamood/
├── app.py              # Flask backend + AI integration
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel deployment config
├── .env                # API keys (not committed)
└── templates/
    └── index.html      # Complete frontend (single file)
```

---

## Setup & Run Locally

### 1. Clone & Create Virtual Environment

```bash
mkdir sir-kamood
cd sir-kamood
python3 -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get OpenRouter API Key (FREE)

1. Go to [openrouter.com/keys](https://openrouter.com/keys)
2. Sign up with Google or GitHub (30 seconds)
3. Click "Create Key"
4. Copy the key (starts with `sk-or-...`)

### 4. Configure Environment

Create `.env` file:

```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### 5. Run the App

```bash
flask run
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

Test the API: [http://127.0.0.1:5000/api/test](http://127.0.0.1:5000/api/test)

---

## Deploy to Vercel

```bash
npm i -g vercel
vercel login
vercel
```

Then add your `OPENROUTER_API_KEY` in Vercel dashboard:
**Project Settings > Environment Variables**

---

## How the AI Works

1. User enters marks
2. Backend picks **one theory type** from 15 ranges based on marks
3. Picks a **random sub-variation** (seed idea) from 5 options
4. Sends to OpenRouter AI with a **trained system prompt** describing the vibe
5. AI generates a **unique, creative theory** expanding on that seed
6. If AI fails → simple mock fallback kicks in instantly
7. **Disclaimer** prepended to every response

The model is trained via system prompt — no pre-written templates in the final output. Every request gets a different random seed, so responses are unique every time.

---

## Free Tier Limits

| Service | Limit |
|---------|-------|
| OpenRouter | 200 requests/day, 20/min |
| DeepSeek (backup) | $5 free credits (~500K tokens) |
| Mock fallback | Unlimited, works offline |

---

## Credits

- Built for students who know the truth
- Differential Paper survivors (50% failure rate, never forget)
- Sir Atif Sultan (he won't increase marks, but try karne mein kuch nahi jaata)

---

## License

MIT — use it, roast your professors, deploy with trauma.
"""

with open('/mnt/agents/output/README.md', 'w') as f:
    f.write(readme_content)

print("README.md updated with Architecture section!")
