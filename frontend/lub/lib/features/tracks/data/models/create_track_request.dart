import 'package:lub/features/tracks/domain/entities/track.dart';
import 'package:lub/shared/models/request_model.dart';

class CreateTrackRequest implements RequestModel {
  final String name;
  final int authorId;

  const CreateTrackRequest({required this.name, required this.authorId});

  @override
  factory CreateTrackRequest.fromEntity(Track track) {
    return CreateTrackRequest(
      name: track.name!,
      authorId: 1
    );
  }

  @override
  Map<String, dynamic> toMap() {
    return {
      'name': name,
      'author_id': authorId,
      // Will be removed later after api update
      'listens': 0,
      'track_length': 180
    };
  }
}