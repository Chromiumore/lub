import 'package:file_picker/file_picker.dart';
import 'package:lub/shared/entities/entity.dart';

class FileMeta extends Entity {
  final int? duration;
  late final FileType? fileType;

  FileMeta({this.duration, required String fileTypeName}) {
    fileType = FileType.values.byName(fileTypeName);
  }
}
