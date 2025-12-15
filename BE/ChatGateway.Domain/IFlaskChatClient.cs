using ChatGateway.Contracts.Response;

namespace ChatGateway.Domain;

public interface IFlaskChatClient
{
    Task<ChatResponseDto> SendAsync(string message);
}
