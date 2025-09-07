from typing import List, Dict, Any
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.langchain.agent.tools import JobSummaryTool
# from app.langchain.agent.tools import JobSummaryTool, SkillAnalysisTool, StudyPlanTool
import json

class CareerAgent:
    """
    A conversational AI agent that helps users interact with their career data.
    
    LEARNING NOTES:
    - This class holds all the "state" (database connection, user info, memory)
    - The agent uses "tools" to access your data
    - It has "memory" to remember the conversation
    - It uses a "prompt template" to know how to behave
    """

    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user
        self.llm = ChatOpenAI(temperature=0.1, model="gpt-4")
        print(f"�� Initialized LLM: {self.llm.model_name}")

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        print(f"�� Initialized memory system")

        job_summary_tool = JobSummaryTool(db, user)

        self.tools = [
            job_summary_tool
        ]

        self.agent_executor = self._create_agent()
        print(f"✅ CareerAgent created successfully!")
    
    def _create_agent(self) -> AgentExecutor:
        """
        Create the agent with tools and prompt template.
        
        LEARNING NOTES:
        - The "prompt template" tells the agent how to behave
        - The "tools" are what the agent can use to get data
        - The "agent executor" runs everything together
        """

        print(f"🔧 Creating agent with {len(self.tools)} tools...")

                # Define the system prompt - this is like giving the agent a job description
        system_prompt = """You are a helpful career assistant for a user named {user_name}. 
        You have access to their job data and can provide summaries of their imported jobs.
        
        Your capabilities:
        1. get_job_summary: Get a summary of all imported jobs
        
        Guidelines:
        - Be conversational and helpful
        - When users ask for job summaries, use the get_job_summary tool
        - Always provide context and explanations, not just raw data
        - If a user asks something you can't help with, politely explain your limitations
        
        Remember: You're helping someone advance their career by making their job data more accessible and actionable."""
        
        print(f"📝 Created system prompt (length: {len(system_prompt)} characters)")

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),  # ← The "job description"
            MessagesPlaceholder(variable_name="chat_history"),  # ← Previous conversation
            ("human", "{input}"),  # ← What the user just asked
            MessagesPlaceholder(variable_name="agent_scratchpad")  # ← Agent's thinking process
        ]).partial(user_name=self.user.email)
        print(f"📝 Created prompt template with {prompt.messages}")

        agent = create_openai_tools_agent(
            llm=self.llm,  # ← The AI model
            tools=self.tools,  # ← What it can do
            prompt=prompt  # ← How it should behave
        )

        # Create the agent executor - this runs the agent and handles the conversation
        agent_executor = AgentExecutor(
            agent=agent,  # ← The agent we just created
            tools=self.tools,  # ← The tools it can use
            memory=self.memory,  # ← Its memory
            verbose=True,  # ← Show what it's thinking (great for learning!)
            handle_parsing_errors=True,  # ← Don't crash on errors
            max_iterations=3  # ← Don't get stuck in loops
        )
        return agent_executor
    
    async def chat(self, message: str) -> str:
        print(f"\n{'='*50}")
        print(f"💬 USER MESSAGE: {message}")
        print(f"{'='*50}")

        try:
            formatted_input = {
                "input": message,
                "user_name": self.user.email
            }
        
            print(f"�� Formatted input: {formatted_input}")
            print(f"��️  Available tools: {[tool.name for tool in self.tools]}")
            print(f"🔍 Memory has {len(self.memory.chat_memory.messages)} previous messages")
            response = await self.agent_executor.ainvoke({"input": message})

            print(f"✅ Agent response: {response['output']}")
            print(f"{'='*50}\n")

            return response["output"]
        
        except Exception as e:
            error_msg = f"I encountered an error while processing your request: {str(e)}. Please try rephrasing your question."
            print(f"❌ Error: {error_msg}")
            return error_msg
        
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history for display purposes.
        
        LEARNING NOTES:
        - This shows you what the agent remembers
        - Each message has a role (user/assistant) and content
        """

        history = []
        for message in self.memory.chat_memory.messages:
            if isinstance(message, HumanMessage):
                history.append({"role": "user", "content": message.content})
            elif isinstance(message, AIMessage):
                history.append({ "role": "assistant", "content": message.content})

        print(f"📚 Retrieved {len(history)} messages from conversation history")
        return history
    
    def clear_memory(self):
        """Clear the conversation memory"""
        print(f"🧹 Clearing conversation memory...")
        self.memory.clear()
        print(f"✅ Memory cleared!")

    def debug_info(self) -> Dict[str, Any]:
        """
        Get debug information about the agent.
        
        LEARNING NOTES:
        - This helps you understand what the agent has access to
        - Great for debugging and learning!
        """
        
        return {
            "user_email": self.user.email,
            "user_id": str(self.user.id),
            "tools": [tool.name for tool in self.tools],
            "tool_descriptions": [tool.description for tool in self.tools],
            "memory_messages": len(self.memory.chat_memory.messages),
            "llm_model": self.llm.model_name,
            "llm_temperature": self.llm.temperature
        }