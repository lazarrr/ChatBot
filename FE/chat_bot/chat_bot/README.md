# ChatBot Flutter Application

This project is a Flutter-based chatbot application that provides a user interface similar to ChatGPT. The app allows users to interact with a chatbot, sending and receiving messages in a chat-like environment.

## Project Structure

```
chat_bot
├── lib
│   ├── main.dart                # Entry point of the application
│   ├── screens
│   │   ├── chat_screen.dart     # Chat interface
│   │   └── home_screen.dart     # Landing page
│   ├── widgets
│   │   ├── message_bubble.dart   # Individual message representation
│   │   ├── chat_input_field.dart  # Input field for messages
│   │   └── chat_list.dart        # List of messages
│   ├── models
│   │   ├── message.dart          # Message model
│   │   └── chat.dart             # Chat session model
│   ├── services
│   │   ├── api_service.dart      # API calls handling
│   │   └── chat_service.dart     # Chat logic management
│   ├── providers
│   │   └── chat_provider.dart     # State management for chat
│   └── utils
│       └── constants.dart        # Constant values
├── pubspec.yaml                  # Project configuration
└── README.md                     # Project documentation
```

## Getting Started

To run this project, ensure you have Flutter installed on your machine. Follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd chat_bot
   ```

3. Install the dependencies:
   ```
   flutter pub get
   ```

4. Run the application:
   ```
   flutter run
   ```

## Features

- User-friendly chat interface
- Real-time message sending and receiving
- State management using ChangeNotifier
- API integration for backend communication

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.