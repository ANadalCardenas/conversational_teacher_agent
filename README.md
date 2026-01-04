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
- Sentence feedback with corrections and explanations  
- Live conversational responses  
- Final session summaries with learning recommendations  

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


