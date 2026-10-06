using System.Diagnostics;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text.Json;

namespace InterviewCoach;

public sealed class OpenRouterFeedbackClient(
    HttpClient http,
    OpenRouterOptions options,
    InterviewContent content,
    ILogger<OpenRouterFeedbackClient> logger)
{
    public async Task<Feedback> GetFeedbackAsync(InterviewQuestion question, string answer, CancellationToken cancellationToken)
    {
        if (!options.IsConfigured)
            throw new FeedbackException(503, "Feedback is not configured yet. Set OPENROUTER_API_KEY and OPENROUTER_MODEL, then restart the app. Your answer is still here.");

        // JSON keeps the answer in the user message, separate from trusted coaching instructions.
        var payload = new
        {
            model = options.Model,
            messages = new[]
            {
                new { role = "system", content = content.Instructions + "\n\nRubric:\n" + content.Rubric },
                new { role = "user", content = JsonSerializer.Serialize(new { question = question.Text, answer }) }
            },
            // Use the JSON-object request shape that previously succeeded in the
            // student's live test. Validate all three fields locally below.
            response_format = new { type = "json_object" },
            max_tokens = OpenRouterOptions.MaxOutputTokens,
            stream = false,
            provider = new { allow_fallbacks = false, require_parameters = true }
        };

        using var request = new HttpRequestMessage(HttpMethod.Post, "https://openrouter.ai/api/v1/chat/completions");
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", options.ApiKey);
        request.Content = JsonContent.Create(payload);
        using var deadline = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
        deadline.CancelAfter(TimeSpan.FromSeconds(OpenRouterOptions.TimeoutSeconds));
        var timer = Stopwatch.StartNew();
        int? promptTokens = null;
        int? completionTokens = null;
        int? reasoningTokens = null;
        decimal? cost = null;
        var outcome = "failed";
        var finishReason = "unavailable";
        var failureStage = "provider_response";
        int? providerStatus = null;
        int? providerErrorCode = null;

        try
        {
            // Exactly one outbound request. There is no retry or paid fallback chain.
            using var response = await http.SendAsync(request, deadline.Token);
            providerStatus = (int)response.StatusCode;
            var body = await response.Content.ReadAsStringAsync(deadline.Token);
            JsonDocument document;
            try
            {
                document = JsonDocument.Parse(body);
            }
            catch (JsonException) when (!response.IsSuccessStatusCode)
            {
                // Error pages are sometimes HTML or empty. Preserve their HTTP status
                // without mistaking them for malformed model-generated feedback.
                throw ProviderFailure(providerStatus.Value);
            }
            using var parsedResponse = document;
            var root = document.RootElement;
            if (!response.IsSuccessStatusCode)
            {
                if (root.ValueKind == JsonValueKind.Object && root.TryGetProperty("error", out var providerError))
                    providerErrorCode = ReadErrorCode(providerError);
                throw ProviderFailure(providerStatus.Value);
            }
            if (root.ValueKind != JsonValueKind.Object)
                throw InvalidOutput();

            if (root.TryGetProperty("usage", out var usage) && usage.ValueKind == JsonValueKind.Object)
            {
                promptTokens = ReadInt(usage, "prompt_tokens");
                completionTokens = ReadInt(usage, "completion_tokens");
                if (usage.TryGetProperty("completion_tokens_details", out var details) && details.ValueKind == JsonValueKind.Object)
                    reasoningTokens = ReadInt(details, "reasoning_tokens");
                if (usage.TryGetProperty("cost", out var value) && value.ValueKind == JsonValueKind.Number && value.TryGetDecimal(out var parsedCost))
                    cost = parsedCost;
            }

            if (root.TryGetProperty("error", out var embeddedError) && embeddedError.ValueKind != JsonValueKind.Null)
            {
                providerErrorCode = ReadErrorCode(embeddedError);
                throw ProviderFailure(providerErrorCode ?? providerStatus.Value);
            }

            if (!root.TryGetProperty("choices", out var choices) || choices.ValueKind != JsonValueKind.Array || choices.GetArrayLength() == 0)
                throw InvalidOutput();
            var choice = choices[0];
            if (choice.ValueKind != JsonValueKind.Object)
                throw InvalidOutput();

            // Allowlist logged values; never log arbitrary provider strings or response content.
            if (choice.TryGetProperty("finish_reason", out var finish) && finish.ValueKind == JsonValueKind.String)
                finishReason = finish.GetString() switch
                {
                    "stop" => "stop",
                    "length" => "length",
                    "content_filter" => "content_filter",
                    "tool_calls" => "tool_calls",
                    _ => "other"
                };
            failureStage = "completion_status";
            if (finishReason == "length")
                throw new FeedbackException(502, "The model reached its output limit before completing feedback. Your answer is still here. Try again manually or choose another compatible model.");
            if (finishReason != "stop")
                throw InvalidOutput();

            failureStage = "feedback_content";
            if (
                !choice.TryGetProperty("message", out var message) || message.ValueKind != JsonValueKind.Object ||
                !message.TryGetProperty("content", out var result) || result.ValueKind != JsonValueKind.String)
                throw InvalidOutput();

            failureStage = "feedback_json";
            using var feedbackDocument = JsonDocument.Parse(result.GetString()!);
            var fields = feedbackDocument.RootElement;
            failureStage = "feedback_fields";
            var feedback = new Feedback(ReadField(fields, "strengths"), ReadField(fields, "improvements"), ReadField(fields, "suggestion"));
            outcome = "success";
            failureStage = "none";
            return feedback;
        }
        catch (OperationCanceledException) when (!cancellationToken.IsCancellationRequested)
        {
            outcome = "timeout";
            throw new FeedbackException(504, "Feedback took too long. Your answer is still here; you can try again manually.");
        }
        catch (HttpRequestException)
        {
            throw new FeedbackException(502, "The feedback service could not be reached. Your answer is still here; check your connection and try again manually.");
        }
        catch (JsonException)
        {
            throw InvalidOutput();
        }
        finally
        {
            // Log only numeric usage and timing, never prompts, answers, keys, or provider bodies.
            logger.LogInformation(
                "Model call outcome={Outcome} provider_status={ProviderStatus} provider_error_code={ProviderErrorCode} finish_reason={FinishReason} failure_stage={FailureStage} elapsed_ms={ElapsedMs} prompt_tokens={PromptTokens} completion_tokens={CompletionTokens} reasoning_tokens={ReasoningTokens} cost_usd={CostUsd} usage={Usage}",
                outcome, providerStatus, providerErrorCode, finishReason, failureStage, timer.ElapsedMilliseconds, promptTokens, completionTokens, reasoningTokens, cost,
                promptTokens.HasValue && completionTokens.HasValue ? "available" : "unavailable_or_incomplete");
        }
    }

    private static int? ReadInt(JsonElement element, string name) =>
        element.TryGetProperty(name, out var value) && value.ValueKind == JsonValueKind.Number && value.TryGetInt32(out var number) ? number : null;

    private static int? ReadErrorCode(JsonElement error)
    {
        if (error.ValueKind != JsonValueKind.Object || !error.TryGetProperty("code", out var value))
            return null;
        int code;
        if (value.ValueKind == JsonValueKind.Number && value.TryGetInt32(out code) && code is >= 400 and <= 599)
            return code;
        if (value.ValueKind == JsonValueKind.String && int.TryParse(value.GetString(), out code) && code is >= 400 and <= 599)
            return code;
        return null;
    }

    private static FeedbackException ProviderFailure(int code)
    {
        // Only our own messages are displayed. Upstream bodies can contain private content.
        var explanation = code switch
        {
            400 or 422 => "OpenRouter rejected the request settings. Check the failed request in OpenRouter Activity for details about model support for JSON output and the output limit.",
            401 => "OpenRouter did not accept the API key. Set a valid OPENROUTER_API_KEY in the terminal that starts the app, then restart it.",
            402 => "OpenRouter reports insufficient credits or an exhausted key spending limit. Check your account balance and this key's limit.",
            403 => "OpenRouter denied this request. Check model access, account restrictions, and the failed request in OpenRouter Activity.",
            404 => "OpenRouter found no matching model endpoint. Check the exact model ID, supported request settings, and your account's provider/privacy restrictions.",
            408 or 504 => "The model provider timed out. Wait before trying again manually.",
            429 => "OpenRouter or the model provider has rate-limited requests. Wait for the limit to reset and check OpenRouter Activity before retrying.",
            >= 500 => "OpenRouter or the model provider is temporarily unavailable. Check OpenRouter Activity and try again later.",
            _ => "OpenRouter could not complete this request. Check the failed request in OpenRouter Activity."
        };
        return new FeedbackException(502, $"{explanation} (OpenRouter code {code}.) Your answer is still here.");
    }

    private static string ReadField(JsonElement element, string name)
    {
        if (element.ValueKind != JsonValueKind.Object || !element.TryGetProperty(name, out var value) || value.ValueKind != JsonValueKind.String)
            throw InvalidOutput();
        var text = value.GetString()?.Trim();
        if (string.IsNullOrWhiteSpace(text) || text.Length > 4000)
            throw InvalidOutput();
        return text;
    }

    private static FeedbackException InvalidOutput() => new(502,
        "The service returned incomplete or unreadable feedback. Your answer is still here; you can try again manually.");
}
