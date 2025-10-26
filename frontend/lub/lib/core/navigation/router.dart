import 'package:go_router/go_router.dart';
import 'package:flutter/material.dart';

import '../../features/tracks/presentation/home.dart';
import '../../features/tracks/presentation/track.dart';
import '../../features/player/presentation/mini_player.dart';
import '../widgets/navigation_sidebar.dart';


final router = GoRouter(
  routes: [
    ShellRoute(
      builder: (context, state, child) {
        return Scaffold(
          appBar: AppBar(title: const Text('LUB')),
          body: child,
          drawer: MyNavigationSidebar(),
        );
      },
      routes: [
        ShellRoute(
          builder: (context, state, child) {
            return Scaffold(
              body: Column(
                children: [
                  Expanded(child: child),
                  MiniPlayer(),
                ],
              )
            );
          },
          routes: [
            GoRoute(
              path: '/',
              builder: (context, state) => HomeScreen(),
            ),
          ]
        ),
        GoRoute(
          path: '/music/:trackID',
          builder: (context, state) => TrackScreen(trackID: int.parse(state.pathParameters['trackID']!)),
        ),
      ]
    )
  ],
);