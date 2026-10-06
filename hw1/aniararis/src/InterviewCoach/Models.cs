namespace InterviewCoach;

public sealed record InterviewQuestion(string Id, string Text, string Hint);
public sealed record AnswerRequest(string? QuestionId, string? Answer);
public sealed record Feedback(string Strengths, string Improvements, string Suggestion);
public sealed record FeedbackResponse(Feedback Feedback, double ElapsedSeconds);
public sealed record ApiError(string Error);

public sealed class FeedbackException(int statusCode, string message) : Exception(message)
{
    public int StatusCode { get; } = statusCode;
}
