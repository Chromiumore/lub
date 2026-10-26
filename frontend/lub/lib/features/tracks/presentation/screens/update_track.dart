import 'package:flutter/material.dart';
import 'package:lub/features/tracks/data/repositories/track_repository.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';
import 'package:lub/features/tracks/presentation/widgets/track_title_form_field.dart';

class UpdateTrackScreen extends StatefulWidget {
  const UpdateTrackScreen({super.key, this.track, required this.trackId});

  final int trackId;
  final Track? track;

  @override
  State<UpdateTrackScreen> createState() => _UpdateTrackScreenState();
}

class _UpdateTrackScreenState extends State<UpdateTrackScreen> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  late final TextEditingController _nameController;

  bool _isLoading = false;

  final TrackRepository _trackRepository = TrackRepository();

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    final track = Track(name: _nameController.text, id: widget.trackId);

    try {
      await _trackRepository.updateTrack(track: track);

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Track uploaded'),
          backgroundColor: Colors.green,
        ),
      );
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Updating error: $e'),
          backgroundColor: Colors.red,
        ),
      );
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController(text: widget.track?.name);
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsetsGeometry.all(16.0),
      child: Form(
        key: _formKey,
        child: Column(
          children: [
            TrackTitleFormField(
              controller: _nameController,
              enabled: !_isLoading,
            ),
            ElevatedButton(
              onPressed: _isLoading ? null : _submit,
              child: _isLoading
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(),
                    )
                  : Text('Send'),
            ),
          ],
        ),
      ),
    );
  }
}
