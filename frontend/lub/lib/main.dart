import 'package:dio/dio.dart';
import 'package:flutter/material.dart';

import 'models.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late Future<List<Track>> _tracks;

  @override
  void initState() {
    super.initState();
    _tracks = getTracks();
  }

  Future<List<Track>> getTracks() async {
    var response = await Dio()
    .get('http://localhost:8000/music');
    final List<dynamic> tracksData = response.data['tracks'];
    List<Track> tracks = tracksData
      .map((item) => Track.fromJson(item as Map<String, dynamic>))
      .toList();
    return Future.value(tracks);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Test App"),),
      body: FutureBuilder<List<Track>>(
              future: _tracks,
              builder:(context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return Center(child: CircularProgressIndicator());
                } else {
                  return Column(
                    children: [
                      FlutterLogo(),
                      Expanded(
                        child: ListView.builder(
                        itemCount: snapshot.data!.length,
                        itemBuilder: (context, index) {
                          return Container(
                            alignment: Alignment.center, 
                            child: Text(
                              snapshot.data![index].name
                            )
                          );
                        }
                      ),
                      ),
                    ],
                  );
                }
              },
            )
    );
  }
}
