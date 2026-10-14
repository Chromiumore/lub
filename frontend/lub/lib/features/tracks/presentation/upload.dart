import 'dart:io';

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
              decoration: InputDecoration(label: Text('Title')),
              validator: (value) {
                if (value == null || value.isEmpty) return 'Title is required';

                return null;
              },
            ),
            TextFormField(
              controller: _authorController,
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
                        onPressed: _pickAudioFile,
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
                            return Text(state.errorText!);
                          }
                          return Container();
                        },
                      ),
                      Text(
                        _audioFile != null
                            ? _audioFile!.path.split('\\').last
                            : '',
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
                        onPressed: _pickCoverImageFile,
                        child: const Text('Pick Cover'),
                      ),
                      Text(
                        _coverImageFile != null
                            ? _coverImageFile!.path.split('\\').last
                            : '',
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                ),
              ],
            ),

            ElevatedButton(
              onPressed: () async {
                if (!_formKey.currentState!.validate()) return;

                Track track = Track(
                  name: _nameController.text,
                  author: User(id: int.tryParse(_authorController.text)),
                );
                String audioPath = _audioFile!.path;
                String? coverPath = _coverImageFile?.path;

                _trackRepository.createTrack(
                  track: track,
                  audioFilePath: audioPath,
                  coverImageFilePath: coverPath,
                );
              },
              child: Text('Send'),
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
