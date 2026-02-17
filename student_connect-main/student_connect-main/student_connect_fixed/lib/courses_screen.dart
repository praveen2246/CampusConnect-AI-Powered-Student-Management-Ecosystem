import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:animate_do/animate_do.dart';

class CoursesScreen extends StatelessWidget {
  const CoursesScreen({super.key});

  final List<Map<String, dynamic>> courses = const [
    {"name": "Data Structures", "code": "CS301", "credits": 4, "progress": 0.85, "color": Color(0xFF2563EB)},
    {"name": "Software Engineering", "code": "CS302", "credits": 3, "progress": 0.70, "color": Color(0xFF8B5CF6)},
    {"name": "Database Management", "code": "CS303", "credits": 4, "progress": 0.45, "color": Color(0xFF10B981)},
    {"name": "Computer Networks", "code": "CS304", "credits": 3, "progress": 0.60, "color": Color(0xFFF59E0B)},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: Text('Academic Courses', style: GoogleFonts.inter(fontWeight: FontWeight.w800)),
        backgroundColor: Colors.white,
        elevation: 0,
        foregroundColor: const Color(0xFF1E293B),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            FadeInDown(
              child: Text(
                "Active Semester",
                style: GoogleFonts.inter(fontSize: 14, fontWeight: FontWeight.w600, color: const Color(0xFF64748B)),
              ),
            ),
            FadeInDown(
              child: Text(
                "Fall 2026 - Year 3",
                style: GoogleFonts.inter(fontSize: 22, fontWeight: FontWeight.w800, color: const Color(0xFF1E293B)),
              ),
            ),
            const SizedBox(height: 30),
            ...courses.asMap().entries.map((entry) {
              int i = entry.key;
              var course = entry.value;
              return FadeInUp(
                duration: Duration(milliseconds: 300 + (i * 100)),
                child: _buildCourseCard(course),
              );
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildCourseCard(Map<String, dynamic> course) {
    return Container(
      margin: const EdgeInsets.only(bottom: 20),
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 10, offset: const Offset(0, 4))
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: (course['color'] as Color).withOpacity(0.1),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Icon(Icons.book_rounded, color: course['color'] as Color, size: 24),
              ),
              Text(
                course['code'] as String,
                style: GoogleFonts.inter(fontWeight: FontWeight.w700, color: const Color(0xFF94A3B8), fontSize: 12),
              ),
            ],
          ),
          const SizedBox(height: 20),
          Text(
            course['name'] as String,
            style: GoogleFonts.inter(fontSize: 18, fontWeight: FontWeight.w800, color: const Color(0xFF1E293B)),
          ),
          const SizedBox(height: 8),
          Text(
            "${course['credits']} Credits",
            style: GoogleFonts.inter(color: const Color(0xFF64748B), fontWeight: FontWeight.w600, fontSize: 13),
          ),
          const SizedBox(height: 20),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                "Completion",
                style: GoogleFonts.inter(fontSize: 12, fontWeight: FontWeight.w600, color: const Color(0xFF64748B)),
              ),
              Text(
                "${((course['progress'] as double) * 100).toInt()}%",
                style: GoogleFonts.inter(fontSize: 12, fontWeight: FontWeight.w700, color: course['color'] as Color),
              ),
            ],
          ),
          const SizedBox(height: 8),
          ClipRRect(
            borderRadius: BorderRadius.circular(10),
            child: LinearProgressIndicator(
              value: course['progress'] as double,
              backgroundColor: const Color(0xFFF1F5F9),
              color: course['color'] as Color,
              minHeight: 8,
            ),
          ),
        ],
      ),
    );
  }
}