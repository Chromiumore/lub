import 'package:flutter/material.dart';
import 'package:lub/features/player/application/audio_player_service.dart';

class PlayerControls extends StatelessWidget {
  const PlayerControls({super.key, required this.playerService, this.trackId});

  final AudioPlayerService playerService;
  final int? trackId;

  String _format(Duration d) {
    final m = d.inMinutes.remainder(60).toString().padLeft(2, '0');
    final s = d.inSeconds.remainder(60).toString().padLeft(2, '0');
    return '$m:$s';
  }

  Future<void> _onPlayPressed() async {
    if (trackId == null) {
      playerService.handlePlayButton();
    } else {
      await playerService.toggleTrack(trackId!);
    }
  }

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<int?>(
      valueListenable: playerService.currentTrackId,
      builder: (context, currentId, _) {
        final isActive = trackId == null
            ? currentId != null
            : currentId == trackId;

        final VoidCallback? onPlay = trackId == null
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
                return Text(_format(pos));
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
                final dur = isActive
                    ? (durSnap.data ?? Duration.zero)
                    : Duration.zero;
                return Text(_format(dur));
              },
            ),
          ],
        );
      },
    );
  }
}
