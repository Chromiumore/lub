import 'package:lub/features/tracks/domain/entities/file_meta.dart';
import 'package:lub/shared/entities/entity.dart';
import 'package:lub/shared/entities/user.dart';

class Track extends Entity {
  final int? id;
  final String? name;
  final User? author;
  final FileMeta? audio;

  Track({this.id, this.name, this.author, this.audio});
}
