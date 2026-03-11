# DroidIDE

A mobile cloud IDE for Android, similar to Firebase Studio / Project IDX.

## Core Concept

A Flutter app that gives the user:
- A code editor with syntax highlighting (Monaco Editor via WebView)
- An integrated terminal (xterm.js via WebView + WebSocket)
- An AI coding agent chat (OpenRouter API)
- A file manager for projects
- Connection to a backend that runs code-server (open-source VS Code server) in Docker

## Tech Stack

- **Frontend**: Flutter 3.41.4 (Dart, null safety)
  - `webview_flutter` — for Monaco editor and xterm.js terminal
  - `web_socket_channel` — for terminal WebSocket connection
  - `http` — for REST API calls
- **Backend**: FastAPI (Python) + code-server + Docker
- **AI**: OpenRouter API, default model: `meta-llama/llama-3.3-70b-instruct:free`
- **Monetization**: Freemium (30 free AI requests/day, unlimited on Pro subscription)

## Architecture

**Flutter App**
  - **Monaco Editor (WebView)** ←→ FastAPI `/files`
  - **xterm.js Terminal (WebView)** ←→ FastAPI WebSocket `/ws/terminal`
  - **AI Chat sidebar** ←→ FastAPI `/ai/chat` ←→ OpenRouter API
  - **File Manager** ←→ FastAPI `/files`

**FastAPI Backend**
  - Docker container with `code-server` per project
  - `/ai/chat` — proxies to OpenRouter, tracks daily usage
  - `/files` — CRUD for project files
  - `/ws/terminal` — WebSocket bridge to container shell

## Project File Structure

```
droidide/
├── lib/
│   ├── main.dart                   # Entry point, MaterialApp, bottom nav
│   ├── screens/
│   │   ├── editor_screen.dart      # Monaco editor in WebView
│   │   ├── terminal_screen.dart    # xterm.js terminal in WebView
│   │   └── chat_screen.dart        # AI agent chat UI
│   ├── widgets/
│   │   ├── file_tree.dart          # Sidebar file manager
│   │   ├── code_editor.dart        # WebView wrapper for Monaco
│   │   ├── terminal_view.dart      # WebView wrapper for xterm.js
│   │   └── ai_chat.dart            # Chat bubbles + input
│   ├── services/
│   │   ├── websocket_service.dart  # WebSocket for terminal
│   │   ├── ai_service.dart         # OpenRouter API calls
│   │   └── file_service.dart       # File CRUD via REST
│   └── models/
│       ├── project.dart
│       ├── file_node.dart
│       └── chat_message.dart
backend/
├── main.py                         # FastAPI app
├── routers/
│   ├── ai.py                       # /ai/chat endpoint
│   ├── files.py                    # /files CRUD
│   └── terminal.py                 # WebSocket /ws/terminal
├── services/
│   ├── docker_service.py           # Manage code-server containers
│   └── usage_service.py            # Track free tier limits
├── .env                            # OPENROUTER_API_KEY, SECRET_KEY
├── docker-compose.yml
└── Dockerfile
```

## UI/UX Requirements

- Dark theme by default (background `#1e1e1e` like VS Code)
- Bottom navigation: Editor | Terminal | AI Chat
- Drawer (left): file tree + project switcher
- Top bar: filename, run button, settings icon
- AI chat: floating panel or bottom sheet that can overlay editor
- Mobile-first: large tap targets, no hover-dependent UI

## Getting Started

### Prerequisites

- Flutter SDK
- Docker
- Python 3.9+

### Frontend (Flutter)

1.  Navigate to the `droidide` directory:
    ```bash
    cd droidide
    ```
2.  Install dependencies:
    ```bash
    flutter pub get
    ```
3.  Run the app:
    ```bash
    flutter run
    ```

### Backend (FastAPI)

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create a `.env` file and add your `OPENROUTER_API_KEY`:
    ```
    OPENROUTER_API_KEY=your_key_here
    ```
3.  Run the backend using Docker Compose:
    ```bash
    docker-compose up --build
    ```

The backend will be available at `http://localhost:8000`.
