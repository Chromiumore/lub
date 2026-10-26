import 'package:lub/features/tracks/domain/entities/track.dart';
import 'package:lub/shared/models/request_model.dart';

class UpdateTrackRequest implements RequestModel {
  final int id;
  final String name;

  const UpdateTrackRequest({required this.id, required this.name});

  factory UpdateTrackRequest.fromEntity(Track track) {
    return UpdateTrackRequest(id: track.id!, name: track.name!);
  }

  @override
  Map<String, dynamic> toMap() {
    return {'name': name};
  }
}
