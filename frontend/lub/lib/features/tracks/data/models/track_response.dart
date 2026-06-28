import 'package:lub/features/tracks/domain/entities/track.dart';
import 'package:lub/shared/models/response_model.dart';

import '../../../../shared/models/user.dart';

class TrackResponse implements ResponseModel {
  final int id;
  final String name;
  final User author;

  TrackResponse({required this.id, required this.name, required this.author});

  @override
  factory TrackResponse.fromMap(Map<String, dynamic> json) {
    return TrackResponse(
      id: json['id'] as int,
      name: json['name'] as String,
      author: User.fromJson(json['author'] as Map<String, dynamic>),
    );
  }

  @override
  factory TrackResponse.fromEntity(Track track) {
    return TrackResponse(
      id: track.id!,
      name: track.name!,
      author: track.author!
    );
  }

  @override
  Track toEntity() {
    return Track(id: id, name: name, author: author);
  }
}