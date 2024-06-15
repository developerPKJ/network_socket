import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class Record {
  String time;
  String memo;

  Record(this.time, this.memo);
}

class WeatherInfo {
  final double temperature;
  final String description;
  final String icon;
  final double feelsLike;
  final int humidity;
  final String location;

  WeatherInfo({
    required this.temperature,
    required this.description,
    required this.icon,
    required this.feelsLike,
    required this.humidity,
    required this.location,
  });
}

//스탑워치 기능
class StopwatchModel with ChangeNotifier {
  int _milliseconds = 0;
  Timer? _timer;
  List<Record> _records = [];
  List<String> _lapTimes = [];
  WeatherInfo? _weatherInfo;

  int get milliseconds => _milliseconds;
  List<Record> get records => _records;
  List<String> get lapTimes => _lapTimes;
  WeatherInfo? get weatherInfo => _weatherInfo;

  void startStopwatch() {
    _timer = Timer.periodic(Duration(milliseconds: 10), (timer) {
      _milliseconds += 10;
      notifyListeners();
    });
  }

  void stopStopwatch() {
    _timer?.cancel();
    notifyListeners();
  }

  void resetStopwatch() {
    _timer?.cancel();
    _milliseconds = 0;
    _lapTimes.clear();
    notifyListeners();
  }

  void saveRecord(String memo) {
    _records.add(Record('${(_milliseconds / 1000).toStringAsFixed(2)} sec', memo));
    notifyListeners();
  }

  void deleteRecord(int index) {
    _records.removeAt(index);
    notifyListeners();
  }

  void updateMemo(int index, String memo) {
    _records[index].memo = memo;
    notifyListeners();
  }

  void recordLapTime() {
    _lapTimes.add('${(_milliseconds / 1000).toStringAsFixed(2)} sec');
    notifyListeners();
  }

//OpenWeather API
  Future<void> fetchWeather() async {
    final url = 'https://api.openweathermap.org/data/2.5/weather?q=Seoul,kr&appid=2604fb21af6eb97a4271a1048c1667d1&units=metric';

    try {
      final response = await http.get(Uri.parse(url));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final temp = data['main']['temp'];
        final description = data['weather'][0]['description'];
        final icon = data['weather'][0]['icon'];
        final feelsLike = data['main']['feels_like'];
        final humidity = data['main']['humidity'];
        final location = data['name'];
        _weatherInfo = WeatherInfo(
          temperature: temp,
          description: description,
          icon: icon,
          feelsLike: feelsLike,
          humidity: humidity,
          location: location,
        );
      } else {
        _weatherInfo = WeatherInfo(
          temperature: 0,
          description: 'Failed to fetch weather. Status code: ${response.statusCode}.',
          icon: '',
          feelsLike: 0,
          humidity: 0,
          location: '',
        );
      }
    } catch (e) {
      _weatherInfo = WeatherInfo(
        temperature: 0,
        description: 'Error: $e',
        icon: '',
        feelsLike: 0,
        humidity: 0,
        location: '',
      );
    }
    notifyListeners();
  }
}

//테마 기능
class ThemeModel with ChangeNotifier {
  bool _isDarkTheme = true;

  bool get isDarkTheme => _isDarkTheme;

  void toggleTheme() {
    _isDarkTheme = !_isDarkTheme;
    notifyListeners();
  }
}

//page
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => StopwatchModel()),
        ChangeNotifierProvider(create: (_) => ThemeModel()),
      ],
      child: Consumer<ThemeModel>(
        builder: (context, themeModel, child) {
          return MaterialApp(
            theme: ThemeData.light(),
            darkTheme: ThemeData.dark(),
            themeMode: themeModel.isDarkTheme ? ThemeMode.dark : ThemeMode.light,
            home: HomePage(),
          );
        },
      ),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          NavigationRail(
            minWidth: 100,
            selectedIndex: _selectedIndex,
            onDestinationSelected: (int index) {
              setState(() {
                _selectedIndex = index;
              });
            },
            labelType: NavigationRailLabelType.selected,
            destinations: [
              NavigationRailDestination(
                icon: Icon(Icons.timer),
                selectedIcon: Icon(Icons.timer),
                label: Text('Stopwatch'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.list),
                selectedIcon: Icon(Icons.list),
                label: Text('Records'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.settings),
                selectedIcon: Icon(Icons.settings),
                label: Text('Settings'),
              ),
            ],
          ),
          Expanded(
            child: _selectedIndex == 0
                ? StopwatchScreen()
                : _selectedIndex == 1
                    ? RecordsScreen()
                    : SettingsScreen(),
          ),
        ],
      ),
    );
  }
}

