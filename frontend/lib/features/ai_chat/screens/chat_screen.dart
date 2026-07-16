import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lifeos/core/telegram_service.dart';

class ChatScreen extends ConsumerStatefulWidget {
  const ChatScreen({super.key});

  @override
  ConsumerState<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends ConsumerState<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<ChatMessage> _messages = [];
  bool _isLoading = false;
  String? _conversationId;

  @override
  void initState() {
    super.initState();
    _messages.add(ChatMessage(
      text: "Hi! I'm your LifeOS AI assistant. How can I help you today?\n\n"
          "Try:\n"
          "• \"I spent 200 CZK on food\"\n"
          "• \"Remind me tomorrow at 9\"\n"
          "• \"I walked 5 km\"",
      isUser: false,
    ));
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _sendMessage() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    setState(() {
      _messages.add(ChatMessage(text: text, isUser: true));
      _controller.clear();
      _isLoading = true;
    });

    try {
      final response = await telegramService.apiPost(
        '/api/v1/ai/chat',
        data: {
          'message': text,
          if (_conversationId != null) 'conversation_id': _conversationId,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data;
        setState(() {
          _conversationId = data['conversation_id'];
          _messages.add(ChatMessage(
            text: data['response'],
            isUser: false,
            actionTaken: data['action_taken'],
          ));
        });
      } else {
        setState(() {
          _messages.add(ChatMessage(
            text: 'Sorry, something went wrong. Please try again.',
            isUser: false,
          ));
        });
      }
    } catch (e) {
      setState(() {
        _messages.add(ChatMessage(
          text: 'Error: ${e.toString()}\n\nPlease check your connection.',
          isUser: false,
        ));
      });
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Assistant'),
        actions: [
          IconButton(
            icon: const Icon(Icons.mic),
            onPressed: () {
              // TODO: Voice input
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Messages
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                return _ChatBubble(message: message);
              },
            ),
          ),

          // Loading indicator
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.all(8),
              child: CircularProgressIndicator(),
            ),

          // Input
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Theme.of(context).scaffoldBackgroundColor,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.05),
                  blurRadius: 10,
                  offset: const Offset(0, -2),
                ),
              ],
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText: 'Type a message...',
                      border: InputBorder.none,
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  onPressed: _isLoading ? null : _sendMessage,
                  icon: const Icon(Icons.send),
                  color: Theme.of(context).colorScheme.primary,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class ChatMessage {
  final String text;
  final bool isUser;
  final Map<String, dynamic>? actionTaken;

  ChatMessage({
    required this.text,
    required this.isUser,
    this.actionTaken,
  });
}

class _ChatBubble extends StatelessWidget {
  final ChatMessage message;

  const _ChatBubble({required this.message});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: message.isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.8,
        ),
        decoration: BoxDecoration(
          color: message.isUser
              ? Theme.of(context).colorScheme.primary
              : Theme.of(context).colorScheme.surfaceVariant,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              message.text,
              style: TextStyle(
                color: message.isUser
                    ? Theme.of(context).colorScheme.onPrimary
                    : Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
            if (message.actionTaken != null) ...[
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.green.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.check_circle, size: 16, color: Colors.green),
                    const SizedBox(width: 4),
                    Text(
                      'Action completed',
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.green[700],
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
