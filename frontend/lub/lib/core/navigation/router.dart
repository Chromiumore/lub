import 'package:go_router/go_router.dart';
import 'package:flutter/material.dart';
import 'package:lub/core/widgets/navigation_sidebar.dart';
import 'package:lub/features/player/presentation/widgets/mini_player.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';
import 'package:lub/features/tracks/presentation/screens/home.dart';
import 'package:lub/features/tracks/presentation/screens/track.dart';
import 'package:lub/features/tracks/presentation/screens/update_audio.dart';
import 'package:lub/features/tracks/presentation/screens/update_track.dart';
import 'package:lub/features/tracks/presentation/screens/upload.dart';

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
              ),
            );
          },
          routes: [
            GoRoute(path: '/', builder: (context, state) => HomeScreen()),
          ],
        ),
        GoRoute(
          path: '/music/:trackId',
          builder: (context, state) =>
              TrackScreen(trackID: int.parse(state.pathParameters['trackId']!)),
        ),
        GoRoute(
          path: '/upload',
          builder: (context, state) => Scaffold(body: UploadTrackScreen()),
        ),
        GoRoute(
          path: '/music/:trackId/update',
          builder: (context, state) => Scaffold(
            body: UpdateTrackScreen(
              trackId: int.parse(state.pathParameters['trackId']!),
              track: state.extra as Track?,
            ),
          ),
        ),
        GoRoute(
          path: '/music/:trackId/audio/update',
          builder: (context, state) => Scaffold(
            body: UpdateTrackAudioScreen(
              trackId: int.parse(state.pathParameters['trackId']!),
            ),
          ),
        ),
      ],
    ),
  ],
);
