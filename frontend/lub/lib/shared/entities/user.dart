import 'package:lub/shared/entities/entity.dart';

class User extends Entity {
  final int? id;
  final String? username;

  User({this.id, this.username});
}
