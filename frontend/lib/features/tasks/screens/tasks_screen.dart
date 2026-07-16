import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class TasksScreen extends ConsumerWidget {
  const TasksScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tasks'),
        actions: [
          IconButton(
            icon: const Icon(Icons.calendar_today),
            onPressed: () {},
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Stats
            Row(
              children: [
                _StatCard(
                  title: 'Today',
                  count: 3,
                  color: Colors.blue,
                ),
                const SizedBox(width: 12),
                _StatCard(
                  title: 'Upcoming',
                  count: 5,
                  color: Colors.orange,
                ),
                const SizedBox(width: 12),
                _StatCard(
                  title: 'Done',
                  count: 8,
                  color: Colors.green,
                ),
              ],
            ),
            const SizedBox(height: 24),

            // High Priority
            Text(
              'High Priority',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            _TaskTile(
              title: 'Finish project proposal',
              dueDate: 'Today, 5:00 PM',
              priority: 3,
              isCompleted: false,
            ),
            _TaskTile(
              title: 'Call dentist',
              dueDate: 'Tomorrow',
              priority: 3,
              isCompleted: false,
            ),
            const SizedBox(height: 24),

            // Medium Priority
            Text(
              'Medium Priority',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            _TaskTile(
              title: 'Buy groceries',
              dueDate: 'Wednesday',
              priority: 2,
              isCompleted: false,
            ),
            _TaskTile(
              title: 'Read documentation',
              dueDate: 'This week',
              priority: 2,
              isCompleted: true,
            ),
            const SizedBox(height: 24),

            // Low Priority
            Text(
              'Low Priority',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            _TaskTile(
              title: 'Organize desk',
              dueDate: 'No deadline',
              priority: 1,
              isCompleted: false,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // TODO: Add task dialog
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  final String title;
  final int count;
  final Color color;

  const _StatCard({
    required this.title,
    required this.count,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              Text(
                count.toString(),
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      color: color,
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 4),
              Text(
                title,
                style: TextStyle(color: Colors.grey[600]),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _TaskTile extends StatelessWidget {
  final String title;
  final String dueDate;
  final int priority;
  final bool isCompleted;

  const _TaskTile({
    required this.title,
    required this.dueDate,
    required this.priority,
    required this.isCompleted,
  });

  Color get _priorityColor {
    switch (priority) {
      case 3:
        return Colors.red;
      case 2:
        return Colors.orange;
      case 1:
        return Colors.green;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: Checkbox(
          value: isCompleted,
          onChanged: (value) {
            // TODO: Toggle task
          },
        ),
        title: Text(
          title,
          style: TextStyle(
            decoration: isCompleted ? TextDecoration.lineThrough : null,
            color: isCompleted ? Colors.grey : null,
          ),
        ),
        subtitle: Text(dueDate),
        trailing: Container(
          width: 4,
          decoration: BoxDecoration(
            color: _priorityColor,
            borderRadius: BorderRadius.circular(2),
          ),
        ),
      ),
    );
  }
}
