import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:lub/features/tracks/data/api_client.dart';

import 'package:lub/features/tracks/data/repositories/track_repository.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';
import 'package:lub/shared/utils/timer_formatter.dart';
import 'package:lub/shared/widgets/cover_image_placeholder.dart';
import 'package:lub/shared/widgets/network_cover_image.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<StatefulWidget> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late Future<List<Track>> _tracks;
  final TrackRepository _trackRepository = TrackRepository();
  final ApiClient _api = ApiClient();

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
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        children: [
          Container(
            alignment: AlignmentGeometry.centerRight,
            padding: EdgeInsets.only(bottom: 10),
            child: ElevatedButton(
              child: Icon(Icons.refresh),
              onPressed: () => context.push('/'),
            ),
          ),
          Expanded(
            child: FutureBuilder<List<Track>>(
              future: _tracks,
              builder: (context, snapshot) {
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
                        leading: SizedBox(
                          height: 50,
                          width: 50,
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(4),
                            child: track.hasCover
                                ? NetworkCoverImage(
                                    _api.getCoverDownloadUrl(track.id!),
                                  )
                                : CoverImagePlaceholder(),
                          ),
                        ),
                        title: Text(track.name!),
                        subtitle: Text(track.author!.username!),
                        trailing: Text(
                          formatDurationMinutesSeconds(
                            Duration(seconds: track.audio!.duration!),
                          ),
                        ),
                        onTap: () => context.go('/music/${track.id}'),
                      );
                    },
                  );
                } else {
                  return Center(child: Text('No data found'));
                }
              },
            ),
          ),
        ],
      ),
    );
  }
}
