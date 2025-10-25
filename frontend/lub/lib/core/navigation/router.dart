import 'package:go_router/go_router.dart';

import '../../features/tracks/presentation/home.dart';
import '../../features/tracks/presentation/track.dart';
import '../widgets/navigation_sidebar.dart';


final router = GoRouter(
  routes: [
    ShellRoute(
      builder: (context, state, child) {
        return MyNavigationSidebar(child: child);
      },
      routes: [
        GoRoute(
          path: '/',
          builder: (context, state) => HomeScreen(),
        ),
        GoRoute(
          path: '/music/:trackID',
          builder: (context, state) => TrackScreen(trackID: int.parse(state.pathParameters['trackID']!)),
        ),
      ]
    )
  ],
);