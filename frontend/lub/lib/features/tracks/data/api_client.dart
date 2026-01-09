import 'package:dio/dio.dart';
import 'package:lub/features/tracks/data/models/track.dart';

class ApiClient {
  final String _host = 'localhost';
  final int _port = 8000;
  static late BaseOptions _options;
  late final Dio _dio;

  ApiClient() {
    _options = BaseOptions(baseUrl: 'http://$_host:$_port');
    _dio = Dio(_options);
  }
  
  Future<TrackModel> getTrack(int trackID) async {
    var response = await _dio
    .get('/music/$trackID');
    TrackModel track = TrackModel.fromJson(response.data!);
    return Future.value(track);
  }

  Future<List<TrackModel>> getTracks() async {
    var response = await _dio
    .get('/music');
    final List<dynamic> tracksData = response.data;
    List<TrackModel> tracks = tracksData
      .map((item) => TrackModel.fromJson(item as Map<String, dynamic>))
      .toList();
    return Future.value(tracks);
  }
}