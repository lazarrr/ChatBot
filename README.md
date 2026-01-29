# ChatBot Gateway

Gateway application for an AI chatbot system.

## Architecture
- Flutter (Frontend)
- ASP.NET Core Web API (Gateway)
- Python worker (Microservice for OpenAI communication)

## Solution Structure
- ChatBot.Gateway.Api
- ChatBot.Gateway.Application
- ChatBot.Gateway.Domain
- ChatBot.Gateway.Infrastructure
- ChatBot.Gateway.Contracts
- ChatBot.Gateway.Shared

## Tech Stack
- .NET 8
- Flutter
- Python 
- OpenAI API

## How to run
First step is to run docker command for rabbitmq (command below)
After first step we need to run: (in separate terminal)
- dotnet run (for BE)
- flutter run (for FE)
- python worker.py (for py worker)

## RabbitMq

- docker run
# latest RabbitMQ 4.x
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
