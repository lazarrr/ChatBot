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

    public async Task<string> ChangeModel(string model)
    {
        var response = await _httpClient.PostAsJsonAsync("change_model", new ChangeModelRequestDto { ModelName = model });

        response.EnsureSuccessStatusCode();

        return await response.Content.ReadAsStringAsync();
    }

    public async Task<ChatResponseDto> SendAsync(string message, string systemPrompt)
    {
        var response = await _httpClient.PostAsJsonAsync(
            "chat",
            new ChatRequestDto { Message = message, SystemPrompt = systemPrompt}
        );

        response.EnsureSuccessStatusCode();

        return (await response.Content.ReadFromJsonAsync<ChatResponseDto>())!;
    }
}
