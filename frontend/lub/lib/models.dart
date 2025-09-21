class User {
  final int id;
  final String username;

  User({required this.id, required this.username});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as int,
      username: json['username'] as String,
      );
  }
}


class Track {
  final int id;
  final String name;
  final int track_length;
  final User author;
  final int listens;

  Track({required this.id, required this.name, required this.track_length, required this.author, required this.listens});

  factory Track.fromJson(Map<String, dynamic> json) {
    return Track(
      id: json['id'] as int,
      name: json['name'] as String,
      track_length: json['track_length'] as int,
      author: User.fromJson(json['author'] as Map<String, dynamic>),
      listens: json['listens'] as int,
    );
  }
}