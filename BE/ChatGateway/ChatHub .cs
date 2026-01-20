using Microsoft.AspNetCore.SignalR;

public class ChatHub : Hub
{
    public override async Task OnConnectedAsync()
    {
        var jobId = Context.GetHttpContext()?.Request.Query["jobId"];
        if (!string.IsNullOrEmpty(jobId))
        {
            await Groups.AddToGroupAsync(Context.ConnectionId, jobId);
        }

        await base.OnConnectedAsync();
    }
}
