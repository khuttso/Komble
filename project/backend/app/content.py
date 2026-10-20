"""Team-authored starter questions. No provider access or mutable user data."""

from .schemas import Pack, Question


PACKS = (
    Pack(
        id="frontend",
        title="Junior Frontend Developer",
        role="Frontend Developer",
        tags=["frontend", "javascript", "entry-level"],
        description="Explain the browser basics and the decisions behind your work.",
        questions=[
            Question(id="frontend-web", text="How do HTML, CSS, and JavaScript work together in a web page?", hint="Explain each part and use a small example."),
            Question(id="frontend-accessibility", text="How would you make a form accessible to keyboard users?", hint="Think about labels, focus, and validation."),
            Question(id="frontend-debugging", text="How would you investigate a page that looks wrong on a phone?", hint="Walk through what you would check first."),
            Question(id="frontend-project", text="Tell me about a small project you built and a challenge you solved.", hint="Describe the situation, your actions, and what happened."),
        ],
    ),
    Pack(
        id="support",
        title="Customer Support Representative",
        role="Customer Support",
        tags=["communication", "support", "entry-level"],
        description="Practise listening, explaining clearly, and finding a way forward.",
        questions=[
            Question(id="support-upset", text="How would you respond to an upset customer whose order is late?", hint="Explain how you would listen, investigate, and follow up."),
            Question(id="support-explain", text="Tell me about a time you explained something difficult clearly.", hint="An example from study, volunteering, or work is welcome."),
            Question(id="support-unknown", text="What would you do if you did not know the answer to a customer question?", hint="Consider what you would communicate and where you would look."),
            Question(id="support-priorities", text="How would you prioritise several customers who all need help?", hint="Make your prioritisation criteria explicit."),
        ],
    ),
    Pack(
        id="graduate",
        title="Graduate Trainee",
        role="Graduate Trainee",
        tags=["general", "behavioral", "entry-level"],
        description="Find clear examples from your experience, even before your first job.",
        questions=[
            Question(id="graduate-introduction", text="Tell me about yourself and what interests you about this role.", hint="Connect your relevant interests and experience to the role."),
            Question(id="graduate-teamwork", text="Describe a time you worked with others to reach a shared goal.", hint="Be clear about your own contribution."),
            Question(id="graduate-learning", text="How do you approach learning a skill you have never used before?", hint="Give a concrete example if you can."),
            Question(id="graduate-mistake", text="Tell me about a mistake you made and what you learned from it.", hint="Describe your actions and learning without inventing an outcome."),
        ],
    ),
)
