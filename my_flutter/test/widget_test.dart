// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility that Flutter provides. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:my_app/main.dart';

void main() {
  testWidgets('Timer increments smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(
      ChangeNotifierProvider(
        create: (_) => StopwatchModel(),
        child: MyApp(),
      ),
    );

    // Verify that our timer starts at 0.
    expect(find.text('0 seconds'), findsOneWidget);
    expect(find.text('1 seconds'), findsNothing);

    // Tap the 'Start' button and trigger a frame.
    await tester.tap(find.text('Start'));
    await tester.pump();

    // Wait for 1 second and pump the timer.
    await tester.pump(Duration(seconds: 1));

    // Verify that our timer has incremented.
    expect(find.text('0 seconds'), findsNothing);
    expect(find.text('1 seconds'), findsOneWidget);

    // Stop the timer.
    await tester.tap(find.text('Stop'));
    await tester.pump();

    // Wait for another second and verify that timer has not incremented.
    await tester.pump(Duration(seconds: 1));
    expect(find.text('1 seconds'), findsOneWidget);
    expect(find.text('2 seconds'), findsNothing);

    // Reset the timer and verify it goes back to 0.
    await tester.tap(find.text('Reset'));
    await tester.pump();
    expect(find.text('0 seconds'), findsOneWidget);
  });
}
