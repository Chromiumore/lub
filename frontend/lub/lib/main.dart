import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'screens/home.dart';
import 'screens/track.dart';
import 'screens/navigation_sidebar.dart';
import 'audio_service/audio_manager_imp.dart';

void main() {
  runApp(const MyApp());
  AudioManagerImp.instance.init();
}

final _router = GoRouter(
  routes: [
    ShellRoute(
      builder: (context, state, child) {
        return MyNavigationSidebar(child: child);
      },
      routes: [
        GoRoute(
          path: '/',
          builder: (context, state) => HomeScreen(),
        ),
        GoRoute(
          path: '/music/:trackID',
          builder: (context, state) => TrackScreen(trackID: int.parse(state.pathParameters['trackID']!)),
        ),
      ]
    )
  ],
);

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: _router,
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
    );
  }
}
