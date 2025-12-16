using ChatGateway.Contracts.Request;
using ChatGateway.Contracts.Response;

namespace ChatGateway.Domain;

public interface IFlaskChatClient
{
    Task<ChatResponseDto> SendAsync(string message, string systemPrompt);
    Task<string> ChangeModel(string model);
}
