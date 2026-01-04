# English Conversational Teacher

An interactive **English Conversational Teacher** web application that helps users practice English through conversation, receive instant corrections, detailed explanations, and a final learning summary. The project combines a lightweight frontend with a Python backend powered by AI, and supports **text and voice-based interaction**.

---

## Features

- Conversational English practice (text + speech)
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

1. User writes or speaks an English sentence.
2. Backend processes the input using AI.
3. The user receives:
   - A corrected sentence
   - An explanation of mistakes
   - A conversational reply
4. At the end, a session summary highlights common errors and exercises.

---

## Target Users

- English learners
- Professionals preparing for English-speaking roles
- Remote workers
- Users who want detailed feedback, not just corrections

---

## License

Educational and experimental use.

---


