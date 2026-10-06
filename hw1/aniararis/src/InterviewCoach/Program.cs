using System.Diagnostics;
using InterviewCoach;

var app = AppHost.Build(args);
await app.RunAsync();

namespace InterviewCoach
{
    public static class AppHost
    {
        public static WebApplication Build(string[] args, Action<WebApplicationBuilder>? configure = null)
        {
            // Assets are copied beside the assembly, so Rider, dotnet run, and published builds
            // all locate the same files regardless of the shell's working directory.
            var builder = WebApplication.CreateBuilder(new WebApplicationOptions
            {
                Args = args,
                ContentRootPath = AppContext.BaseDirectory,
                WebRootPath = "wwwroot"
            });
            if (string.IsNullOrEmpty(builder.Configuration["urls"]))
                builder.WebHost.UseUrls("http://localhost:5180");

            builder.WebHost.ConfigureKestrel(server => server.Limits.MaxRequestBodySize = 32_768);
            builder.Logging.AddFilter("Microsoft.AspNetCore", LogLevel.Warning);
            builder.Logging.AddFilter("System.Net.Http.HttpClient", LogLevel.Warning);
            builder.Services.AddSingleton(OpenRouterOptions.FromEnvironment());
            builder.Services.AddSingleton(new InterviewContent(AppContext.BaseDirectory));
            builder.Services.AddHttpClient<OpenRouterFeedbackClient>(client =>
            {
                client.Timeout = Timeout.InfiniteTimeSpan; // One explicit 20-second deadline in the client.
                client.MaxResponseContentBufferSize = 131_072;
            }).ConfigurePrimaryHttpMessageHandler(() => new HttpClientHandler { AllowAutoRedirect = false });
            configure?.Invoke(builder);
            var app = builder.Build();

            app.Use(async (context, next) =>
            {
                context.Response.Headers.CacheControl = "no-store";
                context.Response.Headers.XContentTypeOptions = "nosniff";
                context.Response.Headers["Referrer-Policy"] = "no-referrer";
                context.Response.Headers.ContentSecurityPolicy = "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'self'";
                await next(context);
            });
            app.UseDefaultFiles();
            app.UseStaticFiles();

            app.MapGet("/api/question", (InterviewContent content) => Results.Ok(content.Questions[0]));
            app.MapPost("/api/feedback", async (AnswerRequest input, InterviewContent content, OpenRouterFeedbackClient client, CancellationToken token) =>
            {
                var answer = input.Answer?.Trim();
                if (string.IsNullOrEmpty(answer) || answer.Length > 3000)
                    return Results.Json(new ApiError("Enter an answer between 1 and 3,000 characters after trimming spaces."), statusCode: 400);
                var question = content.Questions.FirstOrDefault(q => q.Id == input.QuestionId);
                if (question is null)
                    return Results.Json(new ApiError("This question is not available. Reload the page and try again."), statusCode: 400);

                var timer = Stopwatch.StartNew();
                try
                {
                    var feedback = await client.GetFeedbackAsync(question, answer, token);
                    return Results.Ok(new FeedbackResponse(feedback, Math.Round(timer.Elapsed.TotalSeconds, 2)));
                }
                catch (FeedbackException exception)
                {
                    return Results.Json(new ApiError(exception.Message), statusCode: exception.StatusCode);
                }
            });
            return app;
        }
    }
}
