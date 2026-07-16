import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lifeos/app/router.dart';
import 'package:lifeos/app/theme.dart';

class LifeOSApp extends ConsumerWidget {
  const LifeOSApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);
    final theme = ref.watch(themeProvider);

    return MaterialApp.router(
      title: 'LifeOS',
      debugShowCheckedModeBanner: false,
      theme: theme,
      routerConfig: router,
    );
  }
}
