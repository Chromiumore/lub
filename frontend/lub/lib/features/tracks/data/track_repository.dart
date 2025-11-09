import 'package:dio/dio.dart';
import 'package:lub/features/tracks/data/track.dart';

class TrackRepository {
  final Dio dio = Dio();

  Future<Track> getTrack(int trackID) async {
    var response = await dio
    .get('http://localhost:8000/music/$trackID');
    Track track = Track.fromJson(response.data!);
    return Future.value(track);
  }

  Future<List<Track>> getTracks() async {
    var response = await dio
    .get('http://localhost:8000/music');
    final List<dynamic> tracksData = response.data;
    List<Track> tracks = tracksData
      .map((item) => Track.fromJson(item as Map<String, dynamic>))
      .toList();
    return Future.value(tracks);
  }
}