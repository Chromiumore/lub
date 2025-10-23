abstract class AudioManager {
  Future<void> init();
  Future<void> load(String url);
  void play();
  void pause();
  void stop();
  void processControlInput();
  Future<void> dispose();
}