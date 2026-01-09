import 'package:lub/features/tracks/data/api_client.dart';
import 'package:lub/features/tracks/data/models/track.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';

class TrackRepository {
  final ApiClient api = ApiClient();

  Future<Track> getTrack(int trackID) async {
    TrackModel model = await api.getTrack(trackID);
    return model.toEntity();
  }

  Future<List<Track>> getTracks() async {
    List<TrackModel> models = await api.getTracks();
    List<Track> entities = models.map((item) => item.toEntity()).toList();
    return entities;
  }
}