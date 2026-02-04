import 'package:lub/shared/entities/entity.dart';
import 'package:lub/shared/models/base_model.dart';

abstract interface class ResponseModel implements BaseModel {
  factory ResponseModel.fromJson(Map<String, dynamic> json) {
    throw UnimplementedError();
  }
  Entity toEntity();
}