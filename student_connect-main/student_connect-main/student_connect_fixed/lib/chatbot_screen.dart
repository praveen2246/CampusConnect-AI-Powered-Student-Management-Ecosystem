import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:google_fonts/google_fonts.dart';
import 'package:animate_do/animate_do.dart';
import 'package:url_launcher/url_launcher.dart';
import 'config.dart';

class ChatbotScreen extends StatefulWidget {
  final String token;
  final String? conversationName;
  const ChatbotScreen({super.key, required this.token, this.conversationName});

  @override
  State<ChatbotScreen> createState() => _ChatbotScreenState();
}

class _ChatbotScreenState extends State<ChatbotScreen> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<ChatMessage> _messages = [];
  bool _isTyping = false;
  String? _currentConversationName;

  @override
  void initState() {
    super.initState();
    _currentConversationName = widget.conversationName;
    if (_currentConversationName != null) {
      _loadConversation(_currentConversationName!);
    } else {
      // Welcome message
      _messages.add(ChatMessage(
        text: "Hello! I'm your Campus AI Assistant. How can I help you with your outpasses or certificates today?",
        isUser: false,
        time: DateTime.now(),
      ));
    }
  }

  Future<void> _loadConversation(String name) async {
    setState(() => _isTyping = true);
    try {
      final response = await http.get(
        Uri.parse(AppConfig.conversationUrl(name)),
        headers: {'Authorization': widget.token},
      );
      final data = jsonDecode(response.body);
      setState(() {
        _messages.clear();
        _currentConversationName = name;
        for (var msg in data['messages']) {
          _messages.add(ChatMessage(text: msg['user_message'], isUser: true, time: DateTime.parse(msg['timestamp'])));
          _messages.add(ChatMessage(text: msg['bot_response'], isUser: false, time: DateTime.parse(msg['timestamp'])));
        }
        _isTyping = false;
      });
      _scrollToBottom();
    } catch (e) {
      setState(() => _isTyping = false);
    }
  }

  Future<void> _sendMessage() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    setState(() {
      _messages.add(ChatMessage(text: text, isUser: true, time: DateTime.now()));
      _controller.clear();
      _isTyping = true;
    });
    _scrollToBottom();

    _currentConversationName ??= text.length > 20 ? text.substring(0, 20) : text;

    try {
      final response = await http.post(
        Uri.parse(AppConfig.chatUrl),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': widget.token,
        },
        body: jsonEncode({
          'message': text,
          'conversation_name': _currentConversationName,
        }),
      );

      final data = jsonDecode(response.body);
      setState(() {
        _isTyping = false;
        _messages.add(ChatMessage(
          text: data['reply'] ?? "I'm not sure how to respond to that.",
          isUser: false,
          time: DateTime.now(),
        ));
      });
      _scrollToBottom();
    } catch (e) {
      setState(() {
        _isTyping = false;
        _messages.add(ChatMessage(text: "Connection error. Please try again later.", isUser: false, time: DateTime.now()));
      });
    }
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF1F5F9),
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Color(0xFF1E293B), size: 20),
          onPressed: () => Navigator.pop(context),
        ),
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              "Campus AI Assistant",
              style: GoogleFonts.inter(fontSize: 18, fontWeight: FontWeight.w800, color: const Color(0xFF1E293B)),
            ),
            Row(
              children: [
                Container(width: 8, height: 8, decoration: const BoxDecoration(color: Colors.green, shape: BoxShape.circle)),
                const SizedBox(width: 5),
                Text("Online", style: GoogleFonts.inter(fontSize: 12, color: Colors.green, fontWeight: FontWeight.w600)),
              ],
            ),
          ],
        ),
        centerTitle: false,
        actions: [
          IconButton(
            icon: const Icon(Icons.history_rounded, color: Color(0xFF64748B)),
            onPressed: () {}, // History logic can be added later
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
              itemCount: _messages.length,
              itemBuilder: (context, index) => _buildChatBubble(_messages[index]),
            ),
          ),
          if (_isTyping)
            FadeIn(
              child: Padding(
                padding: const EdgeInsets.only(left: 25, bottom: 10),
                child: Row(
                  children: [
                    Text("AI is thinking...", style: GoogleFonts.inter(fontSize: 12, color: const Color(0xFF64748B), fontStyle: FontStyle.italic)),
                  ],
                ),
              ),
            ),
          _buildInputArea(),
        ],
      ),
    );
  }

  Widget _buildChatBubble(ChatMessage message) {
    final bool hasLink = message.text.contains("http://10.0.2.2");
    String cleanText = message.text;
    String? link;

    if (hasLink) {
      final startIndex = message.text.indexOf("http://");
      if (startIndex != -1) {
        link = message.text.substring(startIndex).trim();
        cleanText = message.text.substring(0, startIndex).trim();
      }
    }

    return FadeInUp(
      duration: const Duration(milliseconds: 400),
      child: Padding(
        padding: const EdgeInsets.only(bottom: 15),
        child: Column(
          crossAxisAlignment: message.isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: message.isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
              children: [
                if (!message.isUser)
                  const CircleAvatar(
                    radius: 15,
                    backgroundColor: Color(0xFFEBF2FF),
                    child: Icon(Icons.smart_toy_rounded, size: 18, color: Color(0xFF2563EB)),
                  ),
                const SizedBox(width: 10),
                Flexible(
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    decoration: BoxDecoration(
                      color: message.isUser ? const Color(0xFF2563EB) : Colors.white,
                      borderRadius: BorderRadius.only(
                        topLeft: const Radius.circular(20),
                        topRight: const Radius.circular(20),
                        bottomLeft: Radius.circular(message.isUser ? 20 : 0),
                        bottomRight: Radius.circular(message.isUser ? 0 : 20),
                      ),
                      boxShadow: [
                        BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 5, offset: const Offset(0, 2)),
                      ],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        if (cleanText.isNotEmpty)
                          Text(
                            cleanText,
                            style: GoogleFonts.inter(
                              color: message.isUser ? Colors.white : const Color(0xFF1E293B),
                              fontWeight: FontWeight.w500,
                              height: 1.4,
                            ),
                          ),
                        if (hasLink && link != null) ...[
                          if (cleanText.isNotEmpty) const SizedBox(height: 12),
                          InkWell(
                            onTap: () => _launchURL(link!),
                            child: Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: const Color(0xFFF8FAFC),
                                borderRadius: BorderRadius.circular(12),
                                border: Border.all(color: const Color(0xFFE2E8F0)),
                              ),
                              child: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  const Icon(Icons.picture_as_pdf_rounded, color: Colors.redAccent, size: 28),
                                  const SizedBox(width: 12),
                                  Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        "Official_Outpass.pdf",
                                        style: GoogleFonts.inter(fontSize: 13, fontWeight: FontWeight.w700, color: const Color(0xFF1E293B)),
                                      ),
                                      Text(
                                        "Tap to open document",
                                        style: GoogleFonts.inter(fontSize: 11, color: const Color(0xFF64748B)),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(width: 8),
                                  const Icon(Icons.download_rounded, color: Color(0xFF2563EB), size: 20),
                                ],
                              ),
                            ),
                          ),
                        ]
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                if (message.isUser)
                  const CircleAvatar(
                    radius: 15,
                    backgroundColor: Color(0xFFF1F5F9),
                    child: Icon(Icons.person_outline_rounded, size: 18, color: Color(0xFF64748B)),
                  ),
              ],
            ),
            Padding(
              padding: const EdgeInsets.only(top: 5, left: 45, right: 45),
              child: Text(
                "${message.time.hour}:${message.time.minute.toString().padLeft(2, '0')}",
                style: GoogleFonts.inter(fontSize: 10, color: const Color(0xFF94A3B8)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInputArea() {
    return Container(
      padding: const EdgeInsets.fromLTRB(20, 10, 20, 30),
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.only(topLeft: Radius.circular(30), topRight: Radius.circular(30)),
      ),
      child: Row(
        children: [
          Expanded(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              decoration: BoxDecoration(
                color: const Color(0xFFF1F5F9),
                borderRadius: BorderRadius.circular(20),
              ),
              child: TextField(
                controller: _controller,
                onSubmitted: (_) => _sendMessage(),
                decoration: InputDecoration(
                  hintText: "Ask anything about your campus...",
                  hintStyle: GoogleFonts.inter(color: const Color(0xFF94A3B8), fontSize: 14),
                  border: InputBorder.none,
                ),
              ),
            ),
          ),
          const SizedBox(width: 10),
          GestureDetector(
            onTap: _sendMessage,
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: const BoxDecoration(color: Color(0xFF2563EB), shape: BoxShape.circle),
              child: const Icon(Icons.send_rounded, color: Colors.white, size: 24),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _launchURL(String url) async {
    final Uri uri = Uri.parse(url);
    if (!await launchUrl(uri, mode: LaunchMode.externalApplication)) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Could not open download link.")));
    }
  }
}

class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime time;

  ChatMessage({required this.text, required this.isUser, required this.time});
}