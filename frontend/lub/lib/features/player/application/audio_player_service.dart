import 'package:just_audio/just_audio.dart';
import 'package:just_audio_media_kit/just_audio_media_kit.dart';

class AudioPlayerService {
  final AudioPlayer _player = AudioPlayer();

  AudioPlayerService._privateConstructor();
  static final _instance = AudioPlayerService._privateConstructor();

  static AudioPlayerService get instance => _instance;
  Stream<Duration> get positionStream => _player.positionStream;
  Stream<Duration?> get durationStream => _player.durationStream;
  Stream<bool> get playingStream => _player.playingStream;

  Duration get position => _player.position;
  Duration? get duration => _player.duration;
  bool get isPlaying => _player.playing;

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

  void handlePlayButton() {
    if (_player.playing) {
      _player.pause();
    } else {
      _player.play();
    }
  }

  void handleSeek(double position) {
    _player.seek(Duration(seconds: position.toInt()));
  }

  Future<void> dispose() async {
    await _player.dispose();
  }
}
