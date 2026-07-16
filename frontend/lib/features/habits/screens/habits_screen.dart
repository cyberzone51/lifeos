import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class HabitsScreen extends ConsumerStatefulWidget {
  const HabitsScreen({super.key});

  @override
  ConsumerState<HabitsScreen> createState() => _HabitsScreenState();
}

class _HabitsScreenState extends ConsumerState<HabitsScreen> {
  final List<Map<String, dynamic>> _habits = [
    {"name": "Drink Water", "icon": Icons.water_drop, "color": Colors.blue, "streak": 12, "completed": false},
    {"name": "Exercise", "icon": Icons.fitness_center, "color": Colors.green, "streak": 5, "completed": true},
    {"name": "Read", "icon": Icons.menu_book, "color": Colors.orange, "streak": 20, "completed": false},
    {"name": "Meditate", "icon": Icons.self_improvement, "color": Colors.purple, "streak": 8, "completed": false},
    {"name": "Sleep 8h", "icon": Icons.bedtime, "color": Colors.indigo, "streak": 3, "completed": true},
  ];

  @override
  Widget build(BuildContext context) {
    int completedCount = _habits.where((h) => h["completed"]).length;
    double progress = completedCount / _habits.length;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Habits'),
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
            // Progress Card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Today\'s Progress',
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                        Text(
                          '$completedCount/${_habits.length}',
                          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                fontWeight: FontWeight.bold,
                                color: Theme.of(context).colorScheme.primary,
                              ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: LinearProgressIndicator(
                        value: progress,
                        minHeight: 10,
                        backgroundColor: Colors.grey[200],
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      progress >= 1.0
                          ? "🎉 All habits completed! Great job!"
                          : "Keep going! ${_habits.length - completedCount} more to go.",
                      style: TextStyle(color: Colors.grey[600]),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Habits List
            Text(
              'Your Habits',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            ...(_habits.map((habit) => _HabitTile(
                  habit: habit,
                  onToggle: (value) {
                    setState(() {
                      habit["completed"] = value;
                    });
                  },
                ))),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // TODO: Add habit dialog
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}

class _HabitTile extends StatelessWidget {
  final Map<String, dynamic> habit;
  final Function(bool) onToggle;

  const _HabitTile({required this.habit, required this.onToggle});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: (habit["color"] as Color).withOpacity(0.1),
          child: Icon(habit["icon"], color: habit["color"]),
        ),
        title: Text(
          habit["name"],
          style: TextStyle(
            decoration: habit["completed"] ? TextDecoration.lineThrough : null,
          ),
        ),
        subtitle: Row(
          children: [
            Icon(Icons.local_fire_department, size: 14, color: Colors.orange),
            const SizedBox(width: 4),
            Text('${habit["streak"]} day streak'),
          ],
        ),
        trailing: Checkbox(
          value: habit["completed"],
          onChanged: (value) => onToggle(value ?? false),
        ),
      ),
    );
  }
}
