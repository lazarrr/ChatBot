using ChatGateway.Domain;
using ChatGateway.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddSwaggerGen();

builder.Services.Configure<FlaskSettings>(builder.Configuration.GetSection("FlaskSettings"));

builder.Services.AddHttpClient<IFlaskChatClient, FlaskChatClient>(client =>
{
    client.BaseAddress = new Uri("http://127.0.0.1:5000/");
});

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "My API V1");
    c.RoutePrefix = string.Empty;
});

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();


