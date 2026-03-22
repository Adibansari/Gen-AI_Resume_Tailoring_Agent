import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

def run_tailoring(context, jd):
    llm = ChatOpenAI(model="gpt-4", temperature=0.3)

    base_dir = os.path.dirname(os.path.dirname(__file__))
    prompt_path = os.path.join(base_dir, "prompts", "tailor_prompt.txt")

    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    prompt = PromptTemplate.from_template(template)

    # Pass variables safely
    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "jd": jd
    })

    return response.content
