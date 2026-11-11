import 'package:lub/shared/models/request_model.dart';

class UserLoginRequest implements RequestModel {
  final String email;
  final String password;

  const UserLoginRequest({required this.email, required this.password});

  @override
  Map<String, dynamic> toMap() => {'email': email, 'password': password};
}
