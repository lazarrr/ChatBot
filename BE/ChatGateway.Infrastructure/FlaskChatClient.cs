using ChatGateway.Contracts.Request;
using ChatGateway.Contracts.Response;
using ChatGateway.Domain;
using System.Net.Http.Json;

namespace ChatGateway.Infrastructure;

public class FlaskChatClient : IFlaskChatClient
{
    private readonly HttpClient _httpClient;

    public FlaskChatClient(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<ChatResponseDto> SendAsync(string message)
    {
        var response = await _httpClient.PostAsJsonAsync(
            "chat",
            new ChatRequestDto { Message = message }
        );

        response.EnsureSuccessStatusCode();

        return (await response.Content.ReadFromJsonAsync<ChatResponseDto>())!;
    }
}
