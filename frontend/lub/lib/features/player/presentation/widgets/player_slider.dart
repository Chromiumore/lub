import 'package:flutter/material.dart';
import 'package:lub/features/player/application/audio_player_service.dart';

class PlayerSlider extends StatefulWidget {
  const PlayerSlider({super.key, required this.playerService});

  final AudioPlayerService playerService;

  @override
  State<StatefulWidget> createState() => _PlayerSliderState();
}

class _PlayerSliderState extends State<PlayerSlider> {
  @override
  Widget build(BuildContext context) {
    return StreamBuilder<Duration?>(
      stream: widget.playerService.durationStream,
      builder: (context, durationSnap) {
        final duration = durationSnap.data ?? Duration.zero;
        final max = duration.inSeconds > 0
            ? duration.inSeconds.toDouble()
            : 1.0;

        return StreamBuilder<Duration>(
          stream: widget.playerService.positionStream,
          builder: (context, posSnap) {
            final position = posSnap.data ?? Duration.zero;
            final value = position.inSeconds.toDouble().clamp(0.0, max);

            return Slider(
              min: 0,
              max: max,
              value: value,
              onChanged: (v) => widget.playerService.handleSeek(v),
            );
          },
        );
      },
    );
  }
}
