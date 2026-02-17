import 'package:flutter/material.dart';
import 'package:google_nav_bar/google_nav_bar.dart';
import 'home_screen.dart';
import 'chatbot_screen.dart';
import 'courses_screen.dart';
import 'outpass_screen.dart';
import 'profile_screen.dart';

class MainScaffold extends StatefulWidget {
  final String name;
  final String token;
  const MainScaffold({super.key, required this.name, required this.token});

  @override
  State<MainScaffold> createState() => _MainScaffoldState();
}

class _MainScaffoldState extends State<MainScaffold> {
  int _selectedIndex = 2; // ChatAssist is default

  final List<Color> tabColors = [
    Colors.teal,         // Home
    Colors.orange,       // Courses
    Colors.deepPurple,   // ChatAssist
    Colors.blue,         // Outpass
    Colors.pinkAccent,   // Profile
  ];

  @override
  Widget build(BuildContext context) {
    final List<Widget> actualScreens = [
      HomeScreen(name: widget.name, token: widget.token),
      const CoursesScreen(),
      ChatbotScreen(token: widget.token),
      OutpassScreen(token: widget.token),
      ProfileScreen(token: widget.token), // Pass token here
    ];

    return Scaffold(
      body: actualScreens[_selectedIndex],
      bottomNavigationBar: Container(
        color: Colors.white,
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
        child: GNav(
          gap: 8,
          backgroundColor: Colors.white,
          activeColor: Colors.white,
          color: tabColors[_selectedIndex],
          tabBackgroundColor: tabColors[_selectedIndex],
          tabBorderRadius: 24,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          selectedIndex: _selectedIndex,
          onTabChange: (index) {
            setState(() {
              _selectedIndex = index;
            });
          },
          tabs: [
            GButton(
              icon: Icons.home,
              text: 'Home',
              iconSize: 24,
              backgroundColor: tabColors[0],
            ),
            GButton(
              icon: Icons.book,
              text: 'Courses',
              iconSize: 24,
              backgroundColor: tabColors[1],
            ),
            GButton(
              icon: Icons.chat_bubble,
              text: 'ChatAssist',
              iconSize: 24,
              backgroundColor: tabColors[2],
            ),
            GButton(
              icon: Icons.analytics_rounded, 
              text: 'Status Center',        
              iconSize: 24,
              backgroundColor: tabColors[3],
            ),
            GButton(
              icon: Icons.person,
              text: 'Profile',
              iconSize: 24,
              backgroundColor: tabColors[4],
            ),
          ],
        ),
      ),
    );
  }
}