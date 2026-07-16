import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('LifeOS'),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            onPressed: () {},
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Welcome + AI Briefing
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        CircleAvatar(
                          backgroundColor: Theme.of(context).colorScheme.primary,
                          child: const Icon(Icons.psychology, color: Colors.white),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Good morning! 👋',
                                style: Theme.of(context).textTheme.headlineSmall,
                              ),
                              Text(
                                'Level 12 • 🔥 5 day streak',
                                style: TextStyle(color: Colors.grey[600]),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    const Divider(),
                    const SizedBox(height: 8),
                    Text(
                      "Today's briefing:",
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      "You have 3 tasks today. Your water habit needs attention. Budget is on track.",
                      style: TextStyle(color: Colors.grey[600]),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Quick Actions Grid
            Text(
              'Quick Actions',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            GridView.count(
              crossAxisCount: 4,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              mainAxisSpacing: 12,
              crossAxisSpacing: 12,
              children: [
                _QuickAction(icon: Icons.add_circle, label: 'Expense', color: Colors.green, onTap: () {}),
                _QuickAction(icon: Icons.check_circle, label: 'Task', color: Colors.blue, onTap: () {}),
                _QuickAction(icon: Icons.water_drop, label: 'Water', color: Colors.cyan, onTap: () {}),
                _QuickAction(icon: Icons.chat, label: 'AI Chat', color: Colors.purple, onTap: () {}),
              ],
            ),
            const SizedBox(height: 24),

            // Today's Overview
            Text(
              'Today\'s Overview',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                _OverviewCard(
                  icon: Icons.task_alt,
                  title: 'Tasks',
                  value: '3',
                  subtitle: 'to do',
                  color: Colors.blue,
                ),
                const SizedBox(width: 12),
                _OverviewCard(
                  icon: Icons.local_fire_department,
                  title: 'Habits',
                  value: '2/5',
                  subtitle: 'done',
                  color: Colors.orange,
                ),
                const SizedBox(width: 12),
                _OverviewCard(
                  icon: Icons.account_balance_wallet,
                  title: 'Spent',
                  value: '\$45',
                  subtitle: 'today',
                  color: Colors.green,
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Active Goals
            Text(
              'Active Goals',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            _GoalProgress(
              title: 'Save \$5000',
              progress: 0.65,
              current: '\$3250',
              target: '\$5000',
              color: Colors.green,
            ),
            _GoalProgress(
              title: 'Lose 5 kg',
              progress: 0.4,
              current: '2 kg',
              target: '5 kg',
              color: Colors.blue,
            ),
            const SizedBox(height: 24),

            // Recent Activity
            Text(
              'Recent Activity',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            _ActivityTile(
              icon: Icons.restaurant,
              title: 'Lunch at cafe',
              subtitle: '2 hours ago',
              amount: '-\$15',
              amountColor: Colors.red,
            ),
            _ActivityTile(
              icon: Icons.check_circle,
              title: 'Completed: Review docs',
              subtitle: '3 hours ago',
              amount: '+50 XP',
              amountColor: Colors.green,
            ),
            _ActivityTile(
              icon: Icons.water_drop,
              title: 'Water: 2 glasses',
              subtitle: '4 hours ago',
              amount: null,
              amountColor: null,
            ),
          ],
        ),
      ),
    );
  }
}

class _QuickAction extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;
  final VoidCallback onTap;

  const _QuickAction({
    required this.icon,
    required this.label,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 4),
            Text(
              label,
              style: TextStyle(fontSize: 11, color: color),
            ),
          ],
        ),
      ),
    );
  }
}

class _OverviewCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String value;
  final String subtitle;
  final Color color;

  const _OverviewCard({
    required this.icon,
    required this.title,
    required this.value,
    required this.subtitle,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            children: [
              Icon(icon, color: color, size: 24),
              const SizedBox(height: 8),
              Text(
                value,
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              Text(
                subtitle,
                style: TextStyle(fontSize: 12, color: Colors.grey[600]),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _GoalProgress extends StatelessWidget {
  final String title;
  final double progress;
  final String current;
  final String target;
  final Color color;

  const _GoalProgress({
    required this.title,
    required this.progress,
    required this.current,
    required this.target,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
                Text('$current / $target', style: TextStyle(color: Colors.grey[600])),
              ],
            ),
            const SizedBox(height: 8),
            ClipRRect(
              borderRadius: BorderRadius.circular(4),
              child: LinearProgressIndicator(
                value: progress,
                minHeight: 8,
                backgroundColor: Colors.grey[200],
                color: color,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ActivityTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final String? amount;
  final Color? amountColor;

  const _ActivityTile({
    required this.icon,
    required this.title,
    required this.subtitle,
    this.amount,
    this.amountColor,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: CircleAvatar(child: Icon(icon)),
        title: Text(title),
        subtitle: Text(subtitle),
        trailing: amount != null
            ? Text(
                amount!,
                style: TextStyle(
                  color: amountColor,
                  fontWeight: FontWeight.bold,
                ),
              )
            : null,
      ),
    );
  }
}
