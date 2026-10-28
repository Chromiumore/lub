import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:lub/features/tracks/data/models/create_track_request.dart';
import 'package:lub/features/tracks/data/models/track_response.dart';
import 'package:lub/features/tracks/data/models/update_track_request.dart';

class ApiClient {
  final String _host = 'localhost';
  final int _port = 8000;
  static late BaseOptions _options;
  late final Dio _dio;

  String get baseUrl => 'http://$_host:$_port/api/v1';

  ApiClient() {
    _options = BaseOptions(baseUrl: baseUrl);
    _dio = Dio(_options);
  }

  Future<TrackResponse> getTrack(int trackID) async {
    var response = await _dio.get('/music/$trackID');
    TrackResponse track = TrackResponse.fromMap(response.data!);
    return Future.value(track);
  }

  Future<List<TrackResponse>> getTracks() async {
    var response = await _dio.get('/music');
    final List<dynamic> tracksData = response.data;
    List<TrackResponse> tracks = tracksData
        .map((item) => TrackResponse.fromMap(item as Map<String, dynamic>))
        .toList();
    return Future.value(tracks);
  }

  Future<TrackResponse> postTracks({
    required CreateTrackRequest trackModel,
    required String audioFilePath,
    required int authorId,
    String? coverImageFilePath,
  }) async {
    Map<String, dynamic> data = {
      'audio_file': await MultipartFile.fromFile(
        audioFilePath,
        filename: audioFilePath.split('/').last,
      ),
      'track': jsonEncode(trackModel.toMap()),
    };

    if (coverImageFilePath != null) {
      data['cover_image'] = await MultipartFile.fromFile(
        coverImageFilePath,
        filename: coverImageFilePath.split('/').last,
      );
    }

    try {
      FormData formData = FormData.fromMap(data);
      var response = await _dio.post('/music/', data: formData);
      TrackResponse track = TrackResponse.fromMap(response.data!);
      return Future.value(track);
    } on DioException catch (e) {
      if (e.response != null) {
        print('Status Code: ${e.response?.statusCode}');
        print('Response Data: ${e.response?.data}');
        print('Response Headers: ${e.response?.headers}');
      }
      rethrow;
    }
  }

  Future<TrackResponse> putTrack({
    required UpdateTrackRequest updateModel,
  }) async {
    var response = await _dio.put(
      '/music/${updateModel.id}',
      data: updateModel.toMap(),
    );
    TrackResponse track = TrackResponse.fromMap(response.data!);
    return Future.value(track);
  }

  Future<void> deleteTrack(int id) async {
    await _dio.delete('/music/$id/');
  }

  String getCoverDownloadUrl(int trackId) {
    return '$baseUrl/music/$trackId/cover';
  }
}
