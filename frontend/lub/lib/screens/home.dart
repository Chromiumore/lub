import 'package:flutter/material.dart';
import 'package:dio/dio.dart';

import 'package:lub/models/track.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

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
    final List<dynamic> tracksData = response.data;
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
                } else if (snapshot.hasError) {
                  return Text('Error: ${snapshot.error}');
                } else if (snapshot.hasData) {
                  return Center(
                    child: Column(
                      children: [
                        FlutterLogo(),
                        Expanded(
                          child: SingleChildScrollView(
                            child: DataTable(
                              columns: [
                                DataColumn(label: Text('Name')),
                                DataColumn(label: Text('Author')),
                                DataColumn(label: Text('Listens')),
                                DataColumn(label: Text('Track Length'))
                              ],
                              rows: 
                                snapshot.data!
                                  .map(
                                    (item) => DataRow(cells: [
                                      DataCell(Text(item.name)),
                                      DataCell(Text(item.author.username)),
                                      DataCell(Text(item.listens.toString())),
                                      DataCell(Text(item.track_length.toString())),
                                  ]),
                                ).toList()
                            ),
                          )
                        ),
                      ],
                    ),
                  );
                } else {
                  return Center(
                    child: Text('No data found'),
                  );
                }
              },
            )
    );
  }
}