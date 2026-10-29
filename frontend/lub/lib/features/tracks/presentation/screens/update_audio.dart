import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:lub/features/tracks/data/repositories/track_repository.dart';
import 'package:path/path.dart' as p;
import 'package:flutter/material.dart';
import 'package:lub/features/tracks/presentation/widgets/attach_file_button.dart';

class UpdateTrackAudioScreen extends StatefulWidget {
  const UpdateTrackAudioScreen({super.key, required this.trackId});

  final int trackId;

  @override
  State<UpdateTrackAudioScreen> createState() => _UpdateTrackAudioScreenState();
}

class _UpdateTrackAudioScreenState extends State<UpdateTrackAudioScreen> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  File? _audioFile;
  bool _isLoading = false;

  final TrackRepository _trackRepository = TrackRepository();

  Future<void> _pickAudioFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.audio,
    );

    if (result != null) {
      setState(() {
        _audioFile = File(result.files.single.path!);
      });
    }
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      await _trackRepository.updateAudio(
        trackId: widget.trackId,
        audioFilePath: _audioFile!.path,
      );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Audio file updated'),
          backgroundColor: Colors.green,
        ),
      );

      _formKey.currentState?.reset();
      setState(() {
        _audioFile = null;
      });
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Uploading error: $e'),
          backgroundColor: Colors.red,
        ),
      );
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsetsGeometry.all(16),
      child: Form(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            AttachFileButton(
              file: _audioFile,
              onAttach: _pickAudioFile,
              onDetach: () => setState(() => _audioFile = null),
              attachLabel: 'Pick new audio',
              detachLabel: 'Remove audio',
              attachIcon: Icons.audiotrack,
              enabled: !_isLoading,
            ),
            FormField<File>(
              validator: (value) {
                if (_audioFile == null) {
                  return 'We wanna hear it';
                }
                return null;
              },
              builder: (FormFieldState<File> state) {
                if (state.errorText != null) {
                  return Text(
                    state.errorText!,
                    style: TextStyle(color: Colors.red),
                  );
                }
                return SizedBox.shrink();
              },
            ),
            Text(
              _audioFile != null ? p.basename(_audioFile!.path) : '',
              overflow: TextOverflow.ellipsis,
            ),

            ElevatedButton(
              onPressed: _isLoading ? null : _submit,
              child: _isLoading
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(),
                    )
                  : Text('Save'),
            ),
          ],
        ),
      ),
    );
  }
}
