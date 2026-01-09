import '../../../../shared/models/user.dart';

class Track {
  final int id;
  final String name;
  final int trackLength;
  final User author;
  final int listens;

  Track({required this.id, required this.name, required this.trackLength, required this.author, required this.listens});

  factory Track.fromJson(Map<String, dynamic> json) {
    return Track(
      id: json['id'] as int,
      name: json['name'] as String,
      trackLength: json['track_length'] as int,
      author: User.fromJson(json['author'] as Map<String, dynamic>),
      listens: json['listens'] as int,
    );
  }
}