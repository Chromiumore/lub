import 'package:lub/features/tracks/domain/entities/track.dart';

import '../../../../shared/models/user.dart';

class TrackModel {
  final int id;
  final String name;
  final int trackLength;
  final User author;
  final int listens;

  TrackModel({required this.id, required this.name, required this.trackLength, required this.author, required this.listens});

  factory TrackModel.fromJson(Map<String, dynamic> json) {
    return TrackModel(
      id: json['id'] as int,
      name: json['name'] as String,
      trackLength: json['track_length'] as int,
      author: User.fromJson(json['author'] as Map<String, dynamic>),
      listens: json['listens'] as int,
    );
  }

  Track toEntity() {
    return Track(id: id, name: name, trackLength: trackLength, author: author, listens: listens);
  }
}