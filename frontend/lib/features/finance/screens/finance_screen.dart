import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class FinanceScreen extends ConsumerWidget {
  const FinanceScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Finance'),
        actions: [
          IconButton(
            icon: const Icon(Icons.bar_chart),
            onPressed: () {},
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Balance Card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Balance',
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            color: Colors.grey[600],
                          ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      '\$2,450.00',
                      style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    const SizedBox(height: 16),
                    Row(
                      children: [
                        _BalanceChip(
                          label: 'Income',
                          amount: '+\$3,200',
                          color: Colors.green,
                        ),
                        const SizedBox(width: 12),
                        _BalanceChip(
                          label: 'Expenses',
                          amount: '-\$750',
                          color: Colors.red,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Quick Add
            Text(
              'Quick Add',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () {},
                    icon: const Icon(Icons.remove_circle_outline),
                    label: const Text('Expense'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () {},
                    icon: const Icon(Icons.add_circle_outline),
                    label: const Text('Income'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Categories
            Text(
              'Categories',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            _CategoryTile(
              name: 'Food & Drinks',
              icon: Icons.restaurant,
              amount: '\$320',
              percentage: 0.42,
              color: Colors.orange,
            ),
            _CategoryTile(
              name: 'Transport',
              icon: Icons.directions_bus,
              amount: '\$150',
              percentage: 0.20,
              color: Colors.blue,
            ),
            _CategoryTile(
              name: 'Shopping',
              icon: Icons.shopping_bag,
              amount: '\$180',
              percentage: 0.24,
              color: Colors.purple,
            ),
            _CategoryTile(
              name: 'Other',
              icon: Icons.more_horiz,
              amount: '\$100',
              percentage: 0.14,
              color: Colors.grey,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // TODO: Add expense dialog
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}

class _BalanceChip extends StatelessWidget {
  final String label;
  final String amount;
  final Color color;

  const _BalanceChip({
    required this.label,
    required this.amount,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: TextStyle(
              fontSize: 12,
              color: color,
            ),
          ),
          Text(
            amount,
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
        ],
      ),
    );
  }
}

class _CategoryTile extends StatelessWidget {
  final String name;
  final IconData icon;
  final String amount;
  final double percentage;
  final Color color;

  const _CategoryTile({
    required this.name,
    required this.icon,
    required this.amount,
    required this.percentage,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: color.withOpacity(0.1),
          child: Icon(icon, color: color),
        ),
        title: Text(name),
        subtitle: LinearProgressIndicator(
          value: percentage,
          backgroundColor: Colors.grey[200],
          color: color,
        ),
        trailing: Text(
          amount,
          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
        ),
      ),
    );
  }
}
