import 'package:lub/shared/entities/entity.dart';
import 'package:lub/shared/models/base_model.dart';

abstract interface class ResponseModel extends BaseModel {
  Entity toEntity();
}
