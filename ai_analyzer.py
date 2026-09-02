import os
import json

from dotenv import load_dotenv
from groq import Groq

from schemas import ResumeAnalysis, JobKeywords


class AIAnalysisError(Exception):
    """Raised when AI analysis fails."""
    pass


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-20b"



def _make_groq_schema(schema: dict) -> dict:
    """
    Convert a Pydantic JSON schema into a schema accepted by Groq
    structured outputs.

    Groq requires:
    1. additionalProperties=false on every object.
    2. Every property must be included in the required array.
    """

    def process(node):
        if isinstance(node, dict):

            # Process JSON objects.
            if node.get("type") == "object":

                # Groq requires this on every object.
                node["additionalProperties"] = False

                # Groq requires every property to be required.
                if "properties" in node:
                    node["required"] = list(node["properties"].keys())

                    # Recursively process every property.
                    for key, value in node["properties"].items():
                        node["properties"][key] = process(value)

            # Process nested definitions.
            if "$defs" in node:
                for key, value in node["$defs"].items():
                    node["$defs"][key] = process(value)

            # Process arrays.
            if "items" in node:
                node["items"] = process(node["items"])

            # Process anyOf / oneOf / allOf.
            for key in ("anyOf", "oneOf", "allOf"):
                if key in node:
                    node[key] = [
                        process(item)
                        for item in node[key]
                    ]

            return node

        if isinstance(node, list):
            return [process(item) for item in node]

        return node

    return process(schema)




def _generate_structured_response(
    prompt: str,
    schema_model,
    schema_name: str,
):
    """
    Send a prompt to Groq and return a validated Pydantic object.
    """

    try:
        # Generate Pydantic JSON schema.
        schema = schema_model.model_json_schema()

        # Make it compatible with Groq structured outputs.
        schema = _make_groq_schema(schema)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": schema_name,
                    "schema": schema,
                    "strict": True,
                },
            },
            temperature=0,
            max_completion_tokens=4096,
        )

        content = response.choices[0].message.content

        print("GROQ RAW CONTENT:", repr(content))

        if not content:
            raise AIAnalysisError(
                "Groq returned an empty response."
            )

        data = json.loads(content)

        return schema_model.model_validate(data)

    except AIAnalysisError:
        raise

    except Exception as e:
        raise AIAnalysisError(
            f"AI analysis failed: {str(e)}"
        ) from e


def extract_job_keywords(job_description: str) -> list[str]:
    """Extract important ATS keywords from a job description."""

    prompt = f"""
You are an expert ATS system.

Extract the important keywords and requirements from this job
description.

Focus on:

- Technical skills
- Programming languages
- Frameworks
- Libraries
- Databases
- Cloud technologies
- Tools
- Certifications
- Important job-specific skills

Do NOT include generic words such as:

"teamwork", "good communication", "hard working",
"responsible", or "candidate".

Return only useful job-related keywords.

EDUCATION REQUIREMENT:

Before generating the final answer, carefully scan the entire RESUME
for the EDUCATION section and identify every education record.

For example, if the resume contains:

B.Tech ... 2027
XII ... 2023
X ... 2021

then the education list MUST contain all three records.

Do not summarize them into one record.
Do not omit school-level education.

JOB DESCRIPTION:

{job_description}
"""

    try:
        result = _generate_structured_response(
            prompt=prompt,
            schema_model=JobKeywords,
            schema_name="job_keywords",
        )

        return result.keywords

    except Exception as e:
        raise AIAnalysisError(
            f"Job keyword extraction failed: {str(e)}"
        ) from e


def analyze_resume(
    resume_text: str,
    job_description: str = "",
) -> ResumeAnalysis:

    prompt = f"""
You are an expert resume analyzer.

Analyze the resume provided below.

IMPORTANT RULES:

IMPORTANT RULES:

1. Do not invent information.
2. Extract information directly from the resume text.
3. If information is not present, return an empty string or empty list.
4. Extract skills only when they are present or clearly demonstrated.
5. Evaluate the resume objectively.
6. Give a resume score from 0 to 100.
7. Provide practical improvement suggestions.
8. Identify important ATS keywords present in the resume.

9. EDUCATION EXTRACTION IS IMPORTANT:
   - Extract EVERY education entry explicitly mentioned in the resume.
   - Do NOT return only the highest or most recent degree.
   - Include undergraduate degrees such as B.Tech/B.E.
   - Include Class XII / 12th / Higher Secondary education if present.
   - Include Class X / 10th / Secondary education if present.
   - Include diplomas or other formal education if present.
   - Preserve each education entry as a separate object in the education list.
   - Never omit an education entry simply because another degree is more advanced.
   - Use the actual institution and year stated in the resume.
   - Do not invent missing education information.

10. For LinkedIn and GitHub, return the complete URL only if an actual
   URL is present in the resume.

If a job description is provided:

- Understand the target role.
- Give suggestions for improving the resume for that role.
- Extract important ATS-relevant keywords from the JOB DESCRIPTION
  itself into job_keywords.
- Include technical skills, tools, frameworks, programming languages,
  databases, cloud technologies, and certifications.
- Exclude generic soft-skill terms such as "teamwork",
  "good communication", "hard working", or "responsible".
- Do not calculate ATS scores.
- Do not determine matching or missing keywords.

If no job description is provided:

- Return an empty list for job_keywords.

The ATS score and keyword matching are calculated separately
by the application.

JOB DESCRIPTION:

{job_description if job_description.strip() else "No job description provided."}

RESUME:

{resume_text}
"""

    try:
        return _generate_structured_response(
            prompt=prompt,
            schema_model=ResumeAnalysis,
            schema_name="resume_analysis",
        )

    except Exception as e:
        raise AIAnalysisError(
            f"Resume analysis failed: {str(e)}"
        ) from e