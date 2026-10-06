namespace InterviewCoach;

public sealed record OpenRouterOptions(string? ApiKey, string? Model)
{
    public const int TimeoutSeconds = 20;
    public const int MaxOutputTokens = 1200;
    public bool IsConfigured => !string.IsNullOrWhiteSpace(ApiKey) && !string.IsNullOrWhiteSpace(Model);

    public static OpenRouterOptions FromEnvironment() => new(
        Environment.GetEnvironmentVariable("OPENROUTER_API_KEY"),
        Environment.GetEnvironmentVariable("OPENROUTER_MODEL"));
}
