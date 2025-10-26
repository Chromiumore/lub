import 'package:flutter/material.dart';
import 'package:lub/features/player/application/audio_player_service.dart';

class TrackScreen extends StatefulWidget {
  final int trackID;

  const TrackScreen({super.key, required this.trackID});

  @override
  State<TrackScreen> createState() => _TrackScreenState();
}

class _TrackScreenState extends State<TrackScreen> {
  final _audioManager = AudioPlayerService.instance;

  @override
  void initState() {
    super.initState();
    _init();
  }

  void _init() async {
    await _audioManager.load('http://localhost:8000/music/${widget.trackID}/file');
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        children: [
          Text(widget.trackID.toString()),
          Expanded(
            child: IconButton(
              onPressed: () {
                _audioManager.processControlInput();
              },
              icon: Icon(Icons.play_arrow)
              )
            )
        ],
      ),
    );
  }
}
