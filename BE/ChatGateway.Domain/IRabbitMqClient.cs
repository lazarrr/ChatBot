using ChatGateway.Contracts.Response;
namespace ChatGateway.Domain;

public interface IRabbitMqClient
{
    Task<ChatResponseDto> SendAsync(string message, string systemPrompt);
    Task<UploadFileResponseDto> UploadFile(string filePath);
}
