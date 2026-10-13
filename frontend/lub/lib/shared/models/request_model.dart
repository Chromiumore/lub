import 'package:lub/shared/models/base_model.dart';

abstract interface class RequestModel extends BaseModel {
  Map<String, dynamic> toMap();
}
