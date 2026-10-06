import 'package:flutter/material.dart';
import 'package:lub/features/player/application/audio_player_service.dart';
import 'package:lub/features/player/presentation/widgets/player_controls.dart';
import 'package:lub/features/player/presentation/widgets/player_slider.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';

class ScreenPlayer extends StatelessWidget {
  const ScreenPlayer({super.key, required this.track});

  final Track track;

  @override
  Widget build(BuildContext context) {
    final playerService = AudioPlayerService.instance;
    return Card(
      child: Padding(
        padding: const EdgeInsets.only(top: 24),
        child: Column(
          children: [
            Image.asset(
              'assets/images/photosintesis.jpg',
              height: 300,
              width: 300,
            ),
            Text(track.name!, style: const TextStyle(fontSize: 20)),
            Text(track.author!.username),
            PlayerSlider(playerService: playerService, trackId: track.id),
            Padding(
              padding: const EdgeInsets.only(left: 25, right: 25),
              child: PlayerControls(
                playerService: playerService,
                trackId: track.id,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
