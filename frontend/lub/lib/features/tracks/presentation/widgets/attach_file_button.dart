import 'dart:io';

import 'package:flutter/material.dart';

class AttachFileButton extends StatelessWidget {
  const AttachFileButton({
    required this.file,
    required this.onAttach,
    required this.onDetach,
    required this.attachLabel,
    required this.detachLabel,
    required this.attachIcon,
    this.enabled = true,
  });

  final File? file;
  final VoidCallback onAttach;
  final VoidCallback onDetach;
  final String attachLabel;
  final String detachLabel;
  final IconData attachIcon;
  final bool enabled;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final isAttached = file != null;

    final config = isAttached
        ? (
            label: detachLabel,
            icon: Icons.close,
            onPressed: onDetach,
            style: FilledButton.styleFrom(
              backgroundColor: scheme.errorContainer,
              foregroundColor: scheme.onErrorContainer,
            ),
          )
        : (
            label: attachLabel,
            icon: attachIcon,
            onPressed: onAttach,
            style: null,
          );

    return AnimatedSwitcher(
      duration: const Duration(milliseconds: 200),
      transitionBuilder: (child, animation) =>
          FadeTransition(opacity: animation, child: child),
      child: FilledButton.icon(
        key: ValueKey(isAttached),
        onPressed: enabled ? config.onPressed : null,
        style: config.style,
        icon: Icon(config.icon),
        label: Text(config.label),
      ),
    );
  }
}
