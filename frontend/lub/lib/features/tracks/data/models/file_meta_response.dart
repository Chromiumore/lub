import 'package:lub/features/tracks/domain/entities/file_meta.dart';
import 'package:lub/shared/entities/entity.dart';
import 'package:lub/shared/models/response_model.dart';

class FileMetaResponse implements ResponseModel {
  final int? duration;
  final String fileType;

  FileMetaResponse({required this.duration, required this.fileType});

  factory FileMetaResponse.fromMap(Map<String, dynamic> json) {
    return FileMetaResponse(
      duration: json['duration'] as int?,
      fileType: json['file_type'] as String,
    );
  }

  @override
  Entity toEntity() {
    return FileMeta(fileTypeName: fileType, duration: duration);
  }
}
