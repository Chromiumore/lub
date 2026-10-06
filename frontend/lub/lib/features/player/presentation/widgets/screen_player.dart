import 'package:flutter/material.dart';

import 'package:lub/features/player/application/audio_player_service.dart';
import 'package:lub/features/player/presentation/widgets/player_controls.dart';
import 'package:lub/features/player/presentation/widgets/player_slider.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';

class ScreenPlayer extends StatefulWidget {
  const ScreenPlayer({super.key, required this.track});

  final Track track;

  @override
  State<ScreenPlayer> createState() => _ScreenPlayerState();
}

class _ScreenPlayerState extends State<ScreenPlayer> {
  final _playerService = AudioPlayerService.instance;

  @override
  void initState() {
    _init();
    super.initState();
  }

  void _init() async {
    await _playerService.load(widget.track.id!);
  }

  @override
  void dispose() {
    super.dispose();
  }

  String formatDuration(Duration duration) {
    return '${duration.inMinutes.remainder(60).toString().padLeft(2, '0')}:${duration.inSeconds.remainder(60).toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
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
            Text(widget.track.name!, style: TextStyle(fontSize: 20)),
            Text(widget.track.author!.username),
            PlayerSlider(playerService: _playerService),

            Padding(
              padding: EdgeInsetsGeometry.only(left: 25, right: 25),
              child: PlayerControls(playerService: _playerService),
            ),
          ],
        ),
      ),
    );
  }
}