//스탑워치 메인 레일
class StopwatchScreen extends StatelessWidget {
  final TextEditingController _memoController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    final stopwatchModel = Provider.of<StopwatchModel>(context);

    // fetchWeather를 화면이 빌드될 때 호출
    if (stopwatchModel.weatherInfo == null) {
      stopwatchModel.fetchWeather();
    }

    return Scaffold(
      appBar: AppBar(
        title: Text('Stopwatch App'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              '${(stopwatchModel.milliseconds / 1000).toStringAsFixed(2)} sec',
              style: TextStyle(fontSize: 48),
            ),
            SizedBox(height: 20),
            TextField(
              controller: _memoController,
              textAlign: TextAlign.center,
              decoration: InputDecoration(
                hintText: 'Enter memo',
                filled: true,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                  borderSide: BorderSide.none,
                ),
                contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                alignLabelWithHint: true,
              ),
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                stopwatchModel._timer == null || !stopwatchModel._timer!.isActive
                    ? ElevatedButton(
                        onPressed: stopwatchModel.startStopwatch,
                        child: Text('Start'),
                      )
                    : ElevatedButton(
                        onPressed: stopwatchModel.stopStopwatch,
                        child: Text('Stop'),
                      ),
                SizedBox(width: 10),
                ElevatedButton(
                  onPressed: stopwatchModel.resetStopwatch,
                  child: Text('Reset'),
                ),
                SizedBox(width: 10),
                ElevatedButton(
                  onPressed: () {
                    stopwatchModel.saveRecord(_memoController.text);
                    _memoController.clear();
                  },
                  child: Text('Save Record'),
                ),
                SizedBox(width: 10),
                ElevatedButton(
                  onPressed: stopwatchModel.recordLapTime,
                  child: Text('Lap'),
                ),
              ],
            ),
            SizedBox(height: 20),
            if (stopwatchModel.weatherInfo != null) ...[
              Text(
                stopwatchModel.weatherInfo!.location,
                style: TextStyle(fontSize: 24),
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    '${stopwatchModel.weatherInfo!.temperature}°',
                    style: TextStyle(fontSize: 48),
                  ),
                  Image.network(
                    'https://openweathermap.org/img/wn/${stopwatchModel.weatherInfo!.icon}@2x.png',
                  ),
                ],
              ),
              Text(
                '(체감 온도: ${stopwatchModel.weatherInfo!.feelsLike}°)',
                style: TextStyle(fontSize: 16),
              ),
              Text(
                '습도: ${stopwatchModel.weatherInfo!.humidity}%',
                style: TextStyle(fontSize: 16),
              ),
            ] else ...[
              Text(
                '날씨 불러오는 중...',
                style: TextStyle(fontSize: 20),
              ),
            ],
            SizedBox(height: 20),
            Expanded(
              child: ListView.builder(
                itemCount: stopwatchModel.lapTimes.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text('Lap ${index + 1}: ${stopwatchModel.lapTimes[index]}'),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

//기록 레일
class RecordsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final stopwatchModel = Provider.of<StopwatchModel>(context);
    return Scaffold(
      appBar: AppBar(
        title: Text('Records'),
      ),
      body: Center(
        child: ListView.builder(
          itemCount: stopwatchModel.records.length,
          itemBuilder: (context, index) {
            final record = stopwatchModel.records[index];
            final TextEditingController _memoController = TextEditingController(text: record.memo);
            return ListTile(
              title: Text(record.time),
              subtitle: TextField(
                controller: _memoController,
                textAlign: TextAlign.center,
                decoration: InputDecoration(
                  hintText: 'Enter memo',
                  filled: true,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(10),
                    borderSide: BorderSide.none,
                  ),
                  contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  alignLabelWithHint: true,
                ),
                onSubmitted: (value) {
                  stopwatchModel.updateMemo(index, value);
                },
              ),
              trailing: IconButton(
                icon: Icon(Icons.delete),
                onPressed: () {
                  stopwatchModel.deleteRecord(index);
                },
              ),
            );
          },
        ),
      ),
    );
  }
}

//설정 레일
class SettingsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final themeModel = Provider.of<ThemeModel>(context);
    return Scaffold(
      appBar: AppBar(
        title: Text('Settings'),
      ),
      body: Center(
        child: SwitchListTile(
          title: Text('Dark Theme'),
          value: themeModel.isDarkTheme,
          onChanged: (value) {
            themeModel.toggleTheme();
          },
        ),
      ),
    );
  }
}
