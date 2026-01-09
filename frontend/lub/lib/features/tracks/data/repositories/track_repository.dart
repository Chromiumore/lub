import 'package:lub/features/tracks/data/api_client.dart';
import 'package:lub/features/tracks/data/models/track.dart';

class TrackRepository {
  final ApiClient api = ApiClient();

  Future<TrackModel> getTrack(int trackID) async {
    return api.getTrack(trackID);
  }

  Future<List<TrackModel>> getTracks() async {
    return api.getTracks();
  }
}