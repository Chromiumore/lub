import 'package:flutter/material.dart';
import 'package:lub/features/player/application/audio_player_service.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';
import 'package:lub/shared/utils/timer_formatter.dart';

class PlayerControls extends StatelessWidget {
  const PlayerControls({super.key, required this.playerService, this.track});

  final AudioPlayerService playerService;
  final Track? track;

  Future<void> _onPlayPressed() async {
    if (track == null) {
      playerService.handlePlayButton();
    } else {
      await playerService.toggleTrack(track!.id!);
    }
  }

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<int?>(
      valueListenable: playerService.currentTrackId,
      builder: (context, currentId, _) {
        final isActive = track == null
            ? currentId != null
            : currentId == track?.id;

        final VoidCallback? onPlay = track == null
            ? (isActive ? _onPlayPressed : null)
            : _onPlayPressed;

        return Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            StreamBuilder<Duration>(
              stream: playerService.positionStream,
              initialData: Duration.zero,
              builder: (context, posSnap) {
                final pos = isActive
                    ? (posSnap.data ?? Duration.zero)
                    : Duration.zero;
                return Text(formatDurationMinutesSeconds(pos));
              },
            ),
            StreamBuilder<bool>(
              stream: playerService.playingStream,
              initialData: playerService.isPlaying,
              builder: (context, snap) {
                final isPlaying = isActive && (snap.data ?? false);
                return Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    IconButton(
                      onPressed: isActive ? () {} : null,
                      icon: const Icon(Icons.fast_rewind),
                    ),
                    IconButton(
                      onPressed: onPlay,
                      icon: Icon(isPlaying ? Icons.pause : Icons.play_arrow),
                    ),
                    IconButton(
                      onPressed: isActive ? () {} : null,
                      icon: const Icon(Icons.fast_forward),
                    ),
                  ],
                );
              },
            ),
            StreamBuilder<Duration?>(
              stream: playerService.durationStream,
              initialData: Duration.zero,
              builder: (context, durSnap) {
                final dur = track != null
                    ? Duration(seconds: track!.audio!.duration!)
                    : durSnap.data ?? Duration.zero;
                return Text(formatDurationMinutesSeconds(dur));
              },
            ),
          ],
        );
      },
    );
  }
}
