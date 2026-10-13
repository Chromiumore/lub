import 'package:file_picker/file_picker.dart';
import 'package:lub/features/tracks/data/models/file_meta_response.dart';
import 'package:lub/features/tracks/domain/entities/file_meta.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';
import 'package:lub/shared/entities/user.dart';
import 'package:lub/shared/models/response_model.dart';
import 'package:lub/shared/models/user_response.dart';

class TrackResponse implements ResponseModel {
  final int id;
  final String name;
  final UserResponse author;
  final List<FileMetaResponse> files;

  TrackResponse({
    required this.id,
    required this.name,
    required this.author,
    required this.files,
  });

  factory TrackResponse.fromMap(Map<String, dynamic> json) {
    return TrackResponse(
      id: json['id'] as int,
      name: json['name'] as String,
      author: UserResponse.fromJson(json['author'] as Map<String, dynamic>),
      files:
          json['files']
                  .map<FileMetaResponse>(
                    (item) => FileMetaResponse.fromMap(item),
                  )
                  .toList()
              as List<FileMetaResponse>,
    );
  }

  @override
  Track toEntity() {
    return Track(
      id: id,
      name: name,
      author: author.toEntity() as User,
      audio:
          files
                  .firstWhere(
                    (f) => FileType.values.byName(f.fileType) == FileType.audio,
                  )
                  .toEntity()
              as FileMeta,
    );
  }
}
