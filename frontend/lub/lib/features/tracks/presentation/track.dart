import 'package:flutter/material.dart';
import 'package:lub/features/tracks/data/repositories/track_repository.dart';

import '../../player/presentation/widgets/screen_player.dart';
import '../data/models/track.dart';

class TrackScreen extends StatefulWidget {
  final int trackID;

  const TrackScreen({super.key, required this.trackID});

  @override
  State<TrackScreen> createState() => _TrackScreenState();
}

class _TrackScreenState extends State<TrackScreen> {
  late Future<Track> _track;
  final TrackRepository _trackRepository = TrackRepository();

  @override
  void initState() {
    super.initState();
    _init();
  }

  void _init() async {
    _track = _trackRepository.getTrack(widget.trackID);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: _track,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Text('Error: ${snapshot.error}');
        } else if (snapshot.hasData) {
          return Center(
            child: SizedBox(
              width: 400,
              height: 500,
              child: ScreenPlayer(track: snapshot.data!),
            ),
          );
        } else {
          return Center(
            child: Text('No data found'),
          );
        }
      }
    );
  }
}
