import 'dart:io';
import 'package:path/path.dart' as p;
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:lub/features/tracks/application/services/track_service.dart';
import 'package:lub/features/tracks/presentation/widgets/attach_file_button.dart';

class UpdateTrackCoverScreen extends StatefulWidget {
  const UpdateTrackCoverScreen({super.key, required this.trackId});

  final int trackId;

  @override
  State<UpdateTrackCoverScreen> createState() => _UpdateTrackCoverScreenState();
}

class _UpdateTrackCoverScreenState extends State<UpdateTrackCoverScreen> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  File? _coverFile;
  bool _isLoading = false;

  final TrackService _trackService = TrackService();

  Future<void> _pickCoverFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.image,
    );

    if (result != null) {
      setState(() {
        _coverFile = File(result.files.single.path!);
      });
    }
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      await _trackService.updateCover(
        trackId: widget.trackId,
        coverImageFilePath: _coverFile!.path,
      );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Cover file updated'),
          backgroundColor: Colors.green,
        ),
      );

      _formKey.currentState?.reset();
      setState(() {
        _coverFile = null;
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
              file: _coverFile,
              onAttach: _pickCoverFile,
              onDetach: () => setState(() => _coverFile = null),
              attachLabel: 'Pick new cover image',
              detachLabel: 'Remove cover',
              attachIcon: Icons.image,
              enabled: !_isLoading,
            ),
            FormField<File>(
              validator: (value) {
                if (_coverFile == null) {
                  return 'You should pick the image';
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
              _coverFile != null ? p.basename(_coverFile!.path) : '',
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
