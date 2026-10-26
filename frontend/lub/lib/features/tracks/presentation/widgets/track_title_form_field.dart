import 'package:flutter/material.dart';

class TrackTitleFormField extends StatelessWidget {
  const TrackTitleFormField({
    super.key,
    required this.controller,
    required this.enabled,
  });

  final TextEditingController controller;
  final bool enabled;

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      enabled: enabled,
      decoration: InputDecoration(label: Text('Title')),
      validator: (value) {
        if (value == null || value.isEmpty) return 'Title is required';

        return null;
      },
    );
  }
}
