import 'package:flutter_test/flutter_test.dart';
import 'package:lifeos/core/api_client.dart';

void main() {
  group('ApiClient', () {
    test('should initialize with default base URL', () {
      final client = ApiClient();
      expect(client, isNotNull);
    });

    test('should initialize with custom base URL', () {
      final client = ApiClient(baseUrl: 'http://custom:8000');
      expect(client, isNotNull);
    });
  });
}
