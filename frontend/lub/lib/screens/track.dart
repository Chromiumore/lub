import 'package:flutter/material.dart';
import 'package:lub/audio_service/audio_manager_imp.dart';

class TrackScreen extends StatefulWidget {
  final int trackID;

  const TrackScreen({super.key, required this.trackID});

  @override
  State<TrackScreen> createState() => _TrackScreenState();
}

class _TrackScreenState extends State<TrackScreen> {
  final _audioManager = AudioManagerImp.instance;

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
    return Scaffold(
      body: Center(
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
      ),
    );
  }
}
