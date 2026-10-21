import 'package:flutter/material.dart';

class CoverImagePlaceholder extends StatelessWidget {
  const CoverImagePlaceholder({super.key});

  @override
  Widget build(BuildContext context) {
    return Image.asset(
      'assets/images/photosintesis.jpg',
      errorBuilder: (context, exception, stackTrace) =>
          const Icon(Icons.broken_image),
      fit: BoxFit.cover,
    );
  }
}
