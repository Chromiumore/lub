import 'package:lub/features/tracks/data/repositories/track_repository.dart';
import 'package:lub/features/tracks/data/models/create_track_request.dart';
import 'package:lub/features/tracks/data/models/track_response.dart';
import 'package:lub/features/tracks/data/models/update_track_request.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';

class TrackService {
  final TrackRepository _repository = TrackRepository();

  Future<Track> getTrack(int trackID) async {
    TrackResponse model = await _repository.getTrack(trackID);
    return model.toEntity();
  }

  Future<List<Track>> getTracks() async {
    List<TrackResponse> models = await _repository.getTracks();
    List<Track> entities = models.map((item) => item.toEntity()).toList();
    return entities;
  }

  Future<Track> createTrack({
    required Track track,
    required String audioFilePath,
    String? coverImageFilePath,
  }) async {
    var model = await _repository.postTracks(
      trackModel: CreateTrackRequest.fromEntity(track),
      audioFilePath: audioFilePath,
      authorId: 1,
      coverImageFilePath: coverImageFilePath,
    );

    return model.toEntity();
  }

  Future<Track> updateTrack({required Track track}) async {
    var model = await _repository.putTrack(
      updateModel: UpdateTrackRequest.fromEntity(track),
    );

    return model.toEntity();
  }

  Future<void> updateAudio({
    required int trackId,
    required String audioFilePath,
  }) async {
    await _repository.putAudio(trackId: trackId, audioFilePath: audioFilePath);
  }

  Future<void> updateCover({
    required int trackId,
    required String coverImageFilePath,
  }) async {
    await _repository.putCover(
      trackId: trackId,
      coverImageFilePath: coverImageFilePath,
    );
  }

  Future<void> deleteTrack(int id) async {
    await _repository.deleteTrack(id);
  }
}
