import 'package:lub/shared/entities/entity.dart';

abstract interface class BaseModel {
  factory BaseModel.fromEntity(Entity entity) {
    throw UnimplementedError();   
  }
}