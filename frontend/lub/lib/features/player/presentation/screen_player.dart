import 'package:flutter/material.dart';

import 'package:lub/features/player/application/audio_player_service.dart';
import '../../tracks/domain/track.dart';

class ScreenPlayer extends StatefulWidget {
  const ScreenPlayer({super.key, required this.track});

  final Track track;

  @override
  State<ScreenPlayer> createState() => _ScreenPlayerState();
}

class _ScreenPlayerState extends State<ScreenPlayer> {
    final _playerService = AudioPlayerService.instance;
    bool _isPlaying = false;
    
    @override
    void initState() {
      _init();
      _isPlaying = _playerService.isPlaying();
      super.initState();
    }
    
    void _init() async {
      await _playerService.load('http://localhost:8000/music/${widget.track.id}/file');
    }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Column(
        children: [
          Container(
            child: Image.asset(
              'assets/images/photosintesis.jpg',
              height: 300,
              width: 300,
            )
          ),
          Text(
            widget.track.name,
            style: TextStyle(
              fontSize: 20,
            ),
          ),
          Text(widget.track.author.username),
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
      ),
    );
  }
}