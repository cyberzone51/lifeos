import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Profile Section
          Card(
            child: ListTile(
              leading: CircleAvatar(
                child: Icon(Icons.person),
              ),
              title: Text('User Name'),
              subtitle: Text('user@example.com'),
              trailing: Icon(Icons.chevron_right),
            ),
          ),
          const SizedBox(height: 16),

          // General
          Text(
            'General',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          _SettingsTile(
            icon: Icons.language,
            title: 'Language',
            subtitle: 'English',
          ),
          _SettingsTile(
            icon: Icons.attach_money,
            title: 'Currency',
            subtitle: 'USD',
          ),
          _SettingsTile(
            icon: Icons.access_time,
            title: 'Timezone',
            subtitle: 'UTC',
          ),
          const SizedBox(height: 16),

          // Appearance
          Text(
            'Appearance',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          _SettingsTile(
            icon: Icons.dark_mode,
            title: 'Theme',
            subtitle: 'System',
          ),
          const SizedBox(height: 16),

          // AI
          Text(
            'AI',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          _SettingsTile(
            icon: Icons.psychology,
            title: 'AI Memory',
            subtitle: 'Manage what AI remembers',
          ),
          _SettingsTile(
            icon: Icons.mic,
            title: 'Voice Input',
            subtitle: 'Whisper',
          ),
          const SizedBox(height: 16),

          // Premium
          Card(
            color: Theme.of(context).colorScheme.primaryContainer,
            child: ListTile(
              leading: Icon(
                Icons.star,
                color: Theme.of(context).colorScheme.primary,
              ),
              title: Text('Upgrade to Premium'),
              subtitle: Text('Unlimited AI, advanced features'),
              trailing: Icon(Icons.chevron_right),
            ),
          ),
          const SizedBox(height: 16),

          // About
          Text(
            'About',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          _SettingsTile(
            icon: Icons.info_outline,
            title: 'About LifeOS',
            subtitle: 'Version 1.0.0',
          ),
          _SettingsTile(
            icon: Icons.privacy_tip_outlined,
            title: 'Privacy Policy',
          ),
          _SettingsTile(
            icon: Icons.description_outlined,
            title: 'Terms of Service',
          ),
          const SizedBox(height: 24),

          // Logout
          OutlinedButton(
            onPressed: () {
              // TODO: Logout
            },
            style: OutlinedButton.styleFrom(
              foregroundColor: Colors.red,
            ),
            child: const Text('Logout'),
          ),
        ],
      ),
    );
  }
}

class _SettingsTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String? subtitle;

  const _SettingsTile({
    required this.icon,
    required this.title,
    this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: Icon(icon),
        title: Text(title),
        subtitle: subtitle != null ? Text(subtitle!) : null,
        trailing: Icon(Icons.chevron_right),
        onTap: () {
          // TODO: Navigate to setting
        },
      ),
    );
  }
}
