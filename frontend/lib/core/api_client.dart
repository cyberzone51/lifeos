/// API Client — HTTP клиент для.communication с Backend.

import 'package:dio/dio.dart';

class ApiClient {
  final Dio _dio;
  final String _baseUrl;

  ApiClient({String baseUrl = 'http://localhost:8000'})
      : _baseUrl = baseUrl,
        _dio = Dio(BaseOptions(
          baseUrl: baseUrl,
          connectTimeout: const Duration(seconds: 5),
          receiveTimeout: const Duration(seconds: 10),
          headers: {
            'Content-Type': 'application/json',
          },
        )) {
    _dio.interceptors.add(LogInterceptor(
      requestBody: true,
      responseBody: true,
    ));
  }

  void setToken(String token) {
    _dio.options.headers['Authorization'] = 'Bearer $token';
  }

  void clearToken() {
    _dio.options.headers.remove('Authorization');
  }

  // Auth
  Future<Map<String, dynamic>> telegramLogin({
    required int telegramId,
    required String hash,
    required int authDate,
    String? username,
    String? firstName,
    String? lastName,
    String? photoUrl,
  }) async {
    final response = await _dio.post('/api/v1/auth/telegram', data: {
      'telegram_id': telegramId,
      'hash': hash,
      'auth_date': authDate,
      'username': username,
      'first_name': firstName,
      'last_name': lastName,
      'photo_url': photoUrl,
    });
    return response.data;
  }

  // AI Chat
  Future<Map<String, dynamic>> sendChatMessage({
    required String message,
    String? conversationId,
  }) async {
    final response = await _dio.post('/api/v1/ai/chat', data: {
      'message': message,
      'conversation_id': conversationId,
    });
    return response.data;
  }

  // Finance
  Future<List<dynamic>> getExpenses({
    DateTime? startDate,
    DateTime? endDate,
  }) async {
    final response = await _dio.get('/api/v1/finance/expenses', queryParameters: {
      if (startDate != null) 'start_date': startDate.toIso8601String(),
      if (endDate != null) 'end_date': endDate.toIso8601String(),
    });
    return response.data;
  }

  Future<Map<String, dynamic>> createExpense({
    required double amount,
    required String currencyCode,
    String? categoryId,
    String? description,
    List<String>? tags,
    DateTime? expenseDate,
  }) async {
    final response = await _dio.post('/api/v1/finance/expenses', data: {
      'amount': amount,
      'currency_code': currencyCode,
      'category_id': categoryId,
      'description': description,
      'tags': tags,
      'expense_date': expenseDate?.toIso8601String(),
    });
    return response.data;
  }

  // Tasks
  Future<List<dynamic>> getTasks({String? status}) async {
    final response = await _dio.get('/api/v1/tasks', queryParameters: {
      if (status != null) 'status': status,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> createTask({
    required String title,
    String? description,
    int priority = 2,
    DateTime? dueDate,
    DateTime? reminderAt,
    List<String>? tags,
  }) async {
    final response = await _dio.post('/api/v1/tasks', data: {
      'title': title,
      'description': description,
      'priority': priority,
      'due_date': dueDate?.toIso8601String(),
      'reminder_at': reminderAt?.toIso8601String(),
      'tags': tags,
    });
    return response.data;
  }
}

// Singleton
final apiClient = ApiClient();
