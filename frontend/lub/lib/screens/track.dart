import 'package:flutter/material.dart';

class TrackScreen extends StatelessWidget {
  final int trackID;

  const TrackScreen({super.key, required this.trackID});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: [
            Text(trackID.toString()),
          ],
        ),
      ),
    );
  }
}
