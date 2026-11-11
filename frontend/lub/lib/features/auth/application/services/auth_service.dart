import 'package:lub/features/auth/data/repositories/auth_repository.dart';
import 'package:lub/features/auth/data/repositories/local_token_repository.dart';

class AuthService {
  final LocalTokenRepository tokenService = LocalTokenRepository.instance;
  final AuthRepository _authRepository = AuthRepository();

  Future<void> login(String username, String email, String password) async {}
}
