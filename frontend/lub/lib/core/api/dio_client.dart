import 'package:dio/dio.dart';
import 'package:lub/core/api/dio_config.dart';

class DioClient {
  static Dio create() {
    return Dio(BaseOptions(baseUrl: DioConfig.baseUrl));
  }
}
