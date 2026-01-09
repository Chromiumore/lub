import 'package:lub/features/tracks/data/api_client.dart';
import 'package:lub/features/tracks/data/models/track.dart';

class TrackRepository {
  final ApiClient api = ApiClient();

  Future<Track> getTrack(int trackID) async {
    return api.getTrack(trackID);
  }

  Future<List<Track>> getTracks() async {
    return api.getTracks();
  }
}