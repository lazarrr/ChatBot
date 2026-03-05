# ChatBot Gateway

Gateway application for an AI chatbot system that connects a Flutter frontend with an AI worker service through an ASP.NET Core backend and RabbitMQ messaging.

## Architecture

The system consists of three main components:

* **Frontend:** Flutter mobile/web application
* **Backend Gateway:** ASP.NET Core Web API
* **AI Worker:** Python microservice responsible for communicating with the OpenAI API

Communication between services is handled using **RabbitMQ**.

## Solution Structure


<img src="https://github.com/lazarrr/ChatBot/blob/main/architecture.png" width="600"/>


## Tech Stack

* **.NET 8**
* **Flutter**
* **Python**
* **RabbitMQ**
* **OpenAI API**
* **Docker**

---

# Prerequisites

Before running the project, make sure the following tools are installed or aquared:

### 1. .NET

Install **.NET 8 SDK**

[https://dotnet.microsoft.com/download/dotnet/8.0](https://dotnet.microsoft.com/download/dotnet/8.0)

Verify installation:

```bash
dotnet --version
```

---

### 2. Flutter

Install Flutter by following the official guide:

[https://docs.flutter.dev/get-started/install](https://docs.flutter.dev/get-started/install)

Verify installation:

```bash
flutter doctor
```

---

### 3. Python

Install **Python 3.9+**

[https://www.python.org/downloads/](https://www.python.org/downloads/)

Verify installation:

```bash
python --version
```

---

### 4. Docker

Docker is required for running **RabbitMQ**.

Install Docker:

[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

Verify installation:

```bash
docker --version
```

---

### 5. OpenAI Key

This project is working with OpenAI, so in order to run it you need to have OPENAI_API_KEY key set as variable in you pc

> for mac os

Open a Terminal and add the key to your shell config file (~/.zshrc or ~/.bashrc):
```bash
echo 'export OPENAI_API_KEY="your_api_key"' >> ~/.zshrc
```
Apply changes by restarting the terminal or running source ~/.zshrc.
Verify with 

```bash
echo $OPENAI_API_KEY.
```

> for windows

 - Via Control Panel (Permanent): Search for "Environment Variables," click "Edit the system environment variables," add a new user variable named OPENAI_API_KEY with your key as the value, and restart the command prompt.
 - Via Command Prompt (Permanent): Use setx OPENAI_API_KEY "your_api_key" and restart the command prompt.
---

# Setup

## 1. Start RabbitMQ

Run RabbitMQ using Docker:

```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
```

RabbitMQ Management UI will be available at:

```
http://localhost:15672
```

Default credentials:

```
username: guest
password: guest
```

---

## 2. Install Python Dependencies

Navigate to the AI worker project:

```bash
cd AI/api
```

Install dependencies from `requirements.txt` (it is recommended to use some isolated environments e.g. venv or conda):

```bash
pip install -r requirements.txt
```

---

# Running the Application

The system requires **three services** to be running simultaneously.

Open **three separate terminals**.

---

## 1. Run Backend (.NET)

Navigate to the backend project and run:

```bash
dotnet run
```

---

## 2. Run Flutter Frontend

Navigate to the Flutter project directory and run:

```bash
flutter run
```

---

## 3. Run Python AI Worker

Navigate to the worker directory:

```bash
cd AI/api
```

Run the worker:

```bash
python worker.py
```
