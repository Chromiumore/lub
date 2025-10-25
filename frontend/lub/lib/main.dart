import 'package:flutter/material.dart';

import 'features/player/application/audio_player_service.dart';
import 'core/navigation/router.dart';

void main() {
  runApp(const MyApp());
  AudioPlayerService.instance.init();
}


class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: router,
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
    );
  }
}
