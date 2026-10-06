import 'package:flutter/foundation.dart';
import 'package:just_audio/just_audio.dart';
import 'package:just_audio_media_kit/just_audio_media_kit.dart';

class AudioPlayerService {
  final AudioPlayer _player = AudioPlayer();

  AudioPlayerService._privateConstructor();
  static final _instance = AudioPlayerService._privateConstructor();
  static AudioPlayerService get instance => _instance;

  final ValueNotifier<int?> _currentTrackId = ValueNotifier<int?>(null);
  ValueListenable<int?> get currentTrackId => _currentTrackId;

  late final Stream<Duration> positionStream = _player.positionStream;
  late final Stream<Duration?> durationStream = _player.durationStream;
  late final Stream<bool> playingStream = _player.playingStream;

  Duration get position => _player.position;
  Duration? get duration => _player.duration;
  bool get isPlaying => _player.playing;

  Future<void> init() async {
    JustAudioMediaKit.ensureInitialized();
  }

  Future<void> load(int id) async {
    if (_player.sequenceState.currentSource?.tag == id) {
      _currentTrackId.value = id;
      return;
    }
    String url = 'http://localhost:8000/api/v1/music/$id/audio';
    await _player.setUrl(url, tag: id);
    _currentTrackId.value = id;
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
    if (_currentTrackId.value == null) return;
    if (_player.playing) {
      _player.pause();
    } else {
      _player.play();
    }
  }

  Future<void> toggleTrack(int id) async {
    if (_currentTrackId.value != id) {
      await load(id);
      await _player.play();
    } else {
      handlePlayButton();
    }
  }

  void handleSeek(double position) {
    if (_currentTrackId.value == null) return;
    _player.seek(Duration(seconds: position.toInt()));
  }

  Future<void> dispose() async {
    await _player.dispose();
    _currentTrackId.dispose();
  }
}
