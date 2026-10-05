import 'package:flutter/material.dart';

import 'package:lub/features/player/application/audio_player_service.dart';
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
    await _playerService.load(
      'http://localhost:8000/api/v1/music/${widget.track.id}/audio',
    );
  }

  @override
  void dispose() {
    super.dispose();
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
            StreamBuilder<Duration?>(
              stream: _playerService.durationStream,
              builder: (context, durationSnap) {
                final duration = durationSnap.data ?? Duration.zero;
                final max = duration.inSeconds > 0
                    ? duration.inSeconds.toDouble()
                    : 1.0;

                return StreamBuilder<Duration>(
                  stream: _playerService.positionStream,
                  builder: (context, posSnap) {
                    final position = posSnap.data ?? Duration.zero;
                    final value = position.inSeconds.toDouble().clamp(0.0, max);

                    return Slider(
                      min: 0,
                      max: max,
                      value: value,
                      onChanged: (v) => _playerService.handleSeek(v),
                    );
                  },
                );
              },
            ),

            StreamBuilder<bool>(
              stream: _playerService.playingStream,
              initialData: _playerService.isPlaying,
              builder: (context, snap) {
                final isPlaying = snap.data ?? false;
                return Padding(
                  padding: EdgeInsetsGeometry.only(left: 25, right: 25),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text('00:00'),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          IconButton(
                            onPressed: () {},
                            icon: const Icon(Icons.fast_rewind),
                          ),
                          IconButton(
                            onPressed: _playerService.handlePlayButton,
                            icon: Icon(
                              isPlaying ? Icons.pause : Icons.play_arrow,
                            ),
                          ),
                          IconButton(
                            onPressed: () {},
                            icon: const Icon(Icons.fast_forward),
                          ),
                        ],
                      ),
                      Text('01:00'),
                    ],
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
