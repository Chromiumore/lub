import 'package:lub/features/tracks/data/api_client.dart';
import 'package:lub/features/tracks/data/models/create_track_request.dart';
import 'package:lub/features/tracks/data/models/track_response.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';

class TrackRepository {
  final ApiClient api = ApiClient();

  Future<Track> getTrack(int trackID) async {
    TrackResponse model = await api.getTrack(trackID);
    return model.toEntity();
  }

  Future<List<Track>> getTracks() async {
    List<TrackResponse> models = await api.getTracks();
    List<Track> entities = models.map((item) => item.toEntity()).toList();
    return entities;
  }

  Future<void> createTrack(Track track) async {
    await api.postTracks(CreateTrackRequest.fromEntity(track));
  }
}