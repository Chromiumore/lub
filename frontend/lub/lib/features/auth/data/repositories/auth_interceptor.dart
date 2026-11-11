import 'package:dio/dio.dart';
import 'package:lub/features/auth/data/repositories/auth_repository.dart';
import 'package:lub/features/auth/data/repositories/local_token_repository.dart';

class AuthInterceptor extends QueuedInterceptorsWrapper {
  final Dio _dio;
  final Dio _refreshDio;
  final LocalTokenRepository _service = LocalTokenRepository.instance;

  AuthInterceptor(this._dio)
    : _refreshDio = Dio(BaseOptions(baseUrl: _dio.options.baseUrl));

  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    final accessToken = await _service.getAccessToken();
    if (accessToken != null) {
      options.headers['Authorization'] = 'Bearer $accessToken';
    }
    return handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    final isUnauthorized = err.response?.statusCode == 401;
    final isRefreshRequest = err.requestOptions.path.contains(
      AuthRepository.refreshPath,
    );

    if (isUnauthorized && !isRefreshRequest) {
      try {
        final refreshToken = await _service.getRefreshToken();
        if (refreshToken == null) {
          await _service.deleteAccessToken();
          await _service.deleteRefreshToken();
          return handler.next(err);
        }

        final refreshResponse = await _refreshDio.post(
          AuthRepository.refreshPath,
          options: Options(headers: {'Authorization': 'Bearer $refreshToken'}),
        );

        final newAccessToken = refreshResponse.data['access_token'] as String;
        final newRefreshToken =
            refreshResponse.data['refresh_token'] as String?;

        await _service.saveAccessToken(newAccessToken);
        await _service.saveRefreshToken(newRefreshToken ?? refreshToken);

        final requestOptions = err.requestOptions;
        requestOptions.headers['Authorization'] = 'Bearer $newAccessToken';
        final retryResponse = await _dio.fetch(requestOptions);
        return handler.resolve(retryResponse);
      } catch (e) {
        await _service.deleteAccessToken();
        await _service.deleteRefreshToken();
        return handler.next(err);
      }
    }

    return handler.next(err);
  }
}
