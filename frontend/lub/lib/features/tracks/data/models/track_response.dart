import 'package:lub/features/tracks/domain/entities/track.dart';
import 'package:lub/shared/models/response_model.dart';

import '../../../../shared/models/user.dart';

class TrackResponse implements ResponseModel {
  final int id;
  final String name;
  final int trackLength;
  final User author;
  final int listens;

  TrackResponse({required this.id, required this.name, required this.trackLength, required this.author, required this.listens});

  @override
  factory TrackResponse.fromJson(Map<String, dynamic> json) {
    return TrackResponse(
      id: json['id'] as int,
      name: json['name'] as String,
      trackLength: json['track_length'] as int,
      author: User.fromJson(json['author'] as Map<String, dynamic>),
      listens: json['listens'] as int,
    );
  }

  @override
  factory TrackResponse.fromEntity(Track track) {
    return TrackResponse(
      id: track.id,
      name: track.name,
      trackLength: track.trackLength!,
      author: track.author,
      listens: track.listens!
    );
  }

  @override
  Track toEntity() {
    return Track(id: id, name: name, trackLength: trackLength, author: author, listens: listens);
  }
}