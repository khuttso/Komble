using System.Collections.Concurrent;
using System.Net;
using System.Net.Http.Json;
using InterviewCoach;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

namespace InterviewCoach.Tests;

internal sealed class TestApplication : IAsyncDisposable
{
    private readonly WebApplication app;
    private readonly HttpClient modelHttp;
    public HttpClient Browser { get; }
    public FakeModelHandler Model { get; }
    public CapturedLogs Logs { get; }

    private TestApplication(WebApplication app, HttpClient modelHttp, FakeModelHandler model, CapturedLogs logs)
    {
        this.app = app;
        this.modelHttp = modelHttp;
        Model = model;
        Logs = logs;
        Browser = new HttpClient { BaseAddress = new Uri(app.Urls.Single()), Timeout = TimeSpan.FromSeconds(35) };
    }

    public static async Task<TestApplication> StartAsync(
        Func<HttpRequestMessage, CancellationToken, Task<HttpResponseMessage>>? respond = null,
        bool configured = true,
        string model = "test/model")
    {
        var handler = new FakeModelHandler(respond ?? ((_, _) => Task.FromResult(Completion())));
        var modelHttp = new HttpClient(handler) { Timeout = Timeout.InfiniteTimeSpan };
        var logs = new CapturedLogs();
        var app = AppHost.Build(["--urls", "http://127.0.0.1:0"], builder =>
        {
            builder.Logging.ClearProviders();
            builder.Logging.AddProvider(logs);
            // Override any real environment credentials and replace outbound transport entirely.
            builder.Services.AddSingleton(new OpenRouterOptions(configured ? "test-key-not-real" : null, configured ? model : null));
            builder.Services.AddTransient(services => new OpenRouterFeedbackClient(
                modelHttp,
                services.GetRequiredService<OpenRouterOptions>(),
                services.GetRequiredService<InterviewContent>(),
                services.GetRequiredService<ILogger<OpenRouterFeedbackClient>>()));
        });
        await app.StartAsync();
        return new TestApplication(app, modelHttp, handler, logs);
    }

    public static HttpResponseMessage Completion(
        string content = "{\"strengths\":\"You explained your own action.\",\"improvements\":\"Clarify the outcome.\",\"suggestion\":\"Add one concrete result.\"}",
        bool usage = true,
        string finish = "stop") => new(HttpStatusCode.OK)
    {
        Content = JsonContent.Create(new
        {
            choices = new[] { new { finish_reason = finish, message = new { content } } },
            usage = usage ? new { prompt_tokens = 123, completion_tokens = 45, cost = 0.0002m } : null
        })
    };

    public async ValueTask DisposeAsync()
    {
        Browser.Dispose();
        await app.StopAsync();
        await app.DisposeAsync();
        modelHttp.Dispose();
    }
}

internal sealed class FakeModelHandler(Func<HttpRequestMessage, CancellationToken, Task<HttpResponseMessage>> respond) : HttpMessageHandler
{
    public int Calls { get; private set; }
    public string? LastBody { get; private set; }
    public Uri? LastUri { get; private set; }
    public string? Authorization { get; private set; }

    protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken token)
    {
        Calls++;
        LastBody = await request.Content!.ReadAsStringAsync(token);
        LastUri = request.RequestUri;
        Authorization = request.Headers.Authorization?.ToString();
        return await respond(request, token);
    }
}

internal sealed class CapturedLogs : ILoggerProvider
{
    public ConcurrentQueue<string> Entries { get; } = new();
    public ILogger CreateLogger(string categoryName) => new CaptureLogger(Entries);
    public void Dispose() { }

    private sealed class CaptureLogger(ConcurrentQueue<string> entries) : ILogger
    {
        public IDisposable? BeginScope<TState>(TState state) where TState : notnull => null;
        public bool IsEnabled(LogLevel logLevel) => true;
        public void Log<TState>(LogLevel level, EventId eventId, TState state, Exception? exception, Func<TState, Exception?, string> formatter)
            => entries.Enqueue(formatter(state, exception));
    }
}
