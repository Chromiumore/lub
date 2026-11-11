import 'package:lub/features/auth/data/models/user_login_request.dart';

class UserRegisterRequest extends UserLoginRequest {
  UserRegisterRequest({
    required this.username,
    required super.email,
    required super.password,
  });

  final String username;

  @override
  Map<String, dynamic> toMap() {
    Map<String, dynamic> map = super.toMap();
    map['username'] = username;
    return map;
  }
}
