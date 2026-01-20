using ChatGateway.Contracts.Request;
using ChatGateway.Domain;
using ChatGateway.Infrastructure;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;

namespace ChatGateway.Controllers;


[ApiController]
[Route("api/[controller]")]
public class ChatController : Controller
{

    private readonly ILogger<ChatController> _logger;
    private readonly FlaskSettings _flaskSettings;
    private readonly IRabbitMqClient _rabbitMqClient;

    public ChatController(ILogger<ChatController> logger, IOptions<FlaskSettings> options, IRabbitMqClient rabbitMqClient)
    {
        _logger = logger;
        _flaskSettings = options.Value;
        _rabbitMqClient = rabbitMqClient;
    }

    [HttpPost("chat")]
    [Produces("application/json")]
    [ProducesResponseType(typeof(object), 200)]
    [ProducesResponseType(typeof(string), 400)]
    [ProducesResponseType(500)]
    public async Task<IActionResult> Chat([FromBody] ChatRequestDto chatRequest)
    {
        var response = await _rabbitMqClient.SendAsync(chatRequest.Message, chatRequest.SystemPrompt);

        return Ok(response);
    }
}
