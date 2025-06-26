import streamlit as st
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from core.module_manager import ModuleManager
from core.chat_manager import ChatManager
from bot_builder import show_bot_builder

# Initialize session state
if 'module_manager' not in st.session_state:
    st.session_state.module_manager = ModuleManager()
    
if 'chat_manager' not in st.session_state:
    st.session_state.chat_manager = ChatManager()
    
if 'current_module' not in st.session_state:
    st.session_state.current_module = None
    
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'chat'

def show_about_page():
    """Show the about page with platform information"""
    
    st.header("ℹ️ About AI Forge")
    
    # Platform overview
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 1rem; margin: 1rem 0; color: white;'>
        <h2 style='margin: 0 0 1rem 0; color: white;'>🔥 AI Forge Platform</h2>
        <p style='margin: 0; font-size: 1.1rem; opacity: 0.9;'>Advanced Modular AI Chat Platform with Custom AI Module Creation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Platform Features")
        st.markdown("""
        - **Modular AI System**: Plug-and-play AI modules
        - **Custom Bot Builder**: Create personalized AI assistants
        - **Advanced Configuration**: Fine-tune behavior and personality
        - **Local Processing**: No external APIs required
        - **Learning Capabilities**: Bots adapt and improve over time
        - **Multiple Specializations**: From general chat to specialized domains
        - **Memory Management**: Configurable conversation retention
        - **Multi-language Support**: Auto-detection and preferences
        """)
    
    with col2:
        st.subheader("🛠️ Technical Capabilities")
        st.markdown("""
        - **SQLite Database**: Per-module learning data storage
        - **Dynamic Module Loading**: Runtime AI module discovery
        - **Streamlit Interface**: Modern web-based UI
        - **Python Architecture**: Clean, extensible codebase
        - **Session Management**: Persistent conversation states
        - **Error Handling**: Robust failure recovery
        - **Configuration Export**: JSON-based bot configurations
        - **Response Testing**: Built-in bot validation tools
        """)
    
    # Developer section
    st.markdown("---")
    st.subheader("👨‍💻 Platform Developer")
    
    st.markdown("""
    <div style='background: linear-gradient(45deg, #ff6b6b, #4ecdc4); padding: 1.5rem; border-radius: 0.8rem; margin: 1rem 0;'>
        <div style='color: white;'>
            <h3 style='margin: 0 0 0.5rem 0; color: white;'>🌟 The_sun_kitsune</h3>
            <p style='margin: 0; font-size: 1rem; opacity: 0.9;'>Platform Creator & Lead Developer</p>
            <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;'>Architect of the AI Forge modular AI platform</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics section
    st.markdown("---")
    st.subheader("📊 Platform Statistics")
    
    # Get current statistics
    if hasattr(st.session_state, 'module_manager'):
        available_modules = st.session_state.module_manager.get_available_modules()
        module_count = len(available_modules)
    else:
        module_count = 0
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Available Modules", module_count)
    
    with stat_col2:
        st.metric("Platform Version", "2.0.0")
    
    with stat_col3:
        st.metric("Framework", "Streamlit")
    
    with stat_col4:
        st.metric("Language", "Python 3.11")
    
    # How to use section
    st.markdown("---")
    st.subheader("🎯 How to Use AI Forge")
    
    with st.expander("📖 Getting Started Guide"):
        st.markdown("""
        ### 1. 💬 Chat with Existing Modules
        - Go to the **Chat** section in the sidebar
        - Select an AI module from the dropdown
        - Start chatting with your chosen AI assistant
        - Each module has unique personality and capabilities
        
        ### 2. 🛠️ Create Custom Bots
        - Navigate to the **Bot Builder** section
        - Follow the step-by-step configuration process
        - Configure personality, responses, and knowledge areas
        - Build and deploy your custom AI module
        
        ### 3. 🔧 Advanced Features
        - Adjust creativity levels and response styles
        - Set specialized knowledge domains
        - Configure learning behaviors
        - Export and share your bot configurations
        
        ### 4. 📚 Module Management
        - Use "Refresh Modules" to load new bots
        - View module statistics and performance
        - Clear chat history when needed
        - Download created modules for backup
        """)
    
    # Version history
    with st.expander("📋 Version History"):
        st.markdown("""
        ### Version 2.0.0 - Current
        - Rebranded to AI Forge platform
        - Enhanced Bot Builder with 8 configuration tabs
        - Advanced personality and behavior settings
        - Improved error handling and stability
        - Added About section with developer information
        
        ### Version 1.5.0
        - Added comprehensive Bot Builder feature
        - Implemented custom module generation
        - Enhanced A.v.A module with AI-like reasoning
        - Added progress tracking and help guides
        
        ### Version 1.0.0
        - Initial platform release
        - Basic modular AI system
        - A.v.A module implementation
        - SQLite-based learning system
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1rem; opacity: 0.7;'>
        <p>AI Forge Platform - Advanced Modular AI Chat System</p>
        <p>Developed by The_sun_kitsune | Built with Streamlit & Python</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Chat-PC",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("🔥 AI Forge")
    st.markdown("*Advanced Modular AI Chat Platform with Custom AI Modules*")
    
    # Sidebar for navigation and module selection
    with st.sidebar:
        st.header("🎯 Navigation")
        
        # Page selection
        page_option = st.radio(
            "Choose section:",
            ["💬 Chat", "🛠️ Bot Builder", "ℹ️ About"],
            index=0 if st.session_state.current_page == 'chat' else (1 if st.session_state.current_page == 'bot_builder' else 2)
        )
        
        if page_option == "💬 Chat":
            st.session_state.current_page = 'chat'
        elif page_option == "🛠️ Bot Builder":
            st.session_state.current_page = 'bot_builder'
        else:
            st.session_state.current_page = 'about'
        
        # Show module selection only on chat page
        if st.session_state.current_page == 'chat':
            st.header("🔧 AI Modules")
            
            # Load available modules
            available_modules = st.session_state.module_manager.get_available_modules()
            
            if not available_modules:
                st.warning("No AI modules found in 'moduls' folder")
                if st.session_state.current_page == 'chat':
                    st.info("👈 Use the Bot Builder to create your first AI module!")
                return
            
            # Module selection
            module_names = [module['name'] for module in available_modules]
            
            if st.session_state.current_module:
                try:
                    current_index = module_names.index(st.session_state.current_module)
                except ValueError:
                    current_index = 0
            else:
                current_index = 0
            
            selected_module = st.selectbox(
                "Select AI Module:",
                module_names,
                index=current_index,
                key="module_selector"
            )
            
            # Load selected module if changed
            if selected_module != st.session_state.current_module:
                st.session_state.current_module = selected_module
                st.session_state.module_manager.load_module(selected_module)
                st.session_state.chat_history = []
                st.rerun()
            
            # Display module info
            if st.session_state.current_module:
                module_info = st.session_state.module_manager.get_module_info(selected_module)
                if module_info:
                    st.markdown("### 📋 Module Information")
                    st.markdown(f"**Name:** {module_info.get('name', 'N/A')}")
                    st.markdown(f"**Version:** {module_info.get('version', 'N/A')}")
                    st.markdown(f"**Description:** {module_info.get('description', 'N/A')}")
                    
                    # Module statistics
                    stats = st.session_state.module_manager.get_module_stats(selected_module)
                    if stats:
                        st.markdown("### 📊 Statistics")
                        st.markdown(f"**Learned Responses:** {stats.get('learned_responses', 0)}")
                        st.markdown(f"**Total Conversations:** {stats.get('total_conversations', 0)}")
                        if 'avg_confidence' in stats:
                            st.markdown(f"**Average Confidence:** {stats.get('avg_confidence', 0):.2f}")
                        if 'active_patterns' in stats:
                            st.markdown(f"**Active Patterns:** {stats.get('active_patterns', 0)}")
            
            # Clear chat button
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
            
            # Module management
            st.markdown("---")
            st.markdown("### ⚙️ Module Management")
            
            if st.button("🔄 Refresh Modules", use_container_width=True):
                st.session_state.module_manager.refresh_modules()
                st.rerun()
    
    # Handle different pages
    if st.session_state.current_page == 'bot_builder':
        show_bot_builder()
        return
    elif st.session_state.current_page == 'about':
        show_about_page()
        return
    
    # Main chat interface
    if not st.session_state.current_module:
        st.info("👈 Select an AI module from the sidebar to start chatting")
        return
    
    # Chat history container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Type your message...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Get AI response
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                try:
                    response = st.session_state.module_manager.get_response(
                        st.session_state.current_module,
                        user_input,
                        st.session_state.chat_history[:-1]  # Exclude the current user message
                    )
                    
                    st.write(response)
                    
                    # Add AI response to history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                    # Save conversation for learning
                    st.session_state.chat_manager.save_conversation(
                        st.session_state.current_module,
                        user_input,
                        response
                    )
                    
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
                    st.session_state.chat_history.pop()  # Remove user message if error occurred

if __name__ == "__main__":
    main()
