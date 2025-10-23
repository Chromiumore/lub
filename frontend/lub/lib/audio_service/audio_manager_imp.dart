import 'package:just_audio/just_audio.dart';
import 'package:just_audio_media_kit/just_audio_media_kit.dart';

import 'package:lub/audio_service/audio_manager.dart';


class AudioManagerImp implements AudioManager {
  AudioManagerImp._privateConstructor();
  static final _instance = AudioManagerImp._privateConstructor();

  final AudioPlayer _player = AudioPlayer();

  static AudioManagerImp get instance => _instance;

  @override Future<void> init() async {
    JustAudioMediaKit.ensureInitialized();
  }

  @override
  Future<void> load(String url) async {
    if (_player.sequenceState.currentSource?.tag != url) {
      await _player.setUrl(url, tag: url);
    }
  }

  @override
  void play() {
    _player.play();
  }

  @override
  void pause() {
    _player.pause();
  }

  @override
  void stop() {
    _player.stop();
  }

  @override
  void processControlInput() {
    if (_player.playing) {
      _player.pause();
    } else {
      _player.play();
    }
  }

  @override
  Future<void> dispose() async {
    await _player.dispose();
  }
}