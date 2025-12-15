using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace ChatGateway.Controllers;


[ApiController]
[Route("api/[controller]")]
public class FileUploadController : Controller
{
    private readonly ILogger<FileUploadController> _logger;

    public FileUploadController(ILogger<FileUploadController> logger)
    {
        _logger = logger;
    }

    [HttpPost("upload")]
    [Consumes("multipart/form-data")]
    [Produces("application/json")]
    [ProducesResponseType(typeof(object), 200)]
    [ProducesResponseType(typeof(string), 400)]
    [ProducesResponseType(500)]
    public async Task<IActionResult> UploadFile(IFormFile file)
    {
        if (file == null || file.Length == 0)
            return BadRequest("File is empty");

        // Example: Only allow text/plain and application/pdf files
        if (file.ContentType != "text/plain" && file.ContentType != "application/pdf")
            return BadRequest("Unsupported file type");

        // Normally, you would save the file somewhere
        // For now, we'll just log information about the file
        _logger.LogInformation($"Received file {file.FileName} - size: {file.Length} bytes");

        var filePath = Path.GetTempFileName();
        using (var stream = System.IO.File.Create(filePath))
        {
            await file.CopyToAsync(stream);
        }


        // send file name and path to chat microservice


        return Ok(new { fileName = file.FileName, size = file.Length, path = filePath });
    }
    
}
