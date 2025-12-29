using ChatGateway.Contracts.Request;
using ChatGateway.Domain;
using Microsoft.AspNetCore.Mvc;

namespace ChatGateway.Controllers;

[ApiController]
[Route("api/[controller]")]
public class FileUploadController : Controller
{
    private readonly ILogger<FileUploadController> _logger;
    private readonly IFlaskChatClient _flaskChatClient;

    public FileUploadController(ILogger<FileUploadController> logger, IFlaskChatClient flaskChatClient)
    {
        _logger = logger;
        _flaskChatClient = flaskChatClient;
    }

    [HttpPost("upload")]
    [Produces("application/json")]
    [ProducesResponseType(typeof(object), 200)]
    [ProducesResponseType(typeof(string), 400)]
    [ProducesResponseType(500)]
    public async Task<IActionResult> UploadFile([FromBody] UploadFileRequestDto request)
    {
        if(request.FilePath == null)
            return BadRequest("No file provided");
        if(!request.FilePath.EndsWith(".txt") && !request.FilePath.EndsWith(".pdf") && !request.FilePath.EndsWith(".docx"))
            return BadRequest("Unsupported file type");

        _logger.LogInformation($"Received file {request.FilePath}");


        var responseStatus = await _flaskChatClient.UploadFile(request.FilePath);
       
        return Ok(new { fileName = request.FilePath, status = responseStatus });
    }
}
