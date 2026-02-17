import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'chatbot_screen.dart';

class HomeScreen extends StatelessWidget {
  final String token;
  const HomeScreen({super.key, required this.token});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Home')),
      body: Center(
        child: ElevatedButton.icon(
          icon: const Icon(Icons.history),
          label: const Text('View Previous Conversations'),
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => ConversationListScreen(token: token),
              ),
            );
          },
        ),
      ),
    );
  }
}

class ConversationListScreen extends StatefulWidget {
  final String token;
  const ConversationListScreen({super.key, required this.token});

  @override
  State<ConversationListScreen> createState() => _ConversationListScreenState();
}

class _ConversationListScreenState extends State<ConversationListScreen> {
  List<String> conversations = [];

  Future<void> _fetchConversations() async {
    final response = await http.get(
      Uri.parse('http://10.0.2.2:8000/conversations'),
      headers: {'Authorization': widget.token},
    );
    final data = jsonDecode(response.body);
    setState(() {
      conversations = List<String>.from(data['conversations']);
    });
  }

  @override
  void initState() {
    super.initState();
    _fetchConversations();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Your Conversations')),
      body: ListView.builder(
        itemCount: conversations.length,
        itemBuilder: (context, index) {
          final name = conversations[index];
          return ListTile(
            title: Text(name),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ChatbotScreen(
                    token: widget.token,
                    conversationName: name,
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}