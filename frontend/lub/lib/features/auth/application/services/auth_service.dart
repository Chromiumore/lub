import 'package:lub/features/auth/data/models/tokens_response.dart';
import 'package:lub/features/auth/data/models/user_login_request.dart';
import 'package:lub/features/auth/data/models/user_register_request.dart';
import 'package:lub/features/auth/data/repositories/auth_repository.dart';
import 'package:lub/features/auth/data/repositories/local_token_repository.dart';

class AuthService {
  AuthService(this._tokenRepository, this._authRepository);

  final LocalTokenRepository _tokenRepository;
  final AuthRepository _authRepository;

  Future<void> login(UserLoginRequest request) async {
    TokensResponse tokens = await _authRepository.login(request);
    _tokenRepository.saveTokens(tokens);
  }

  Future<void> register(UserRegisterRequest request) async {
    await _authRepository.register(request);
  }
}
