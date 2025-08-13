import os
import streamlit as st
from langchain_community.llms import HuggingFacePipeline
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import AgentAction, AgentFinish, HumanMessage, SystemMessage
from typing import List, Union, Dict, Any
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, GenerationConfig

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"

def load_local_model():
    """Load a local language model"""
    try:
        model_name = "gpt2"  # Using a small model that's quick to load
        
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32
        )
        
        # Configure generation
        generation_config = GenerationConfig(
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
        
        # Create text generation pipeline
        text_generation_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=0 if device == "cuda" else -1,
            generation_config=generation_config
        )
        
        # Create LangChain LLM
        llm = HuggingFacePipeline(pipeline=text_generation_pipeline)
        return llm
        
    except Exception as e:
        st.error(f"Error loading local model: {str(e)}")
        return None

def create_agentic_chatbot():
    """
    Create and return an agentic chatbot with web search and document reading capabilities.
    
    Returns:
        Agent: Initialized LangChain agent or None if there's an error
    """
    try:
        # Initialize the local language model
        llm = load_local_model()
        if not llm:
            return None
        
        # Initialize memory with proper message format
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            memory_key_kwargs={"human_prefix": "User", "ai_prefix": "Assistant"}
        )
        
        # Add a system message to set the context
        memory.chat_memory.add_message(
            SystemMessage(content="""You are a helpful AI assistant. Keep your responses concise and to the point. 
            If you don't know something, say so instead of making things up.""")
        )
        
        def search_web(query):
            """Search the web using DuckDuckGo (no API key needed)"""
            try:
                from duckduckgo_search import ddg
                results = ddg(query, max_results=3)
                if results:
                    return "\n".join([f"{r['title']}: {r['body']}" for r in results])
                return "No search results found."
            except Exception as e:
                return f"Error performing web search: {str(e)}. Please try again later."
        
        def read_docs(path="data/sample_docs/info.txt"):
            """Read content from documents"""
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                if not os.path.exists(path):
                    # Create a sample file if it doesn't exist
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "w") as f:
                        f.write("This is a sample document. Replace this with your own content.")
                with open(path, "r") as f:
                    return f.read()
            except Exception as e:
                return f"Error reading document: {str(e)}"
        
        # Define tools
        tools = [
            Tool(
                name="Web Search",
                func=search_web,
                description="Useful for searching the web for current information. Input should be a search query."
            ),
            Tool(
                name="Document Reader",
                func=read_docs,
                description="Useful for reading documents. Input should be a file path. Default is 'data/sample_docs/info.txt'"
            )
        ]
        
        # Initialize the agent
        from langchain.agents import initialize_agent
        
        agent = initialize_agent(
            tools, 
            llm, 
            agent="conversational-react-description",
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )
        
        return agent
        
    except Exception as e:
        st.error(f"Error creating agent: {str(e)}")
        return None

def show_agentic_chatbot():
    """Display the Agentic Chatbot interface"""
    st.markdown("### 🧵 Local AI Chatbot")
    st.write("Chat with a local AI that can search the web and read documents (no API key required).")
    
    # Initialize session state for chat history if it doesn't exist
    if "agent_messages" not in st.session_state:
        st.session_state.agent_messages = [
            {"role": "assistant", "content": "Hello! I'm your local AI assistant. How can I help you today?"}
        ]
    
    # Initialize agent if it doesn't exist
    if "agent" not in st.session_state:
        with st.spinner("Initializing local AI model (this may take a minute)..."):
            try:
                st.session_state.agent = create_agentic_chatbot()
                if not st.session_state.agent:
                    st.error("Failed to initialize the local AI model. Please check the error message above.")
                    return
            except Exception as e:
                st.error(f"Error initializing AI agent: {str(e)}")
                st.info("Please make sure you have the required packages installed.")
                return
    
    # Display chat messages
    for message in st.session_state.agent_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    user_input = st.chat_input("Type your message here...", key="agent_chat_input")
    
    if user_input:
        # Add user message to chat history
        st.session_state.agent_messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate AI response
        if st.session_state.agent:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Get the response
                        response = st.session_state.agent.run(user_input)
                        
                        # Update the UI
                        st.markdown(response)
                        st.session_state.agent_messages.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.agent_messages.append({"role": "assistant", "content": error_msg})
                        
                        # If there's an error, clear the memory to prevent state corruption
                        if hasattr(st.session_state, 'agent') and hasattr(st.session_state.agent, 'memory'):
                            st.session_state.agent.memory.clear()
        else:
            error_msg = "Agent not properly initialized. Please try refreshing the page."
            st.error(error_msg)
            st.session_state.agent_messages.append({"role": "assistant", "content": error_msg})
    
    # Add information about the local model
    st.markdown("---")
    with st.expander("ℹ️ About This Chatbot"):
        st.markdown("""
        This chatbot runs locally on your machine using a pre-trained language model.
        
        **Features:**
        - No API keys required
        - Works offline after initial setup
        - Can search the web (requires internet connection)
        - Can read local documents
        
        **Note:** The model is smaller than commercial alternatives, so responses may be less sophisticated.
        """)

show_agentic_chatbot()
