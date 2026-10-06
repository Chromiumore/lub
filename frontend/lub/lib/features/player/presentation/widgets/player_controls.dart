import 'package:flutter/material.dart';
import 'package:lub/features/player/application/audio_player_service.dart';

class PlayerControls extends StatefulWidget {
  const PlayerControls({super.key, required this.playerService});

  final AudioPlayerService playerService;

  @override
  State<PlayerControls> createState() => _PlayerControlsState();
}

class _PlayerControlsState extends State<PlayerControls> {
  String formatDuration(Duration duration) {
    return '${duration.inMinutes.remainder(60).toString().padLeft(2, '0')}:${duration.inSeconds.remainder(60).toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        StreamBuilder<Duration>(
          stream: widget.playerService.positionStream,
          builder: (context, posSnap) {
            final position = posSnap.data ?? Duration.zero;
            return Text(formatDuration(position));
          },
        ),

        StreamBuilder<bool>(
          stream: widget.playerService.playingStream,
          initialData: widget.playerService.isPlaying,
          builder: (context, snap) {
            final isPlaying = snap.data ?? false;
            return Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton(
                  onPressed: () {},
                  icon: const Icon(Icons.fast_rewind),
                ),
                IconButton(
                  onPressed: widget.playerService.handlePlayButton,
                  icon: Icon(isPlaying ? Icons.pause : Icons.play_arrow),
                ),
                IconButton(
                  onPressed: () {},
                  icon: const Icon(Icons.fast_forward),
                ),
              ],
            );
          },
        ),

        StreamBuilder<Duration?>(
          stream: widget.playerService.durationStream,
          builder: (context, durationSnap) {
            final duration = durationSnap.data ?? Duration.zero;
            return Text(formatDuration(duration));
          },
        ),
      ],
    );
  }
}
