from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from prompt.TriageAgentPrompt import TRIAGE_AGENT_PROMPT
from prompt.CriticAgentPrompt import CRITIQUE_AGENT_PROMPT
from prompt.expertAgentPrompt import EXPERT_AGENT_PROMPT
from prompt.promptSmith import PROMPT_SMITH_PROMPT
from modelConfig import GEMINI
from agent.state import AgentState


def create_chain(system_prompt: str, include_user_msg: bool = True):
    """Factory function to create prompt chains"""
    messages = [("system", system_prompt)]
    if include_user_msg:
        messages.append(("user", "{user_input}"))
    
    template = ChatPromptTemplate.from_messages(messages)
    return template | GEMINI | StrOutputParser()


PERSONA_MAP = {
    "ARCHITECT": "Senior Solutions Architect & Strategist",
    "BUILDER": "Senior Software Engineer & Implementation Specialist",
    "MENTOR": "Expert Educator & Technical Communicator",
    "ANALYST": "Lead Quality Assurance & Data Analyst"
}


def triageAgent(state: AgentState) -> dict:
    """Classifies user intent"""
    print("🔍 [TRIAGE] Analyzing...")
    chain = create_chain(TRIAGE_AGENT_PROMPT)
    response = chain.invoke({"user_input": state["user_query"]})
    
    intent = response.strip().upper()
    valid_intents = list(PERSONA_MAP.keys())
    result = intent if intent in valid_intents else "ARCHITECT"
    
    print(f"✅ [TRIAGE] {result}")
    return {"intent": result}


def criticAgent(state: AgentState) -> dict:
    """Identifies gaps in the user query"""
    print("🔍 [CRITIC] Analyzing...")
    chain = create_chain(CRITIQUE_AGENT_PROMPT)
    response = chain.invoke({"user_input": state["user_query"]})
    
    print("✅ [CRITIC] Done")
    return {"critique": response.strip()}


def expertAgent(state: AgentState) -> dict:
    """Provides domain-specific expert advice"""
    print(f"🔍 [EXPERT] Consulting {state['intent']} expert...")
    
    selected_persona = PERSONA_MAP.get(state["intent"], "Helpful AI Assistant")
    
    # ✅ CORRECT: Use placeholders, not f-strings
    template = ChatPromptTemplate.from_messages([
        ("system", EXPERT_AGENT_PROMPT),
        ("user", """Context:
- User's Intent Mode: {intent}
- Original Query: {user_query}
- Critique (Gaps Identified): {critique}

Provide your expert suggestions now.""")
    ])
    
    chain = template | GEMINI | StrOutputParser()
    
    response = chain.invoke({
        "persona": selected_persona,
        "intent": state["intent"],
        "user_query": state["user_query"],
        "critique": state["critique"]
    })
    
    print("✅ [EXPERT] Done")
    return {"expert_suggestions": response.strip()}


def promptSmith(state: AgentState) -> dict:
    """Synthesizes the final structured prompt"""
    print("🔍 [SMITH] Crafting final prompt...")
    
    template = ChatPromptTemplate.from_messages([
        ("system", PROMPT_SMITH_PROMPT),
        ("user", """Inputs for synthesis:

1. Original Query: {user_query}
2. Expert Advice: {expert_suggestions}
3. Identified Gaps: {critique}

Create the final refined prompt now.""")
    ])
    
    chain = template | GEMINI | StrOutputParser()
    
    response = chain.invoke({
        "user_query": state["user_query"],
        "expert_suggestions": state["expert_suggestions"],
        "critique": state["critique"]
    })
    
    print("✅ [SMITH] Done")
    return {"final_prompt_draft": response.strip()}
