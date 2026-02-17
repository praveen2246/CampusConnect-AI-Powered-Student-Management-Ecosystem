import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'config.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:animate_do/animate_do.dart';
import 'package:url_launcher/url_launcher.dart';

class OutpassScreen extends StatefulWidget {
  final String token;
  const OutpassScreen({super.key, required this.token});

  @override
  State<OutpassScreen> createState() => _OutpassScreenState();
}

class _OutpassScreenState extends State<OutpassScreen> {
  List<dynamic> outpasses = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchOutpasses();
  }

  Future<void> fetchOutpasses() async {
    try {
      final response = await http.get(
        Uri.parse(AppConfig.myOutpasses),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${widget.token}',
        },
      );
      if (response.statusCode == 200) {
        if (mounted) {
          setState(() {
            outpasses = jsonDecode(response.body);
            isLoading = false;
          });
        }
      }
    } catch (e) {
      if (mounted) setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: Text('Status Center', style: GoogleFonts.inter(fontWeight: FontWeight.w800)),
        backgroundColor: Colors.white,
        elevation: 0,
        foregroundColor: const Color(0xFF1E293B),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh_rounded),
            onPressed: fetchOutpasses,
          )
        ],
      ),
      body: isLoading 
          ? const Center(child: CircularProgressIndicator())
          : outpasses.isEmpty 
              ? _buildEmptyState()
              : SingleChildScrollView(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Padding(
                        padding: const EdgeInsets.fromLTRB(24, 20, 24, 0),
                        child: Text(
                          "Active Applications",
                          style: GoogleFonts.inter(fontSize: 14, fontWeight: FontWeight.w600, color: const Color(0xFF64748B)),
                        ),
                      ),
                      ListView.builder(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        padding: const EdgeInsets.all(20),
                        itemCount: outpasses.length,
                        itemBuilder: (ctx, i) => FadeInUp(
                          duration: Duration(milliseconds: 300 + (i * 100)),
                          child: _buildOutpassCard(outpasses[i]),
                        ),
                      ),
                    ],
                  ),
                ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {}, // Redirect to chatbot or show dialog
        backgroundColor: const Color(0xFF2563EB),
        icon: const Icon(Icons.add_rounded),
        label: const Text("New Request"),
      ),
    );
  }

  String _formatDate(dynamic date) {
    if (date == null) return 'N/A';
    String dateStr = date.toString();
    if (dateStr.length < 10) return dateStr;
    return dateStr.substring(0, 10);
  }

  Widget _buildOutpassCard(dynamic item) {
    try {
      final status = (item['status'] ?? 'PENDING') as String;
      Color statusColor = const Color(0xFF64748B);
      IconData statusIcon = Icons.hourglass_empty_rounded;

      if (status == 'APPROVED') {
        statusColor = Colors.green;
        statusIcon = Icons.check_circle_rounded;
      } else if (status == 'REJECTED') {
        statusColor = Colors.redAccent;
        statusIcon = Icons.cancel_rounded;
      }

      return Container(
        margin: const EdgeInsets.only(bottom: 20),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(24),
          boxShadow: [
            BoxShadow(color: Colors.black.withValues(alpha: 0.04), blurRadius: 10, offset: const Offset(0, 4))
          ],
        ),
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: const Color(0xFF2563EB).withValues(alpha: 0.1),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          (item['type'] ?? 'OUTPASS').toString().toUpperCase(),
                          style: GoogleFonts.inter(
                            color: const Color(0xFF2563EB),
                            fontWeight: FontWeight.w800,
                            fontSize: 10,
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: statusColor.withValues(alpha: 0.1),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Row(
                          children: [
                            Icon(statusIcon, size: 12, color: statusColor),
                            const SizedBox(width: 4),
                            Text(
                              status,
                              style: GoogleFonts.inter(
                                color: statusColor,
                                fontWeight: FontWeight.w700,
                                fontSize: 10,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  Text(
                    _formatDate(item['date_from']),
                    style: GoogleFonts.inter(color: const Color(0xFF94A3B8), fontSize: 11, fontWeight: FontWeight.w600),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              Text(
                item['reason'] ?? 'No Reason Specified',
                style: GoogleFonts.inter(fontSize: 18, fontWeight: FontWeight.w800, color: const Color(0xFF1E293B)),
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  const Icon(Icons.calendar_month_rounded, size: 16, color: Color(0xFF64748B)),
                  const SizedBox(width: 8),
                  Text(
                    "${item['date_from'] ?? 'N/A'} to ${item['date_to'] ?? 'N/A'}",
                    style: GoogleFonts.inter(color: const Color(0xFF64748B), fontWeight: FontWeight.w500),
                  ),
                ],
              ),
              if (status == 'APPROVED') ...[
                const SizedBox(height: 16),
                const Divider(color: Color(0xFFF1F5F9)),
                const SizedBox(height: 8),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: () => _downloadOutpass(item['_id']),
                    icon: const Icon(Icons.download_rounded, size: 18),
                    label: const Text("Download"),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF2563EB),
                      foregroundColor: Colors.white,
                      elevation: 0,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      padding: const EdgeInsets.symmetric(vertical: 12),
                    ),
                  ),
                ),
              ],
            ],
          ),
        ),
      );
    } catch (e) {
      debugPrint("Error building outpass card: $e");
      return const SizedBox.shrink();
    }
  }

  Future<void> _downloadOutpass(String id) async {
    final url = "${AppConfig.baseUrl}/outpass/download/$id";
    final Uri uri = Uri.parse(url);
    if (!await launchUrl(uri, mode: LaunchMode.externalApplication)) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Could not open download link.")));
      }
    }
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.assignment_late_rounded, size: 80, color: Color(0xFFE2E8F0)),
          const SizedBox(height: 20),
          Text(
            "No Records Found",
            style: GoogleFonts.inter(fontSize: 18, fontWeight: FontWeight.w700, color: const Color(0xFF94A3B8)),
          ),
        ],
      ),
    );
  }
}
