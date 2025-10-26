import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class MyNavigationSidebar extends StatelessWidget {
  const MyNavigationSidebar({super.key});

  @override build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          const DrawerHeader(
            decoration: BoxDecoration(color: Colors.blue),
            child: Text('Goin to...'),
          ),
          ListTile(
            title: const Text('Home'),
            onTap: () => context.go('/'),
          )
        ],
      ),
    );
  }
}