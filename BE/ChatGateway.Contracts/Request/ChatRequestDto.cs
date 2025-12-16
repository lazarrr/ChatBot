namespace ChatGateway.Contracts.Request;

public class ChatRequestDto
{
    public required string Message { get; set; }
    public required string SystemPrompt { get; set; }
}
