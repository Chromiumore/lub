import 'package:lub/shared/models/base_model.dart';

abstract interface class RequestModel implements BaseModel {
  Map<String, dynamic> toJson();
}