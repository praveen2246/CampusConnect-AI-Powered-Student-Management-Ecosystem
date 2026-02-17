import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'config.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:animate_do/animate_do.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ProfileScreen extends StatefulWidget {
  final String token;
  const ProfileScreen({super.key, required this.token});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  bool isEditing = false;
  Map<String, dynamic> profile = {};
  final _formKey = GlobalKey<FormState>();
  bool _isLoading = true;

  final fields = [
    {"key": "Roll No.", "icon": Icons.assignment_ind_rounded},
    {"key": "Name", "icon": Icons.person_rounded},
    {"key": "Gender", "icon": Icons.transgender_rounded},
    {"key": "Date of Birth", "icon": Icons.cake_rounded},
    {"key": "Address", "icon": Icons.home_rounded},
    {"key": "City", "icon": Icons.location_city_rounded},
    {"key": "Pincode", "icon": Icons.pin_drop_rounded},
    {"key": "District", "icon": Icons.map_rounded},
  ];

  @override
  void initState() {
    super.initState();
    _fetchProfile();
  }

  Future<void> _fetchProfile() async {
    try {
      final response = await http.get(
        Uri.parse(AppConfig.profileUrl),
        headers: {'Authorization': widget.token},
      );
      final data = jsonDecode(response.body);
      setState(() {
        profile = data['profile'] ?? {};
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _saveProfile() async {
    if (!_formKey.currentState!.validate()) return;
    _formKey.currentState!.save();
    
    setState(() => _isLoading = true);
    
    try {
      final response = await http.post(
        Uri.parse(AppConfig.profileUrl),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': widget.token,
        },
        body: jsonEncode(profile),
      );
      if (response.statusCode == 200) {
        setState(() {
          isEditing = false;
          _isLoading = false;
        });
        _fetchProfile();
      }
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    if (!mounted) return;
    Navigator.pushNamedAndRemoveUntil(context, '/auth', (route) => false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: Text('Student Profile', style: GoogleFonts.inter(fontWeight: FontWeight.w800)),
        backgroundColor: Colors.white,
        elevation: 0,
        foregroundColor: const Color(0xFF1E293B),
        actions: [
          IconButton(
            icon: Icon(isEditing ? Icons.check_circle_rounded : Icons.edit_rounded, 
                 color: isEditing ? Colors.green : const Color(0xFF2563EB)),
            onPressed: () {
              if (isEditing) {
                _saveProfile();
              } else {
                setState(() => isEditing = true);
              }
            },
          ),
          IconButton(
            icon: const Icon(Icons.logout_rounded, color: Colors.redAccent),
            onPressed: _logout,
          ),
        ],
      ),
      body: _isLoading 
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: Form(
                key: _formKey,
                child: Column(
                  children: [
                    FadeInDown(
                      child: Center(
                        child: Stack(
                          children: [
                            Container(
                              width: 100,
                              height: 100,
                              decoration: BoxDecoration(
                                color: const Color(0xFFE2E8F0),
                                shape: BoxShape.circle,
                                border: Border.all(color: Colors.white, width: 4),
                                boxShadow: [
                                  BoxShadow(color: Colors.black.withValues(alpha: 0.1), blurRadius: 10)
                                ]
                              ),
                              child: const Icon(Icons.person, size: 50, color: Color(0xFF64748B)),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 30),
                    ...fields.map((field) {
                      return FadeInUp(
                        duration: const Duration(milliseconds: 400),
                        child: Padding(
                          padding: const EdgeInsets.only(bottom: 16),
                          child: TextFormField(
                            initialValue: profile[field['key']] ?? '',
                            enabled: isEditing,
                            style: GoogleFonts.inter(fontWeight: FontWeight.w600),
                            decoration: InputDecoration(
                              labelText: field['key'] as String,
                              prefixIcon: Icon(field['icon'] as IconData, color: const Color(0xFF64748B)),
                              filled: true,
                              fillColor: isEditing ? Colors.white : const Color(0xFFF1F5F9),
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(16),
                                borderSide: BorderSide.none,
                              ),
                              enabledBorder: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(16),
                                borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
                              ),
                              focusedBorder: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(16),
                                borderSide: const BorderSide(color: Color(0xFF2563EB), width: 2),
                              ),
                            ),
                            onSaved: (val) => profile[field['key'] as String] = val ?? '',
                          ),
                        ),
                      );
                    }),
                  ],
                ),
              ),
            ),
    );
  }
}