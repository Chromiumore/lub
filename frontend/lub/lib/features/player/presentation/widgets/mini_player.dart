import 'package:flutter/material.dart';
import 'package:lub/features/player/application/audio_player_service.dart';
import 'package:lub/features/player/presentation/widgets/player_controls.dart';
import 'package:lub/features/player/presentation/widgets/player_slider.dart';

class MiniPlayer extends StatelessWidget {
  const MiniPlayer({super.key});

  @override
  Widget build(BuildContext context) {
    final playerService = AudioPlayerService.instance;
    return Container(
      padding: const EdgeInsets.all(20),
      child: Column(
        children: [
          PlayerSlider(playerService: playerService),
          Padding(
            padding: const EdgeInsets.only(left: 25, right: 25),
            child: PlayerControls(playerService: playerService),
          ),
        ],
      ),
    );
  }
}
