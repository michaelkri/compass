from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from core.models import Job
from core.schemas import AnalysisSchema


def create_ai_analysis(job_description: str, resume_content: str) -> AnalysisSchema:
    # llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    
    # prompt_template = ChatPromptTemplate.from_messages([
    #     (
    #         "system",
    #         "You are an Expert Talent Analyst and Resume Strategist. "
    #         "Your task is to conduct a rigorous, objective, and fact-based comparison of "
    #         "a candidate's resume against a job description. Your output will serve as a realistic "
    #         "assessment of alignment, identifying clear strengths, significant gaps, and strategic recommendations. "
    #         "Your tone must be professional, direct, and grounded in the evidence provided in the two documents. "
    #         "Always address the user directly using the second person ('you,' 'your'). "
    #         "Structure your advice as directed guidance to the user, capable of handling a frank assessment."
    #         "Avoid overly optimistic or 'coaching' language. "
    #         "The goal is to provide clarity and actionable intelligence, not cheerleading."
            
    #         "\n\n**CRITICAL INSTRUCTIONS FOR ACTIONABLE INSIGHTS:**"
    #         "\n1. **Quick Impact Technologies**: Identify 1-3 specific, non-core technologies (e.g., a logging tool, a cloud CLI command, a minor framework) that are REQUIRED by the JD but MISSING from the Resume. These must be skills that a competent engineer could reasonably learn or refresh in 20 hours or less."
    #         "\n2. **Insight Categories**: Use the categories: 'Match', 'Missing', 'Overqualified', 'Alignment', and 'QuickLearn' for the insights_list."
            
    #         "If you do not know the value of an attribute asked to extract, "
    #         "return null for the attribute's value.",
    #     ),
    #     (
    #         "user",
    #         "Please perform the analysis using the following documents:"
    #         "\n\n--- JOB DESCRIPTION ---\n{job_description}"
    #         "\n\n--- CANDIDATE RESUME ---\n{resume_content}"
    #     ),
    # ])

    # structured_llm = llm.with_structured_output(schema=AnalysisSchema)

    # prompt = prompt_template.invoke({
    #     "job_description": job_description,
    #     "resume_content": resume_content
    # })

    # llm_analysis = structured_llm.invoke(prompt)

    # Mock analysis
    from core.schemas import InsightSchema
    llm_analysis = AnalysisSchema(candidate_fit_score=45, application_summary='Your profile presents a solid academic foundation in Computer Science and a clear passion for the field, evidenced by your diverse projects and extracurricular involvement. However, your application is significantly impacted by the absence of professional software development work experience and the lack of information regarding your GPA and ability to work on-site in Tel Aviv, which are explicit requirements.', top_strengths=['Strong academic foundation in Computer Science with relevant coursework.', 'Demonstrated breadth of technical skills including Python, Java, C++, React, and SQL.', 'Clear passion for computer science, evidenced by projects, club membership, and stated interests.'], key_gaps=['Absence of explicit professional work experience in software development.', 'Missing GPA information, which is a specific requirement (90 or higher).', 'No confirmation of ability to work 2.5 days a week from the company office in Tel Aviv.'], quick_impact_skills=[], insights_list=[InsightSchema(title='Educational Standing Alignment', category='Match', requirement='Student for Computer Science or Software Engineering in semester 3 and above from a University.', candidate_fact='Bachelor of Science in Computer Science, University of Citytown, Expected Graduation: May 2025', summary='Your educational background as a Computer Science student aligns with the requirement for candidates in their third semester or beyond.'), InsightSchema(title='GPA Information Missing', category='Missing', requirement='GPA of 90 or higher.', candidate_fact=None, summary='Your resume does not include your GPA, which is a specific requirement for this role.'), InsightSchema(title='Technical Skill Breadth', category='Match', requirement='Technical Skills: Wide knowledge of technologies and programming languages.', candidate_fact='Programming Languages: Python, Java, C++; Web Technologies: HTML, CSS, JavaScript, React; Database: SQL, MySQL; Version Control: Git; Agile Methodologies', summary="You demonstrate a wide range of technical skills and programming languages, including Python, Java, C++, React, and SQL, which meets the job's general technical breadth expectation."), InsightSchema(title='Demonstrated Passion for Computer Science', category='Match', requirement='Real passion for computers and computer science.', candidate_fact='Member, University Coding Club (2022 - Present); Volunteer, Local Tech Community Workshops (2023); Interests: Artificial Intelligence, Open Source Contributions, Competitive Programming', summary='Your involvement in extracurricular activities and stated interests in AI, open source, and competitive programming clearly demonstrates a passion for computers and computer science.'), InsightSchema(title='Software Development Work Experience Gap', category='Missing', requirement='Work experience in software development is required.', candidate_fact=None, summary='Your resume lacks explicit professional work experience in software development, which is a mandatory requirement for this position. While you have strong projects, they do not substitute for formal work experience.'), InsightSchema(title='On-site Availability and Location', category='Missing', requirement='Ability to work at least 2.5 days a week from the company office in Tel Aviv.', candidate_fact=None, summary='Your resume does not address your ability or willingness to work on-site in Tel Aviv for 2.5 days a week, which is a logistical requirement for the role.')])
    return llm_analysis