import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:lub/features/tracks/data/api_client.dart';

import 'package:lub/features/tracks/data/repositories/track_repository.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';
import 'package:lub/shared/utils/timer_formatter.dart';
import 'package:lub/shared/widgets/cover_image_placeholder.dart';
import 'package:lub/shared/widgets/network_cover_image.dart';

enum _TrackPopupMenuAction { EDIT_INFO, CHANGE_AUDIO, CHANGE_COVER, DELETE }

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
    _tracks = _trackRepository.getTracks();
  }

  Future<void> _deleteTrack(int id) async {
    try {
      await _trackRepository.deleteTrack(id);

      if (!mounted) return;
      setState(() {
        _tracks = _trackRepository.getTracks();
      });

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Track has been deleted'),
          backgroundColor: Colors.green,
        ),
      );
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error while deleting: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
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
              onPressed: () {
                setState(() {
                  _tracks = _trackRepository.getTracks();
                });
              },
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
                        trailing: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            PopupMenuButton(
                              offset: Offset(-50, 0),
                              onSelected: (_TrackPopupMenuAction item) {
                                switch (item) {
                                  case _TrackPopupMenuAction.EDIT_INFO:
                                    context.push(
                                      '/music/${track.id!}/update',
                                      extra: track,
                                    );
                                    break;
                                  case _TrackPopupMenuAction.DELETE:
                                    _deleteTrack(track.id!);
                                    break;
                                  default:
                                }
                              },
                              itemBuilder: (context) => [
                                PopupMenuItem<_TrackPopupMenuAction>(
                                  value: _TrackPopupMenuAction.EDIT_INFO,
                                  child: Row(
                                    children: [
                                      Icon(Icons.edit),
                                      Text('Edit Info'),
                                    ],
                                  ),
                                ),
                                PopupMenuItem<_TrackPopupMenuAction>(
                                  value: _TrackPopupMenuAction.CHANGE_AUDIO,
                                  child: Row(
                                    children: [
                                      Icon(Icons.audio_file),
                                      Text('Change Audio'),
                                    ],
                                  ),
                                ),
                                PopupMenuItem<_TrackPopupMenuAction>(
                                  value: _TrackPopupMenuAction.CHANGE_COVER,
                                  child: Row(
                                    children: [
                                      Icon(Icons.image),
                                      Text('Change Cover'),
                                    ],
                                  ),
                                ),
                                PopupMenuItem<_TrackPopupMenuAction>(
                                  value: _TrackPopupMenuAction.DELETE,
                                  child: Row(
                                    children: [
                                      Icon(Icons.delete, color: Colors.red),
                                      Text(
                                        'Delete',
                                        style: TextStyle(color: Colors.red),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                            Text(
                              formatDurationMinutesSeconds(
                                Duration(seconds: track.audio!.duration!),
                              ),
                            ),
                          ],
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
