import 'package:lub/shared/models/user.dart';

class Track {
  final int id;
  final String name;
  final int trackLength;
  final User author;
  final int listens;

  Track({required this.id, required this.name, required this.trackLength, required this.author, required this.listens});
}