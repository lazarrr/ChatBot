import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiClient {
  static const String _baseUrl = 'http://localhost:8080';

  final Map<String, String> _defaultHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  /// GET request
  Future<dynamic> get(String endpoint, {Map<String, String>? headers}) async {
    final uri = Uri.parse('$_baseUrl$endpoint');

    final response = await http.get(
      uri,
      headers: {..._defaultHeaders, ...?headers},
    );

    return _handleResponse(response);
  }

  /// POST request
  Future<dynamic> post(String endpoint,
      {Map<String, String>? headers, dynamic body}) async {
    final uri = Uri.parse('$_baseUrl$endpoint');

    final response = await http.post(
      uri,
      headers: {..._defaultHeaders, ...?headers},
      body: body != null ? jsonEncode(body) : null,
    );

    return _handleResponse(response);
  }

  /// Common response handler
  dynamic _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (response.body.isEmpty) return null;
      return jsonDecode(response.body);
    } else {
      throw ApiException(
        statusCode: response.statusCode,
        message: response.body,
      );
    }
  }
}

class ApiException implements Exception {
  final int statusCode;
  final String message;

  ApiException({required this.statusCode, required this.message});

  @override
  String toString() => 'ApiException ($statusCode): $message';
}
