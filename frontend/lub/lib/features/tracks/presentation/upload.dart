import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:lub/features/tracks/data/repositories/track_repository.dart';
import 'package:lub/features/tracks/domain/entities/track.dart';

class UploadTrackScreen extends StatefulWidget {
  const UploadTrackScreen({super.key});

  @override
  State<UploadTrackScreen> createState() => _UploadTrackScreenState();
}

class _UploadTrackScreenState extends State<UploadTrackScreen> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  final TextEditingController _nameController = TextEditingController();
  File? _trackFile;

  final TrackRepository _trackRepository = TrackRepository();

  Future<void> _pickFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.audio,
    );

    if (result != null) {
      setState(() {
        _trackFile = File(result.files.single.path!);
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
              decoration: InputDecoration(
                label: Text('Title'),
              ),
            ),

            Container(
              alignment: Alignment.centerLeft,
              child: ElevatedButton(
                onPressed: _pickFile,
                child: const Text('Pick File'),
              ),
            ),
            FormField<File>(
              validator: (value) {
                if (_trackFile == null) {
                  return 'We wanna hear it';
                }
                return null;
              },
              builder: (FormFieldState<File> state) {
                if (state.errorText != null) {
                  return Text(state.errorText!);
                }
                return Container();
              }
            ),

            ElevatedButton(
              onPressed: () async {
                Track track = Track(name: _nameController.text);
                String path = _trackFile!.path;
                
                _trackRepository.createTrack(track, path);
              },
              child: Text('Send')
            ),
          ],
        )
      ),
    );
  }

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }
}