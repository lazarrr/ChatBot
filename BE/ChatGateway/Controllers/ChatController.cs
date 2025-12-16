using ChatGateway.Contracts.Request;
using ChatGateway.Domain;
using ChatGateway.Infrastructure;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using System.Reflection;
using System.Runtime.Serialization;
using System.Threading.Tasks;

namespace ChatGateway.Controllers;


[ApiController]
[Route("api/[controller]")]
public class ChatController : Controller
{

    private readonly ILogger<ChatController> _logger;
    private readonly FlaskSettings _flaskSettings;
    private readonly IFlaskChatClient _flaskChatClient;

    public ChatController(ILogger<ChatController> logger, IOptions<FlaskSettings> options, IFlaskChatClient flaskChatClient)
    {
        _logger = logger;
        _flaskSettings = options.Value;
        _flaskChatClient = flaskChatClient;
    }

    [HttpPost("chat")]
    [Produces("application/json")]
    [ProducesResponseType(typeof(object), 200)]
    [ProducesResponseType(typeof(string), 400)]
    [ProducesResponseType(500)]
    public async Task<IActionResult> Chat([FromBody] ChatRequestDto chatRequest)
    {
        var response = await _flaskChatClient.SendAsync(chatRequest.Message, chatRequest.SystemPrompt);

        return Ok(response);
    }

    [HttpPost("change_model")]
    [Produces("application/json")]
    [ProducesResponseType(typeof(object), 200)]
    [ProducesResponseType(typeof(string), 400)]
    [ProducesResponseType(500)]
    public async Task<IActionResult> ChangeModel(ChangeModelRequestEnumDto changeModelRequest)
    {
        var enumMember = changeModelRequest
                    .GetType()
                    .GetField(changeModelRequest.ToString())?
                    .GetCustomAttribute<EnumMemberAttribute>();

        var modelName = enumMember?.Value ?? changeModelRequest.ToString();

        if(modelName == null)
        {
            return BadRequest("Invalid model name.");
        }

        var response = await _flaskChatClient.ChangeModel(modelName);
        return Ok(response);
    }


}
