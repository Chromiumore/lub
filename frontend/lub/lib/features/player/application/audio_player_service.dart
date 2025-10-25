import 'package:just_audio/just_audio.dart';
import 'package:just_audio_media_kit/just_audio_media_kit.dart';


class AudioPlayerService {
  AudioPlayerService._privateConstructor();
  static final _instance = AudioPlayerService._privateConstructor();

  final AudioPlayer _player = AudioPlayer();

  static AudioPlayerService get instance => _instance;

  Future<void> init() async {
    JustAudioMediaKit.ensureInitialized();
  }

  Future<void> load(String url) async {
    if (_player.sequenceState.currentSource?.tag != url) {
      await _player.setUrl(url, tag: url);
    }
  }

  void play() {
    _player.play();
  }

  void pause() {
    _player.pause();
  }

  void stop() {
    _player.stop();
  }

  void processControlInput() {
    if (_player.playing) {
      _player.pause();
    } else {
      _player.play();
    }
  }

  Future<void> dispose() async {
    await _player.dispose();
  }
}