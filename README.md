# ChatBot Gateway

Gateway application for an AI chatbot system that connects a Flutter frontend with an AI worker service through an ASP.NET Core backend and RabbitMQ messaging.

## Architecture

The system consists of three main components:

* **Frontend:** Flutter mobile/web application
* **Backend Gateway:** ASP.NET Core Web API
* **AI Worker:** Python microservice responsible for communicating with the OpenAI API

Communication between services is handled using **RabbitMQ**.

## Solution Structure

```
![architecture overview](https://github.com/lazarrr/ChatBot/blob/main/Gemini_Generated_Image_bzfve7bzfve7bzfv.png)
```

## Tech Stack

* **.NET 8**
* **Flutter**
* **Python**
* **RabbitMQ**
* **OpenAI API**
* **Docker**

---

# Prerequisites

Before running the project, make sure the following tools are installed:

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

---

# Application Flow

1. The **Flutter app** sends a request to the **ASP.NET Core Gateway API**.
2. The Gateway publishes a message to **RabbitMQ**.
3. The **Python Worker** consumes the message.
4. The worker sends the request to the **OpenAI API**.
5. The response is returned through the same pipeline back to the **Flutter application**.

---