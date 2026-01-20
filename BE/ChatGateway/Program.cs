using ChatGateway.Domain;
using ChatGateway.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddSwaggerGen();

builder.Services.Configure<FlaskSettings>(builder.Configuration.GetSection("FlaskSettings"));

//builder.Services.AddHttpClient<IRabbitMqClient, RabbitMqClient>(client =>
//{
//    client.BaseAddress = new Uri("http://127.0.0.1:8081/");
//});

builder.Services.AddScoped<IRabbitMqClient, RabbitMqClient>();

builder.Services.AddSignalR();

builder.Services
    .AddControllers()
    .AddNewtonsoftJson(options =>
    {
        options.SerializerSettings.Converters.Add(
            new Newtonsoft.Json.Converters.StringEnumConverter()
        );
    });

// <-- Register your hosted service here
builder.Services.AddHostedService<AiResponseListener>();

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "My API V1");
    c.RoutePrefix = string.Empty;
});

app.MapHub<ChatHub>("/chatHub");

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
