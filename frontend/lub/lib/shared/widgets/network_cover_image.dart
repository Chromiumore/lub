import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';

class NetworkCoverImage extends StatelessWidget {
  const NetworkCoverImage(this.url, {super.key});

  final String url;

  @override
  Widget build(BuildContext context) {
    return CachedNetworkImage(
      imageUrl: url,
      placeholder: (context, url) =>
          const Center(child: CircularProgressIndicator(strokeWidth: 2)),
      errorWidget: (context, url, error) => const Icon(Icons.broken_image),
      fit: BoxFit.cover,
    );
  }
}
