import 'dart:io';
import 'package:path/path.dart' as p;

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:lub/features/tracks/data/repositories/track_repository.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';
import 'package:lub/shared/entities/user.dart';

class UploadTrackScreen extends StatefulWidget {
  const UploadTrackScreen({super.key});

  @override
  State<UploadTrackScreen> createState() => _UploadTrackScreenState();
}

class _UploadTrackScreenState extends State<UploadTrackScreen> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _authorController = TextEditingController();

  File? _audioFile;
  File? _coverImageFile;
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

  Future<void> _pickCoverImageFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.image,
    );

    if (result != null) {
      setState(() {
        _coverImageFile = File(result.files.single.path!);
      });
    }
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    final track = Track(
      name: _nameController.text,
      author: User(id: int.tryParse(_authorController.text)),
    );

    try {
      await _trackRepository.createTrack(
        track: track,
        audioFilePath: _audioFile!.path,
        coverImageFilePath: _coverImageFile?.path,
      );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Track uploaded'),
          backgroundColor: Colors.green,
        ),
      );

      _formKey.currentState?.reset();
      _nameController.clear();
      _authorController.clear();
      setState(() {
        _audioFile = null;
        _coverImageFile = null;
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
      padding: const EdgeInsets.all(16.0),
      child: Form(
        key: _formKey,
        child: Column(
          spacing: 20.0,
          children: [
            TextFormField(
              controller: _nameController,
              enabled: !_isLoading,
              decoration: InputDecoration(label: Text('Title')),
              validator: (value) {
                if (value == null || value.isEmpty) return 'Title is required';

                return null;
              },
            ),
            TextFormField(
              controller: _authorController,
              enabled: !_isLoading,
              decoration: InputDecoration(label: Text('Author ID')),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Author id is required';
                }
                if (int.tryParse(value) == null) {
                  return 'Id must be a not negative integer';
                }

                return null;
              },
            ),

            Row(
              children: [
                SizedBox(
                  width: 150,
                  child: Column(
                    children: [
                      ElevatedButton(
                        onPressed: _isLoading ? null : _pickAudioFile,
                        child: const Text('Pick Audio'),
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
                    ],
                  ),
                ),
                SizedBox(
                  width: 150,
                  child: Column(
                    children: [
                      ElevatedButton(
                        onPressed: _isLoading ? null : _pickCoverImageFile,
                        child: const Text('Pick Cover'),
                      ),
                      Text(
                        _coverImageFile != null
                            ? p.basename(_coverImageFile!.path)
                            : '',
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                ),
              ],
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

  @override
  void dispose() {
    _nameController.dispose();
    _authorController.dispose();
    super.dispose();
  }
}
