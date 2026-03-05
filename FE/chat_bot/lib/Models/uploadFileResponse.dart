// ignore: file_names
class UplaodFileResponse {
  final String jobId;

  UplaodFileResponse({required this.jobId});

  factory UplaodFileResponse.fromJson(Map<String, dynamic> json) {
    return UplaodFileResponse(jobId: json['jobId']);
  }
}
