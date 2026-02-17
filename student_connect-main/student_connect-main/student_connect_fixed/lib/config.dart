class AppConfig {
  // API Base URL - Change based on your environment
  
  // For Web (Chrome/Edge) or Windows Desktop
  static const String baseUrl = 'http://localhost:8000';

  // For Android Emulator (alternative)
  // static const String baseUrl = 'http://10.0.2.2:8000';
  
  // API Endpoints
  static const String loginUrl = '$baseUrl/login';
  static const String signupUrl = '$baseUrl/signup';
  static const String chatUrl = '$baseUrl/chat';
  static const String conversationsUrl = '$baseUrl/conversations';
  static const String profileUrl = '$baseUrl/profile';
  
  static String conversationUrl(String name) => '$baseUrl/conversation/$name';
  static const String renameConversationUrl = '$baseUrl/rename_conversation';
  static const String outpassRequest = '$baseUrl/outpass/request';
  static const String myOutpasses = '$baseUrl/outpass/my';
}
