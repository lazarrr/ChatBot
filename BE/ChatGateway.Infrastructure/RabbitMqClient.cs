using ChatGateway.Contracts.Models;
using ChatGateway.Contracts.Response;
using ChatGateway.Domain;
using RabbitMQ.Client;
using System.Text;
using System.Text.Json;

namespace ChatGateway.Infrastructure;

public class RabbitMqClient : IRabbitMqClient
{
    //ConnectionFactory factory;
    public RabbitMqClient()
    {
        //factory = new ConnectionFactory() { HostName = "localhost" };
    }

    public async Task<ChatResponseDto> SendAsync(string message, string systemPrompt)
    {
        var jobId = Guid.NewGuid().ToString();
        var factory = new ConnectionFactory() { HostName = "localhost" };
        using var connection = await factory.CreateConnectionAsync();
        using var channel = await connection.CreateChannelAsync();

        await channel.QueueDeclareAsync(queue: "ai_request", durable: false, exclusive: false, autoDelete: false,
            arguments: null);

        var messageObject = new
        {
            jobId = jobId,
            prompt = message,
            type = nameof(TypeEnum.Chat)
        };

        var body = Encoding.UTF8.GetBytes(JsonSerializer.Serialize(messageObject));

        await channel.BasicPublishAsync(exchange: string.Empty, routingKey: "ai_requests", body: body);

        return new ChatResponseDto { JobId = jobId };
    }


    public async Task<UploadFileResponseDto> UploadFile(string filePath)
    {
        var jobId = Guid.NewGuid().ToString();
        var factory = new ConnectionFactory() { HostName = "localhost" };
        using var connection = await factory.CreateConnectionAsync();
        using var channel = await connection.CreateChannelAsync();

        await channel.QueueDeclareAsync(queue: "ai_request", durable: false, exclusive: false, autoDelete: false,
            arguments: null);

        var messageObject = new
        {
            jobId = jobId,
            prompt = filePath,
            type = nameof(TypeEnum.Upload)
        };

        var body = Encoding.UTF8.GetBytes(JsonSerializer.Serialize(messageObject));

        await channel.BasicPublishAsync(exchange: string.Empty, routingKey: "ai_requests", body: body);

        return new UploadFileResponseDto { JobId = jobId };
    }
}
