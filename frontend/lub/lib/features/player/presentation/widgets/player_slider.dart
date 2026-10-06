import 'package:flutter/material.dart';
import 'package:lub/features/player/application/audio_player_service.dart';

class PlayerSlider extends StatelessWidget {
  const PlayerSlider({super.key, required this.playerService, this.trackId});

  final AudioPlayerService playerService;

  final int? trackId;

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<int?>(
      valueListenable: playerService.currentTrackId,
      builder: (context, currentId, _) {
        final isActive = trackId == null
            ? currentId != null
            : currentId == trackId;

        if (!isActive) {
          return const Slider(min: 0, max: 1, value: 0, onChanged: null);
        }

        return StreamBuilder<Duration?>(
          stream: playerService.durationStream,
          builder: (context, durationSnap) {
            final duration = durationSnap.data ?? Duration.zero;
            final max = duration.inSeconds > 0
                ? duration.inSeconds.toDouble()
                : 1.0;

            return StreamBuilder<Duration>(
              stream: playerService.positionStream,
              builder: (context, posSnap) {
                final position = posSnap.data ?? Duration.zero;
                final value = position.inSeconds.toDouble().clamp(0.0, max);

                return Slider(
                  min: 0,
                  max: max,
                  value: value,
                  onChanged: (v) => playerService.handleSeek(v),
                );
              },
            );
          },
        );
      },
    );
  }
}
