class DioConfig {
  static final String host = 'localhost';
  static final int port = 8000;

  static String get baseUrl => 'http://$host:$port/api/v1';
}
