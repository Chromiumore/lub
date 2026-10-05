import 'package:flutter/material.dart';
import 'package:lub/features/player/application/audio_player_service.dart';
import 'package:lub/features/player/presentation/widgets/player_controls.dart';
import 'package:lub/features/player/presentation/widgets/player_slider.dart';

class MiniPlayer extends StatefulWidget {
  const MiniPlayer({super.key});

  @override
  State<MiniPlayer> createState() => _MiniPlayerState();
}

class _MiniPlayerState extends State<MiniPlayer> {
  final _playerService = AudioPlayerService.instance;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(20),
      child: Column(
        children: [
          PlayerSlider(playerService: _playerService),
          Padding(
            padding: EdgeInsetsGeometry.only(left: 25, right: 25),
            child: PlayerControls(playerService: _playerService),
          ),
        ],
      ),
    );
  }
}
