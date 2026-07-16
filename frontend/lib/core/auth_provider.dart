/// Auth Provider — управление состоянием авторизации.

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lifeos/core/telegram_service.dart';

/// Auth state
class AuthState {
  final bool isLoading;
  final bool isAuthenticated;
  final String? userId;
  final String? error;

  const AuthState({
    this.isLoading = false,
    this.isAuthenticated = false,
    this.userId,
    this.error,
  });

  AuthState copyWith({
    bool? isLoading,
    bool? isAuthenticated,
    String? userId,
    String? error,
  }) {
    return AuthState(
      isLoading: isLoading ?? this.isLoading,
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      userId: userId ?? this.userId,
      error: error,
    );
  }
}

/// Auth notifier
class AuthNotifier extends StateNotifier<AuthState> {
  final TelegramService _telegramService;

  AuthNotifier(this._telegramService) : super(const AuthState()) {
    _init();
  }

  Future<void> _init() async {
    state = state.copyWith(isLoading: true);
    await _telegramService.init();
    
    state = state.copyWith(
      isLoading: false,
      isAuthenticated: _telegramService.isAuthenticated,
      userId: _telegramService.userId,
    );
  }

  Future<bool> login(String initData) async {
    state = state.copyWith(isLoading: true, error: null);
    
    final success = await _telegramService.authenticate(initData);
    
    if (success) {
      state = state.copyWith(
        isLoading: false,
        isAuthenticated: true,
        userId: _telegramService.userId,
      );
      return true;
    } else {
      state = state.copyWith(
        isLoading: false,
        error: 'Authentication failed',
      );
      return false;
    }
  }

  Future<void> logout() async {
    await _telegramService.logout();
    state = const AuthState();
  }
}

/// Auth provider
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(telegramService);
});

/// Auth state selector
final isAuthenticatedProvider = Provider<bool>((ref) {
  return ref.watch(authProvider).isAuthenticated;
});
