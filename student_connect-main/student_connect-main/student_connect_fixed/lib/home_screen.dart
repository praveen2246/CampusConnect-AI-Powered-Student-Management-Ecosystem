import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:animate_do/animate_do.dart';

class HomeScreen extends StatelessWidget {
  final String name;
  final String token;
  const HomeScreen({super.key, required this.name, required this.token});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      body: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: Container(
              padding: const EdgeInsets.fromLTRB(25, 60, 25, 30),
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(40),
                  bottomRight: Radius.circular(40),
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  FadeInDown(
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              "Hello,",
                              style: GoogleFonts.inter(
                                fontSize: 16,
                                color: const Color(0xFF64748B),
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                            Text(
                              name,
                              style: GoogleFonts.inter(
                                fontSize: 24,
                                fontWeight: FontWeight.w900,
                                color: const Color(0xFF1E293B),
                              ),
                            ),
                          ],
                        ),
                        Container(
                          padding: const EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            color: const Color(0xFF2563EB).withValues(alpha: 0.1),
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(Icons.notifications_none_rounded, color: Color(0xFF2563EB)),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 30),
                  FadeInUp(
                    delay: const Duration(milliseconds: 200),
                    child: Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(25),
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [Color(0xFF2563EB), Color(0xFF3B82F6)],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                        borderRadius: BorderRadius.circular(30),
                        boxShadow: [
                          BoxShadow(
                            color: const Color(0xFF2563EB).withValues(alpha: 0.3),
                            blurRadius: 20,
                            offset: const Offset(0, 10),
                          ),
                        ],
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            "Campus AI Assistant",
                            style: GoogleFonts.inter(
                              color: Colors.white.withValues(alpha: 0.8),
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          const SizedBox(height: 10),
                          Text(
                            "How can I help you\ntoday, $name?",
                            style: GoogleFonts.inter(
                              color: Colors.white,
                              fontSize: 20,
                              fontWeight: FontWeight.w800,
                              height: 1.2,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          
          SliverPadding(
            padding: const EdgeInsets.all(25),
            sliver: SliverGrid(
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                mainAxisSpacing: 20,
                crossAxisSpacing: 20,
                childAspectRatio: 1,
              ),
              delegate: SliverChildListDelegate([
                _buildMenuCard(
                  title: "Outpass",
                  icon: Icons.assignment_turned_in_rounded,
                  color: const Color(0xFF8B5CF6),
                  delay: 400,
                ),
                _buildMenuCard(
                  title: "Attendance",
                  icon: Icons.calendar_today_rounded,
                  color: const Color(0xFFF59E0B),
                  delay: 600,
                ),
                _buildMenuCard(
                  title: "Courses",
                  icon: Icons.menu_book_rounded,
                  color: const Color(0xFF10B981),
                  delay: 800,
                ),
                _buildMenuCard(
                  title: "Profile",
                  icon: Icons.person_rounded,
                  color: const Color(0xFFEF4444),
                  delay: 1000,
                ),
              ]),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMenuCard({
    required String title,
    required IconData icon,
    required Color color,
    required int delay,
  }) {
    return FadeInUp(
      delay: Duration(milliseconds: delay),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(30),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.03),
              blurRadius: 10,
              offset: const Offset(0, 5),
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                color: color.withValues(alpha: 0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: color, size: 30),
            ),
            const SizedBox(height: 15),
            Text(
              title,
              style: GoogleFonts.inter(
                fontWeight: FontWeight.w700,
                color: const Color(0xFF1E293B),
              ),
            ),
          ],
        ),
      ),
    );
  }
}