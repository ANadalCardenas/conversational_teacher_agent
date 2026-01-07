# English Conversational Teacher

An interactive **English Conversational Teacher** web application that helps users practice English through conversation, receive instant corrections, detailed explanations, and a final learning summary. The project pairs a lightweight interface with an AI-driven Python backend to deliver seamless **voice interaction** powered by **automatic speech recognition**.


---

## Features

- Conversational English practice (voice-based interaction)
- Transcription to text with speech recognition model (Wishper, https://openai.com/index/whisper/)
- Instant sentence correction with highlighted improvements
- Clear explanations of grammar, vocabulary, and usage mistakes
- Context-aware follow-up questions
- Session summary with common mistakes and suggested activities
- Press-and-hold speech input
- Fully Dockerized frontend and backend

---

## Application Screenshots

The repository includes screenshots showing:
- Live conversational questions/responses 
- Sentence feedback with corrections and explanations  
- Final session summaries with learning recommendations
<img width="870" height="405" alt="Screenshot from 2026-01-04 13-27-20" src="https://github.com/user-attachments/assets/26a4e72c-e159-4a56-bf63-0edaea0081a2" />
<img width="865" height="906" alt="Screenshot from 2026-01-04 13-27-04" src="https://github.com/user-attachments/assets/170aa296-c1c6-4706-982a-9eef92d37a1e" />
<img width="844" height="785" alt="Screenshot from 2026-01-04 17-07-50" src="https://github.com/user-attachments/assets/04462fc1-d9d6-486a-ba3b-bab39c74c2a2" />
<img width="850" height="824" alt="Screenshot from 2026-01-04 17-15-39" src="https://github.com/user-attachments/assets/c56cd1a1-7644-4b03-8acb-e55e6f8b4f52" />

---

## Project Structure

```
.
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── chatgpt_client.py
│   │   ├── main.py
│   │   └── speech_to_text.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend
│   ├── html
│   │   ├── index.html
│   │   ├── script.js
│   │   └── style.css
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yaml
├── .gitignore
└── README.md
```


```mermaid
flowchart TD
  U((User))

  subgraph FE[Frontend - Browser]
    MIC[Hold microphone button]
    UI1[Show corrections or summary]
    SUMBTN[Request session summary]
  end

  subgraph BE[Backend API]
    API_ASR[POST transcribe audio]
    API_TXT[POST chat message]
    API_SUM[POST summary request]
    CTX[(Conversation context)]
  end

  subgraph ASR[Speech to Text]
    WHISPER[Whisper model]
  end

  subgraph LLM[AI Teacher Agent - OpenAI]
    CORR[Correct user sentence]
    EXPL[Explain mistakes]
    FOLLOW[Generate follow up question]
    SUM[Generate learning summary]
  end

  %% Voice input path
  U --> MIC --> API_ASR
  API_ASR --> WHISPER --> API_TXT

  %% Teacher response
  API_TXT --> CTX
  CTX --> CORR --> EXPL --> FOLLOW --> UI1
  UI1 --> U
  FOLLOW --> CTX

  %% Summary flow
  U --> SUMBTN --> API_SUM
  API_SUM --> CTX --> SUM --> UI1
```

---

## Getting Started

### Prerequisites
- Docker
- Docker Compose
- OpenAI API key. Create it, then copy it into the .env file located in the project folder.
  OPENAI_API_KEY = ... (private key).

### Run the application

```bash
docker-compose up --build
```

Open your browser at:

```
http://localhost:8080
```

---

## How It Works

1. User speaks an English sentence.
2. With a speech recognition model, the application transcribes into text what the user said.
3. Backend processes the input using AI.
4. The user receives:
   - A corrected sentence
   - An explanation of mistakes
   - A conversational reply
5. At the end, a session summary highlights common errors and exercises.

---

## License

Educational and experimental use.

---


