import 'package:lub/shared/entities/entity.dart';
import 'package:lub/shared/models/user.dart';

class Track extends Entity {
  final int? id;
  final String? name;
  final User? author;

  Track({this.id, this.name, this.author});
}