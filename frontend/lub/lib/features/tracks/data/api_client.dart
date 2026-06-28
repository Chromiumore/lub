import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:lub/features/tracks/data/models/create_track_request.dart';
import 'package:lub/features/tracks/data/models/track_response.dart';

class ApiClient {
  final String _host = 'localhost';
  final int _port = 8000;
  static late BaseOptions _options;
  late final Dio _dio;

  ApiClient() {
    _options = BaseOptions(baseUrl: 'http://$_host:$_port/api/v1');
    _dio = Dio(_options);
  }
  
  Future<TrackResponse> getTrack(int trackID) async {
    var response = await _dio
    .get('/music/$trackID');
    TrackResponse track = TrackResponse.fromMap(response.data!);
    return Future.value(track);
  }

  Future<List<TrackResponse>> getTracks() async {
    var response = await _dio
    .get('/music');
    final List<dynamic> tracksData = response.data;
    List<TrackResponse> tracks = tracksData
      .map((item) => TrackResponse.fromMap(item as Map<String, dynamic>))
      .toList();
    return Future.value(tracks);
  }

  Future<void> postTracks(CreateTrackRequest trackModel, String path) async {
    FormData formData = FormData.fromMap({
      'file': await MultipartFile.fromFile(
        path,
        filename: path.split('/').last,
      ),
      'track': jsonEncode(trackModel.toMap()),
    });
    await _dio.post('/music/', data: formData);
  }
}