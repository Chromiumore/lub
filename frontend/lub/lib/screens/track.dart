import 'package:flutter/material.dart';
import 'package:just_audio/just_audio.dart';

class TrackScreen extends StatefulWidget {
  final int trackID;

  const TrackScreen({super.key, required this.trackID});

  @override
  State<TrackScreen> createState() => _TrackScreenState();
}

class _TrackScreenState extends State<TrackScreen> {
  final _player = AudioPlayer();

  @override
  void initState() {
    super.initState();
    _init();
  }

  void _init() async {
    await _player.setUrl('http://localhost:8000/music/${widget.trackID}/file');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: [
            Text(widget.trackID.toString()),
            Expanded(
              child: IconButton(
                onPressed: () {
                  if (_player.playing) {
                    _player.stop();
                  } else {
                    _player.play();
                  }
                },
                icon: Icon(Icons.play_arrow)
                )
              )
          ],
        ),
      ),
    );
  }
}
