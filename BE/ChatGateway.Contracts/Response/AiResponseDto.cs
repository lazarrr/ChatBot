using System.Text.Json.Serialization;

public class AiResponseDto
{
    [JsonPropertyName("jobId")]
    public string JobId { get; set; }

    [JsonPropertyName("status")]
    public string Status { get; set; }

    [JsonPropertyName("result")]
    public string Result { get; set; }
}
