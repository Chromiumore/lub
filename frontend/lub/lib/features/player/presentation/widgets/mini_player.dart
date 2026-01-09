import 'package:flutter/material.dart';
import 'package:lub/features/player/application/audio_player_service.dart';

class MiniPlayer extends StatefulWidget {
  const MiniPlayer({super.key});
  
  @override
  State<MiniPlayer> createState() => _MiniPlayerState();
}

class _MiniPlayerState extends State<MiniPlayer> {
  final _playerService = AudioPlayerService.instance;
  bool _isPlaying = false;
  
  @override
  void initState() {
    _isPlaying = _playerService.isPlaying();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: Column(
        children: [
          Slider(
            value: 0.5,
            onChanged: (value) {}
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              IconButton(
                onPressed: () => (),
                icon: Icon(Icons.fast_rewind)
              ),
              IconButton(
                onPressed: () {
                  _playerService.processControlInput();
                  setState(() {
                    _isPlaying = !_isPlaying;
                  });
                },
                icon: _isPlaying ? Icon(Icons.pause) : Icon(Icons.play_arrow)
              ),
              IconButton(
                onPressed: () => (),
                icon: Icon(Icons.fast_forward)
              ),
            ],
          )
        ],
      )
    );
  }
}
