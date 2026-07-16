import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class HealthScreen extends ConsumerWidget {
  const HealthScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Health'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Weight Card
            _HealthCard(
              title: 'Weight',
              icon: Icons.monitor_weight_outlined,
              value: '75.5 kg',
              trend: '-0.5 kg this week',
              trendColor: Colors.green,
              onTap: () {},
            ),
            const SizedBox(height: 12),

            // Sleep Card
            _HealthCard(
              title: 'Sleep',
              icon: Icons.bedtime_outlined,
              value: '7h 30m',
              trend: 'Quality: Good',
              trendColor: Colors.blue,
              onTap: () {},
            ),
            const SizedBox(height: 12),

            // Water Card
            _HealthCard(
              title: 'Water',
              icon: Icons.water_drop_outlined,
              value: '6 / 8 glasses',
              trend: '75% completed',
              trendColor: Colors.cyan,
              onTap: () {},
            ),
            const SizedBox(height: 12),

            // Mood Card
            _HealthCard(
              title: 'Mood',
              icon: Icons.sentiment_satisfied_outlined,
              value: 'Good',
              trend: 'Average this week: 7/10',
              trendColor: Colors.amber,
              onTap: () {},
            ),
            const SizedBox(height: 24),

            // Quick Actions
            Text(
              'Quick Actions',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                _QuickAction(
                  icon: Icons.add,
                  label: 'Log Weight',
                  onTap: () {},
                ),
                const SizedBox(width: 12),
                _QuickAction(
                  icon: Icons.nightlight_outlined,
                  label: 'Log Sleep',
                  onTap: () {},
                ),
                const SizedBox(width: 12),
                _QuickAction(
                  icon: Icons.water_drop,
                  label: 'Add Water',
                  onTap: () {},
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Stats
            Text(
              'Weekly Stats',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    _StatRow(label: 'Avg Sleep', value: '7h 15m'),
                    _StatRow(label: 'Avg Mood', value: '7.2/10'),
                    _StatRow(label: 'Water Goal', value: '85%'),
                    _StatRow(label: 'Workouts', value: '3'),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _HealthCard extends StatelessWidget {
  final String title;
  final IconData icon;
  final String value;
  final String trend;
  final Color trendColor;
  final VoidCallback onTap;

  const _HealthCard({
    required this.title,
    required this.icon,
    required this.value,
    required this.trend,
    required this.trendColor,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              CircleAvatar(
                backgroundColor: trendColor.withOpacity(0.1),
                child: Icon(icon, color: trendColor),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: TextStyle(color: Colors.grey[600])),
                    Text(
                      value,
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                  ],
                ),
              ),
              Text(
                trend,
                style: TextStyle(color: trendColor, fontSize: 12),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _QuickAction extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;

  const _QuickAction({
    required this.icon,
    required this.label,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Card(
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(16),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                Icon(icon, color: Theme.of(context).colorScheme.primary),
                const SizedBox(height: 8),
                Text(label, style: Theme.of(context).textTheme.bodySmall),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _StatRow extends StatelessWidget {
  final String label;
  final String value;

  const _StatRow({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: TextStyle(color: Colors.grey[600])),
          Text(value, style: const TextStyle(fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
