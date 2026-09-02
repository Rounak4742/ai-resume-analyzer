from ats_analyzer import calculate_ats_score


resume = """
I am a Java developer.

I have experience with Python and SQL.
"""


job_description = """
Looking for a Java developer with Python and SQL experience.
"""


keywords = [
    "Java",
    "Python",
    "SQL"
]


result = calculate_ats_score(
    resume,
    job_description,
    keywords
)

print(result)