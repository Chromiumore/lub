import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:just_audio_media_kit/just_audio_media_kit.dart';

import 'screens/home.dart';
import 'screens/track.dart';

void main() {
  JustAudioMediaKit.ensureInitialized();
  runApp(const MyApp());
}

final _router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => HomeScreen(),
      ),
      GoRoute(
        path: '/music/:trackID',
        builder: (context, state) => TrackScreen(trackID: int.parse(state.pathParameters['trackID']!)),
      ),
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
