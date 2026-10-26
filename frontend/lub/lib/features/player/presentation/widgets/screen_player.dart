import 'package:flutter/material.dart';
import 'package:lub/features/player/application/audio_player_service.dart';
import 'package:lub/features/player/presentation/widgets/player_controls.dart';
import 'package:lub/features/player/presentation/widgets/player_slider.dart';
import 'package:lub/features/tracks/data/api_client.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';
import 'package:lub/shared/widgets/cover_image_placeholder.dart';
import 'package:lub/shared/widgets/network_cover_image.dart';

class ScreenPlayer extends StatelessWidget {
  ScreenPlayer({super.key, required this.track});

  final Track track;
  final ApiClient _api = ApiClient();

  @override
  Widget build(BuildContext context) {
    final playerService = AudioPlayerService.instance;
    return Card(
      child: Padding(
        padding: const EdgeInsets.only(top: 24),
        child: Column(
          children: [
            SizedBox(
              width: 300,
              height: 300,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(15),
                child: track.hasCover
                    ? NetworkCoverImage(_api.getCoverDownloadUrl(track.id!))
                    : CoverImagePlaceholder(),
              ),
            ),
            Text(track.name!, style: const TextStyle(fontSize: 20)),
            Text(track.author!.username!),
            PlayerSlider(playerService: playerService, track: track),
            Padding(
              padding: const EdgeInsets.only(left: 25, right: 25),
              child: PlayerControls(playerService: playerService, track: track),
            ),
          ],
        ),
      ),
    );
  }
}
