import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'splash_screen.dart';
import 'auth_screen.dart';
import 'main_scaffold.dart';

void main() async {
  // 1. Ensure Flutter is ready
  WidgetsFlutterBinding.ensureInitialized();
  
  // 2. Check for existing session
  final prefs = await SharedPreferences.getInstance();
  final String? token = prefs.getString('token');
  final String? name = prefs.getString('name');
  
  runApp(MyApp(initialToken: token, initialName: name));
}

class MyApp extends StatelessWidget {
  final String? initialToken;
  final String? initialName;
  
  const MyApp({super.key, this.initialToken, this.initialName});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CampusConnect',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF2563EB)),
        useMaterial3: true,
        textTheme: GoogleFonts.interTextTheme(),
      ),
      // If we have a token, start at splash (for logo feel) but it will skip to home
      home: SplashScreen(startToken: initialToken, startName: initialName),
      onGenerateRoute: (settings) {
        if (settings.name == '/home') {
          final args = settings.arguments as Map?;
          return MaterialPageRoute(
            builder: (context) => MainScaffold(
              name: args?['name'] ?? 'Student',
              token: args?['token'] ?? '',
            ),
          );
        }
        if (settings.name == '/auth') {
          return MaterialPageRoute(builder: (context) => const AuthScreen());
        }
        return null;
      },
      routes: {
        '/auth': (context) => const AuthScreen(),
      },
    );
  }
}