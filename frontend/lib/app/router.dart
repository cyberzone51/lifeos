import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:lifeos/core/auth_provider.dart';
import 'package:lifeos/features/auth/screens/login_screen.dart';
import 'package:lifeos/features/dashboard/screens/dashboard_screen.dart';
import 'package:lifeos/features/ai_chat/screens/chat_screen.dart';
import 'package:lifeos/features/finance/screens/finance_screen.dart';
import 'package:lifeos/features/tasks/screens/tasks_screen.dart';
import 'package:lifeos/features/habits/screens/habits_screen.dart';
import 'package:lifeos/features/health/screens/health_screen.dart';
import 'package:lifeos/features/settings/screens/settings_screen.dart';

final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authProvider);

  return GoRouter(
    initialLocation: '/',
    redirect: (context, state) {
      if (!authState.isAuthenticated && state.uri.toString() != '/login') {
        return '/login';
      }
      if (authState.isAuthenticated && state.uri.toString() == '/login') {
        return '/';
      }
      return null;
    },
    routes: [
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      ShellRoute(
        builder: (context, state, child) {
          return ScaffoldWithNavigation(child: child);
        },
        routes: [
          GoRoute(
            path: '/',
            builder: (context, state) => const DashboardScreen(),
          ),
          GoRoute(
            path: '/chat',
            builder: (context, state) => const ChatScreen(),
          ),
          GoRoute(
            path: '/finance',
            builder: (context, state) => const FinanceScreen(),
          ),
          GoRoute(
            path: '/tasks',
            builder: (context, state) => const TasksScreen(),
          ),
          GoRoute(
            path: '/habits',
            builder: (context, state) => const HabitsScreen(),
          ),
          GoRoute(
            path: '/health',
            builder: (context, state) => const HealthScreen(),
          ),
          GoRoute(
            path: '/settings',
            builder: (context, state) => const SettingsScreen(),
          ),
        ],
      ),
    ],
  );
});

class ScaffoldWithNavigation extends StatelessWidget {
  final Widget child;

  const ScaffoldWithNavigation({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: child,
      bottomNavigationBar: NavigationBar(
        selectedIndex: _getSelectedIndex(context),
        onDestinationSelected: (index) => _onItemTapped(index, context),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: 'Home',
          ),
          NavigationDestination(
            icon: Icon(Icons.chat_outlined),
            selectedIcon: Icon(Icons.chat),
            label: 'AI',
          ),
          NavigationDestination(
            icon: Icon(Icons.account_balance_wallet_outlined),
            selectedIcon: Icon(Icons.account_balance_wallet),
            label: 'Finance',
          ),
          NavigationDestination(
            icon: Icon(Icons.task_outlined),
            selectedIcon: Icon(Icons.task),
            label: 'Tasks',
          ),
          NavigationDestination(
            icon: Icon(Icons.more_horiz),
            selectedIcon: Icon(Icons.more_horiz),
            label: 'More',
          ),
        ],
      ),
    );
  }

  int _getSelectedIndex(BuildContext context) {
    final location = GoRouterState.of(context).uri.toString();
    if (location.startsWith('/chat')) return 1;
    if (location.startsWith('/finance')) return 2;
    if (location.startsWith('/tasks')) return 3;
    if (location.startsWith('/habits') ||
        location.startsWith('/health') ||
        location.startsWith('/settings')) return 4;
    return 0;
  }

  void _onItemTapped(int index, BuildContext context) {
    switch (index) {
      case 0:
        context.go('/');
        break;
      case 1:
        context.go('/chat');
        break;
      case 2:
        context.go('/finance');
        break;
      case 3:
        context.go('/tasks');
        break;
      case 4:
        // Show bottom sheet with more options
        _showMoreOptions(context);
        break;
    }
  }

  void _showMoreOptions(BuildContext context) {
    showModalBottomSheet(
      context: context,
      builder: (context) => Container(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.local_fire_department),
              title: const Text('Habits'),
              onTap: () {
                Navigator.pop(context);
                context.go('/habits');
              },
            ),
            ListTile(
              leading: const Icon(Icons.favorite_border),
              title: const Text('Health'),
              onTap: () {
                Navigator.pop(context);
                context.go('/health');
              },
            ),
            ListTile(
              leading: const Icon(Icons.settings_outlined),
              title: const Text('Settings'),
              onTap: () {
                Navigator.pop(context);
                context.go('/settings');
              },
            ),
          ],
        ),
      ),
    );
  }
}
