import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:animate_do/animate_do.dart';

class SplashScreen extends StatefulWidget {
  final String? startToken;
  final String? startName;
  const SplashScreen({super.key, this.startToken, this.startName});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _startNavigation();
  }

  void _startNavigation() {
    Future.delayed(const Duration(seconds: 3), () {
      if (!mounted) return;
      
      // AUTO-LOGIN LOGIC
      if (widget.startToken != null && widget.startName != null) {
        Navigator.pushReplacementNamed(
          context, 
          '/home', 
          arguments: {'token': widget.startToken, 'name': widget.startName}
        );
      } else {
        Navigator.pushReplacementNamed(context, '/auth');
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SizedBox.expand(
        child: Stack(
          alignment: Alignment.center,
          children: [
            Positioned(
              bottom: -40,
              left: -40,
              child: FadeInUp(
                duration: const Duration(seconds: 1),
                child: Container(
                  width: 180,
                  height: 180,
                  decoration: BoxDecoration(
                    color: const Color(0xFF2563EB).withValues(alpha: 0.05),
                    shape: BoxShape.circle,
                  ),
                ),
              ),
            ),
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ZoomIn(
                  duration: const Duration(milliseconds: 800),
                  child: Container(
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      color: const Color(0xFFEBF2FF),
                      borderRadius: BorderRadius.circular(32),
                    ),
                    child: const Icon(
                      Icons.school_rounded,
                      size: 64,
                      color: Color(0xFF2563EB),
                    ),
                  ),
                ),
                const SizedBox(height: 32),
                FadeInUp(
                  duration: const Duration(milliseconds: 600),
                  delay: const Duration(milliseconds: 400),
                  child: Text(
                    'CampusConnect',
                    style: GoogleFonts.inter(
                      fontSize: 32,
                      fontWeight: FontWeight.w900,
                      color: const Color(0xFF1E293B),
                      letterSpacing: -0.5,
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                FadeInUp(
                  duration: const Duration(milliseconds: 600),
                  delay: const Duration(milliseconds: 600),
                  child: Text(
                    'Precision Student Management',
                    style: GoogleFonts.inter(
                      fontSize: 14,
                      fontWeight: FontWeight.w500,
                      color: const Color(0xFF64748B),
                    ),
                  ),
                ),
                const SizedBox(height: 64),
                FadeIn(
                  delay: const Duration(milliseconds: 1200),
                  child: const SizedBox(
                    width: 48,
                    child: LinearProgressIndicator(
                      backgroundColor: Color(0xFFF1F5F9),
                      color: Color(0xFF2563EB),
                      minHeight: 2,
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}