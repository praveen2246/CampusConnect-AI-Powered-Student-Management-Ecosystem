import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:google_fonts/google_fonts.dart';
import 'package:animate_do/animate_do.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'config.dart';

class AuthScreen extends StatefulWidget {
  const AuthScreen({super.key});

  @override
  State<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  bool isLogin = true;
  bool _isLoading = false;
  bool _obscurePassword = true;
  final _formKey = GlobalKey<FormState>();
  
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _nameController = TextEditingController();
  
  String _errorMessage = '';

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
      _errorMessage = '';
    });

    final String url = isLogin ? AppConfig.loginUrl : AppConfig.signupUrl;
    
    final body = isLogin
        ? {
            'email': _emailController.text.trim(),
            'password': _passwordController.text.trim()
          }
        : {
            'name': _nameController.text.trim(),
            'email': _emailController.text.trim(),
            'password': _passwordController.text.trim()
          };

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );

      final data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        if (isLogin) {
          // SAVE SESSION
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString('token', data['token']);
          await prefs.setString('name', data['name']);

          if (!mounted) return;
          Navigator.pushReplacementNamed(
            context, 
            '/home',
            arguments: {'token': data['token'], 'name': data['name']},
          );
        } else {
          setState(() {
            isLogin = true;
            _isLoading = false;
          });
          if (!mounted) return;
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Registration successful! Please login.')),
          );
        }
      } else {
        setState(() {
          _errorMessage = data['error'] ?? 'Authentication failed';
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Connection error. Please check your server.';
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    
    return Scaffold(
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        child: Container(
          constraints: BoxConstraints(minHeight: size.height),
          child: Stack(
            children: [
              // Decorative background elements
              Positioned(
                top: -size.height * 0.1,
                right: -size.width * 0.2,
                child: FadeInDown(
                  child: Container(
                    width: size.width * 0.8,
                    height: size.width * 0.8,
                    decoration: BoxDecoration(
                      color: const Color(0xFF2563EB).withOpacity(0.08),
                      shape: BoxShape.circle,
                    ),
                  ),
                ),
              ),
              
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 30),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    SizedBox(height: size.height * 0.12),
                    
                    FadeInDown(
                      duration: const Duration(milliseconds: 800),
                      child: Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: const Color(0xFF2563EB).withOpacity(0.1),
                          borderRadius: BorderRadius.circular(15),
                        ),
                        child: const Icon(Icons.school_rounded, color: Color(0xFF2563EB), size: 30),
                      ),
                    ),
                    
                    const SizedBox(height: 25),
                    
                    FadeInDown(
                      duration: const Duration(milliseconds: 1000),
                      child: Text(
                        isLogin ? "Welcome\nBack!" : "Create\nAccount",
                        style: GoogleFonts.inter(
                          fontSize: 36,
                          fontWeight: FontWeight.w900,
                          color: const Color(0xFF1E293B),
                          height: 1.1,
                        ),
                      ),
                    ),
                    
                    const SizedBox(height: 40),
                    
                    Form(
                      key: _formKey,
                      child: Column(
                        children: [
                          if (!isLogin) 
                            FadeInUp(
                              duration: const Duration(milliseconds: 400),
                              child: _buildTextField(
                                controller: _nameController,
                                label: "Full Name",
                                icon: Icons.person_outline,
                                validator: (v) => v!.isEmpty ? "Required" : null,
                              ),
                            ),
                          
                          const SizedBox(height: 18),
                          FadeInUp(
                            duration: const Duration(milliseconds: 600),
                            child: _buildTextField(
                              controller: _emailController,
                              label: "Student Email",
                              icon: Icons.alternate_email_rounded,
                              keyboardType: TextInputType.emailAddress,
                              validator: (v) => v!.isEmpty || !v.contains("@") ? "Invalid email" : null,
                            ),
                          ),
                          
                          const SizedBox(height: 18),
                          FadeInUp(
                            duration: const Duration(milliseconds: 800),
                            child: _buildTextField(
                              controller: _passwordController,
                              label: "Password",
                              icon: Icons.lock_open_rounded,
                              isPassword: true,
                              obscureText: _obscurePassword,
                              onTogglePassword: () => setState(() => _obscurePassword = !_obscurePassword),
                              validator: (v) => v!.length < 6 ? "Min 6 chars" : null,
                            ),
                          ),
                        ],
                      ),
                    ),
                    
                    if (_errorMessage.isNotEmpty)
                      Padding(
                        padding: const EdgeInsets.only(top: 15),
                        child: FadeIn(
                          child: Text(
                            _errorMessage,
                            style: GoogleFonts.inter(color: Colors.redAccent, fontSize: 13, fontWeight: FontWeight.w600),
                          ),
                        ),
                      ),
                    
                    const SizedBox(height: 35),
                    
                    FadeInUp(
                      duration: const Duration(milliseconds: 1000),
                      child: SizedBox(
                        width: double.infinity,
                        height: 56,
                        child: ElevatedButton(
                          onPressed: _isLoading ? null : _submit,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF2563EB),
                            foregroundColor: Colors.white,
                            elevation: 8,
                            shadowColor: const Color(0xFF2563EB).withOpacity(0.4),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(16),
                            ),
                          ),
                          child: _isLoading 
                            ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                            : Text(
                                isLogin ? "Sign In" : "Get Started",
                                style: GoogleFonts.inter(
                                  fontSize: 18,
                                  fontWeight: FontWeight.w700,
                                ),
                              ),
                        ),
                      ),
                    ),
                    
                    const SizedBox(height: 25),
                    
                    FadeInUp(
                      duration: const Duration(milliseconds: 1200),
                      child: Center(
                        child: GestureDetector(
                          onTap: () => setState(() {
                            isLogin = !isLogin;
                            _errorMessage = '';
                          }),
                          child: RichText(
                            text: TextSpan(
                              style: GoogleFonts.inter(color: const Color(0xFF64748B), fontSize: 14),
                              children: [
                                TextSpan(text: isLogin ? "Don't have an account? " : "Already a member? "),
                                TextSpan(
                                  text: isLogin ? "Sign Up" : "Login",
                                  style: const TextStyle(color: Color(0xFF2563EB), fontWeight: FontWeight.w800),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    required IconData icon,
    bool isPassword = false,
    bool obscureText = false,
    VoidCallback? onTogglePassword,
    TextInputType? keyboardType,
    String? Function(String?)? validator,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFFF1F5F9),
        borderRadius: BorderRadius.circular(16),
      ),
      child: TextFormField(
        controller: controller,
        obscureText: obscureText,
        keyboardType: keyboardType,
        validator: validator,
        style: GoogleFonts.inter(fontWeight: FontWeight.w600, color: const Color(0xFF0F172A)),
        decoration: InputDecoration(
          prefixIcon: Icon(icon, color: const Color(0xFF64748B), size: 20),
          suffixIcon: isPassword 
              ? IconButton(
                  icon: Icon(
                    obscureText ? Icons.visibility_off_rounded : Icons.visibility_rounded,
                    color: const Color(0xFF64748B),
                    size: 20,
                  ),
                  onPressed: onTogglePassword,
                )
              : null,
          hintText: label,
          hintStyle: GoogleFonts.inter(color: const Color(0xFF94A3B8), fontWeight: FontWeight.w500, fontSize: 14),
          border: InputBorder.none,
          contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        ),
      ),
    );
  }
}