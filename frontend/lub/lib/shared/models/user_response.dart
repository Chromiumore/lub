import 'package:lub/shared/entities/entity.dart';
import 'package:lub/shared/entities/user.dart';
import 'package:lub/shared/models/response_model.dart';

class UserResponse implements ResponseModel {
  final int id;
  final String username;

  UserResponse({required this.id, required this.username});

  factory UserResponse.fromJson(Map<String, dynamic> json) {
    return UserResponse(
      id: json['id'] as int,
      username: json['username'] as String,
    );
  }

  @override
  Entity toEntity() {
    return User(id: id, username: username);
  }
}
