import 'package:dio/dio.dart';
import 'package:lub/features/auth/data/models/tokens_response.dart';
import 'package:lub/features/auth/data/models/user_login_request.dart';
import 'package:lub/features/auth/data/models/user_register_request.dart';

class AuthRepository {
  AuthRepository(this._dio);

  final Dio _dio;

  static const refreshPath = '/refresh';

  Future<TokensResponse> login(UserLoginRequest request) async {
    var response = await _dio.post('/login', data: request.toMap());
    TokensResponse tokens = TokensResponse.fromMap(response.data!);
    return Future.value(tokens);
  }

  Future<void> register(UserRegisterRequest request) async {
    await _dio.post('/register', data: request.toMap());
  }

  Future<void> refresh(String refreshToken) async {
    await _dio.get(
      '/refresh',
      options: Options(headers: {'Authorization': 'Bearer $refreshToken'}),
    );
  }
}
