import 'package:flutter/material.dart';
import 'package:dio/dio.dart';

import '../../player/presentation/screen_player.dart';
import '../domain/track.dart';

class TrackScreen extends StatefulWidget {
  final int trackID;

  const TrackScreen({super.key, required this.trackID});

  @override
  State<TrackScreen> createState() => _TrackScreenState();
}

class _TrackScreenState extends State<TrackScreen> {
  late Future<Track> _track;

  @override
  void initState() {
    super.initState();
    _track = getTrack();
  }

  Future<Track> getTrack() async {
    var response = await Dio()
    .get('http://localhost:8000/music/${widget.trackID}');
    Track track = Track.fromJson(response.data!);
    return Future.value(track);
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
