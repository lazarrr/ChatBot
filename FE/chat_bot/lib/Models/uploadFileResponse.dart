// ignore: file_names
class UplaodFileResponse {
  final String status;

  UplaodFileResponse({required this.status});

  factory UplaodFileResponse.fromJson(Map<String, dynamic> json) {
    return UplaodFileResponse(status: json['status']);
  }
}
