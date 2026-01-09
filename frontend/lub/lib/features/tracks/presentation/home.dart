import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'package:lub/features/tracks/data/track.dart';
import 'package:lub/features/tracks/data/track_repository.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<StatefulWidget> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late Future<List<Track>> _tracks;
  final TrackRepository _trackRepository = TrackRepository();

  @override
  void initState() {
    super.initState();
    _init();
  }

  void _init() async {
    _tracks = _trackRepository.getTracks();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Track>>(
      future: _tracks,
      builder:(context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Text('Error: ${snapshot.error}');
        } else if (snapshot.hasData) {
          return ListView.builder(
            itemCount: snapshot.data!.length,
            itemBuilder: (context, index) {
              final track = snapshot.data![index];
              return ListTile(
                leading: FlutterLogo(),
                title: Text(track.name),
                subtitle: Text(track.author.username),
                trailing: Text(track.trackLength.toString()),
                onTap: () => context.go('/music/${track.id}'),
              );
            },
          );
        } else {
          return Center(
            child: Text('No data found'),
          );
        }
      },
    );
  }
}