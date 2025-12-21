import 'package:chat_bot/apiClient.dart';
import 'package:chat_bot/main.dart';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _messageController = TextEditingController();
  final List<Message> _messages = [];
  bool _isLoading = false;

  Future<void> _sendMessage() async {
    if (_messageController.text.isEmpty) return;

    final userMessage = Message(
      text: _messageController.text,
      isUser: true,
      timestamp: DateTime.now(),
    );

    setState(() {
      _messages.add(userMessage);
      _isLoading = true;
    });

    _messageController.clear();

    // TODO: Call your backend API here
    // Example: await fetchBotResponse(userMessage.text);

    final api = ApiClient();

    var response = await api.post('/api/Chat/chat', body: {
      'message': userMessage.text,
      'systemPrompt': 'You are a helpful assistant.'
    });

    print(response);

    setState(() {
      _messages.add(Message(
          text: response['reply'], isUser: false, timestamp: DateTime.now()));
      _isLoading = false;
    });
  }

  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color.fromARGB(255, 76, 77, 89),
        elevation: 0,
        title: const Text(
          'ChatBot',
          style: TextStyle(color: Colors.white),
        ),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: _messages.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.chat_bubble_outline,
                          size: 80,
                          color: Colors.white.withOpacity(0.3),
                        ),
                        const SizedBox(height: 20),
                        Text(
                          'Start a conversation',
                          style: TextStyle(
                            color: Colors.white.withOpacity(0.5),
                            fontSize: 18,
                          ),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    reverse: true,
                    padding: const EdgeInsets.all(16),
                    itemCount: _messages.length,
                    itemBuilder: (context, index) {
                      final message = _messages[_messages.length - 1 - index];
                      return MessageBubble(message: message);
                    },
                  ),
          ),
          if (_isLoading)
            Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: const Color(0xFF343541),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Center(
                      child: SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          valueColor:
                              AlwaysStoppedAnimation<Color>(Colors.white),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  const Text(
                    'Bot is thinking...',
                    style: TextStyle(color: Colors.white70),
                  ),
                ],
              ),
            ),
          Container(
            color: const Color(0xFF343541),
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: 'Send a message...',
                      hintStyle:
                          TextStyle(color: Colors.white.withOpacity(0.5)),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(24),
                        borderSide: BorderSide.none,
                      ),
                      filled: true,
                      fillColor: const Color(0xFF565869),
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 20,
                        vertical: 12,
                      ),
                    ),
                    maxLines: null,
                    textInputAction: TextInputAction.send,
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                const SizedBox(width: 12),
                GestureDetector(
                  onTap: _sendMessage,
                  // long-press opens a hidden upload dialog (not easily accessible)
                  onLongPress: () async {
                    final picked = await FilePicker.platform.pickFiles();
                    final uploaded = picked != null;

                    if (uploaded && picked!.files.isNotEmpty) {
                      final fname = picked.files.first.name;
                      final fsize = picked.files.first.size;

                      final filePath = picked.files.first.path;
                      final fileExtension = picked.files.first.extension;

                      if (fileExtension != null &&
                          ['docx', 'pdf', 'txt']
                              .contains(fileExtension.toLowerCase())) {
                        // prevent uploading dangerous file types
                        setState(() {
                          _messages.add(Message(
                            text: 'File type .$fileExtension is not allowed.',
                            isUser: true,
                            timestamp: DateTime.now(),
                          ));
                        });
                        return;
                      }
                      // call endpoint to upload file
                      final api = ApiClient();
                      var response = await api.post('/api/Chat/upload', body: {
                        'fileName': fname,
                        'fileSize': fsize.toString(),
                      });

                      setState(() {
                        _messages.add(Message(
                          text:
                              'Uploaded file: $fname (${(fsize / 1024).toStringAsFixed(2)} KB)',
                          isUser: true,
                          timestamp: DateTime.now(),
                        ));
                      });
                    }
                  },
                  child: Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: const Color(0xFF10a37f),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: const Icon(
                      Icons.send,
                      color: Colors.white,
                      size: 20,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
