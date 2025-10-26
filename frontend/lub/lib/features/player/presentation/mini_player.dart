import 'package:flutter/material.dart';

class MiniPlayer extends StatefulWidget {
  @override
  State<MiniPlayer> createState() => _MiniPlayerState();
}

class _MiniPlayerState extends State<MiniPlayer> {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Column(
        children: [
          Slider(
            value: 0.5,
            onChanged: (value) {}
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              IconButton(
                onPressed: () => (),
                icon: Icon(Icons.fast_rewind)
              ),
              IconButton(
                onPressed: () => (),
                icon: Icon(Icons.play_arrow)
              ),
              IconButton(
                onPressed: () => (),
                icon: Icon(Icons.fast_forward)
              ),
            ],
          )
        ],
      )
    );
  }
}
