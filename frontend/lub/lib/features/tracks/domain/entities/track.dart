import 'package:lub/shared/entities/entity.dart';
import 'package:lub/shared/models/user.dart';

class Track extends Entity {
  final int? id;
  final String? name;
  final int? trackLength;
  final User? author;
  final int? listens;

  Track({this.id, this.name, this.trackLength, this.author, this.listens});
}