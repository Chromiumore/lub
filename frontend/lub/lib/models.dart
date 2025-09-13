class Track {
  final int id;
  final String name;
  final int track_length;
  final int author_id;
  final int listens;

  Track({required this.id, required this.name, required this.track_length, required this.author_id, required this.listens});

  factory Track.fromJson(Map<String, dynamic> json) {
    return Track(
      id: json['id'] as int,
      name: json['name'] as String,
      track_length: json['track_length'] as int,
      author_id: json['author_id'] as int,
      listens: json['listens'] as int,
    );
  }
}