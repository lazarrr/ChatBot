using System.Text;
using System.Text.Json;
using Microsoft.AspNetCore.SignalR;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;

public class AiResponseListener : BackgroundService
{
    private readonly IHubContext<ChatHub> _hubContext;
    private IConnection _connection;
    private IChannel _channel;

    public AiResponseListener(IHubContext<ChatHub> hubContext)
    {
        _hubContext = hubContext;
    }

    private async Task InitializeRabbitMqAsync()
    {
        var factory = new ConnectionFactory
        {
            HostName = "localhost", // or rabbitmq in docker
            UserName = "guest",
            Password = "guest"
        };

        _connection = await factory.CreateConnectionAsync();
        _channel = await _connection.CreateChannelAsync();

        await _channel.QueueDeclareAsync(
            queue: "ai_responses",
            durable: true,
            exclusive: false,
            autoDelete: false
        );
    }

    protected override async Task<Task> ExecuteAsync(CancellationToken stoppingToken)
    {
        await InitializeRabbitMqAsync();
        var consumer = new AsyncEventingBasicConsumer(_channel);

        consumer.ReceivedAsync += async (_, ea) =>
        {
            var body = ea.Body.ToArray();
            var message = Encoding.UTF8.GetString(body);

            var response = JsonSerializer.Deserialize<AiResponseDto>(message);

            // Push to specific client (jobId as group)
            await _hubContext
                .Clients
                .Group(response.JobId)
                .SendAsync("AiResponse", response);

            await _channel.BasicAckAsync(ea.DeliveryTag, false);
        };

        await _channel.BasicConsumeAsync(
            queue: "ai_responses",
            autoAck: false,
            consumer: consumer
        );

        return Task.CompletedTask;
    }

    public override void Dispose()
    {
        _channel?.CloseAsync();
        _connection?.CloseAsync();
        base.Dispose();
    }
}
