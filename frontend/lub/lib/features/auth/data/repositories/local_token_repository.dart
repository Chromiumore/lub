import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:lub/features/auth/data/models/tokens_response.dart';

class LocalTokenRepository {
  LocalTokenRepository._privateConstructor();
  static final _instance = LocalTokenRepository._privateConstructor();
  static LocalTokenRepository get instance => _instance;

  final FlutterSecureStorage _storage = FlutterSecureStorage();

  static const String _accessTokenKey = 'access_token';
  static const String _refreshTokenKey = 'refresh_token';

  Future<void> saveTokens(TokensResponse tokens) async {
    saveAccessToken(tokens.accessToken);
    saveRefreshToken(tokens.refreshToken);
  }

  Future<void> saveAccessToken(String token) async {
    await _storage.write(key: _accessTokenKey, value: token);
  }

  Future<void> saveRefreshToken(String token) async {
    await _storage.write(key: _refreshTokenKey, value: token);
  }

  Future<String?> getAccessToken() async {
    return await _storage.read(key: _accessTokenKey);
  }

  Future<String?> getRefreshToken() async {
    return await _storage.read(key: _refreshTokenKey);
  }

  Future<void> deleteAccessToken() async {
    await _storage.delete(key: _accessTokenKey);
  }

  Future<void> deleteRefreshToken() async {
    await _storage.delete(key: _refreshTokenKey);
  }
}
