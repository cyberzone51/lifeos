/// Telegram Service — интеграция с Telegram Mini App SDK.

import 'dart:async';
import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

class TelegramService {
  final Dio _dio;
  String? _accessToken;
  String? _userId;
  bool _isInitialized = false;

  TelegramService({String baseUrl = 'http://localhost:8000'})
      : _dio = Dio(BaseOptions(
          baseUrl: baseUrl,
          connectTimeout: const Duration(seconds: 5),
          receiveTimeout: const Duration(seconds: 10),
        ));

  bool get isInitialized => _isInitialized;
  bool get isAuthenticated => _accessToken != null;
  String? get userId => _userId;

  /// Initialize Telegram Mini App
  Future<void> init() async {
    // Load saved token
    final prefs = await SharedPreferences.getInstance();
    _accessToken = prefs.getString('telegram_access_token');
    _userId = prefs.getString('telegram_user_id');

    if (_accessToken != null) {
      _dio.options.headers['Authorization'] = 'Bearer $_accessToken';
      _isInitialized = true;
    }
  }

  /// Authenticate with Telegram
  Future<bool> authenticate(String initData) async {
    try {
      final response = await _dio.post(
        '/api/v1/telegram/auth',
        data: {
          'init_data': initData,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data;
        _accessToken = data['access_token'];
        _userId = data['user_id'];

        // Save to storage
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('telegram_access_token', _accessToken!);
        await prefs.setString('telegram_user_id', _userId!);

        // Set auth header
        _dio.options.headers['Authorization'] = 'Bearer $_accessToken';

        _isInitialized = true;
        return true;
      }
      return false;
    } catch (e) {
      print('Telegram auth error: $e');
      return false;
    }
  }

  /// Get user info from Telegram WebApp
  Map<String, dynamic>? getTelegramUser() {
    // In actual Telegram Mini App, this would access window.Telegram.WebApp
    // For web, we return mock data
    return null;
  }

  /// Send data to bot
  void sendData(String data) {
    // In Telegram Mini App, this would use WebApp.sendData()
    print('Sending data to bot: $data');
  }

  /// Close Mini App
  void close() {
    // WebApp.close()
    print('Closing Mini App');
  }

  /// Get init data from URL or Telegram
  String getInitData() {
    // In production, this comes from Telegram
    // For development, we mock it
    return 'mock_init_data';
  }

  /// Logout
  Future<void> logout() async {
    _accessToken = null;
    _userId = null;
    _isInitialized = false;

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('telegram_access_token');
    await prefs.remove('telegram_user_id');

    _dio.options.headers.remove('Authorization');
  }

  /// Make authenticated API call
  Future<Response> apiGet(String path, {Map<String, dynamic>? params}) {
    return _dio.get(path, queryParameters: params);
  }

  /// Make authenticated POST
  Future<Response> apiPost(String path, {dynamic data}) {
    return _dio.post(path, data: data);
  }
}

// Singleton
final telegramService = TelegramService();
