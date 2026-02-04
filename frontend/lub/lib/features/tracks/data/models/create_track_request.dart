import 'package:lub/features/tracks/domain/entities/track.dart';
import 'package:lub/shared/models/request_model.dart';
import 'package:lub/shared/models/user.dart';

class CreateTrackRequest implements RequestModel {
  final String name;
  final int authorId;

  const CreateTrackRequest({required this.name, required this.authorId});

  @override
  factory CreateTrackRequest.fromJson(Map<String, dynamic> json) {
    return CreateTrackRequest(
      name: json['name'] as String,
      authorId: User.fromJson(json['author'] as Map<String, dynamic>).id
    );
  }

  @override
  factory CreateTrackRequest.fromEntity(Track track) {
    return CreateTrackRequest(
      name: track.name,
      authorId: track.author.id
    );
  }

  @override
  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'author_id': authorId
    };
  }
}