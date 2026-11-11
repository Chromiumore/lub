class TokensResponse {
  TokensResponse({required this.accessToken, required this.refreshToken});

  final String accessToken;
  final String refreshToken;

  factory TokensResponse.fromMap(Map<String, dynamic> json) {
    return TokensResponse(
      accessToken: json['access_token'] as String,
      refreshToken: json['refresh_token'] as String,
    );
  }
}
