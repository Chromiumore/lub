import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:get_it/get_it.dart';
import 'package:just_audio/just_audio.dart';
import 'package:lub/core/api/dio_client.dart';
import 'package:lub/core/api/dio_config.dart';
import 'package:lub/features/auth/application/services/auth_service.dart';
import 'package:lub/features/auth/data/repositories/auth_interceptor.dart';
import 'package:lub/features/auth/data/repositories/auth_repository.dart';
import 'package:lub/features/auth/data/repositories/local_token_repository.dart';
import 'package:lub/features/player/application/audio_player_service.dart';
import 'package:lub/features/tracks/application/services/track_service.dart';
import 'package:lub/features/tracks/data/repositories/track_repository.dart';

class InjectionService {
  static final locator = GetIt.instance;

  static void configureDependencies() {
    locator
      ..registerLazySingleton<Dio>(DioClient.create)
      ..registerLazySingleton<TrackRepository>(() => TrackRepository(locator()))
      ..registerLazySingleton<TrackService>(() => TrackService(locator()))
      ..registerLazySingleton<AudioPlayer>(() => AudioPlayer())
      ..registerLazySingleton<AudioPlayerService>(
        () => AudioPlayerService(locator()),
      )
      ..registerLazySingleton<FlutterSecureStorage>(
        () => FlutterSecureStorage(),
      )
      ..registerLazySingleton<AuthRepository>(() => AuthRepository(locator()))
      ..registerLazySingleton<LocalTokenRepository>(
        () => LocalTokenRepository(locator()),
      )
      ..registerLazySingleton<AuthInterceptor>(
        () => AuthInterceptor(locator(), locator()),
      )
      ..registerLazySingleton<AuthService>(
        () => AuthService(locator(), locator()),
      );
  }
}
