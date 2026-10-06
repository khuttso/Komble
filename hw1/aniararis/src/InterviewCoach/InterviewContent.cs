using System.Text.Json;

namespace InterviewCoach;

public sealed class InterviewContent
{
    public IReadOnlyList<InterviewQuestion> Questions { get; }
    public string Rubric { get; }
    public string Instructions { get; }

    public InterviewContent(string root)
    {
        var json = File.ReadAllText(Path.Combine(root, "data", "questions.json"));
        Questions = JsonSerializer.Deserialize<List<InterviewQuestion>>(json, new JsonSerializerOptions(JsonSerializerDefaults.Web))
            ?? throw new InvalidOperationException("The question list is missing.");
        if (Questions.Count == 0 || Questions.Any(q => string.IsNullOrWhiteSpace(q.Id) || string.IsNullOrWhiteSpace(q.Text)))
            throw new InvalidOperationException("At least one valid prepared question is required.");

        Rubric = File.ReadAllText(Path.Combine(root, "data", "feedback-rubric.md"));
        Instructions = File.ReadAllText(Path.Combine(root, "Prompts", "feedback.txt"));
    }
}
