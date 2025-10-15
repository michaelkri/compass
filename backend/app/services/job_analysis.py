from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from core.models import Job
from core.schemas import AnalysisSchema


def create_ai_analysis(job_description: str, resume_content: str) -> AnalysisSchema:
    llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    
    prompt_template = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an Expert Talent Analyst and Resume Strategist. "
            "Your task is to conduct a rigorous, objective, and fact-based comparison of "
            "a candidate's resume against a job description. Your output will serve as a realistic "
            "assessment of alignment, identifying clear strengths, significant gaps, and strategic recommendations. "
            "Your tone must be professional, direct, and grounded in the evidence provided in the two documents. "
            "Always address the user directly using the second person ('you,' 'your'). "
            "Structure your advice as directed guidance to the user, capable of handling a frank assessment."
            "Avoid overly optimistic or 'coaching' language. "
            "The goal is to provide clarity and actionable intelligence, not cheerleading."
            
            "\n\n**CRITICAL INSTRUCTIONS FOR ACTIONABLE INSIGHTS:**"
            "\n1. **Quick Impact Technologies**: Identify 1-3 specific, non-core technologies (e.g., a logging tool, a cloud CLI command, a minor framework) that are REQUIRED by the JD but MISSING from the Resume. These must be skills that a competent engineer could reasonably learn or refresh in 20 hours or less."
            "\n2. **Insight Categories**: Use the categories: 'Match', 'Missing', 'Overqualified', 'Alignment', and 'QuickLearn' for the insights_list."
            
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        (
            "user",
            "Please perform the analysis using the following documents:"
            "\n\n--- JOB DESCRIPTION ---\n{job_description}"
            "\n\n--- CANDIDATE RESUME ---\n{resume_content}"
        ),
    ])

    structured_llm = llm.with_structured_output(schema=AnalysisSchema)

    prompt = prompt_template.invoke({
        "job_description": job_description,
        "resume_content": resume_content
    })

    llm_analysis = structured_llm.invoke(prompt)

    # import pickle

    # with open("mock_llm.pkl", "rb") as f:
    #     llm_analysis = pickle.load(f)

    return llm_analysis