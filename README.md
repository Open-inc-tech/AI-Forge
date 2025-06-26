# AI Forge - Advanced Modular AI Chat Platform

## Overview

AI Forge is an advanced modular AI chatbot platform built with Streamlit that allows users to interact with custom AI modules and create their own AI personalities. The platform provides a comprehensive web-based interface for managing AI modules, chatting with different AI assistants, and building custom bots with sophisticated configuration options. Each module can learn from conversations and maintain its own conversation history through SQLite databases.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

### Frontend Architecture
- **Framework**: Streamlit web application
- **UI Components**: Sidebar for module selection, main chat interface
- **State Management**: Streamlit session state for managing current module, chat history, and managers
- **Configuration**: Custom Streamlit theming with red primary color and clean design

### Backend Architecture
- **Core Management**: Centralized managers for modules and chat functionality
- **Module System**: Plugin-based architecture where AI modules inherit from BaseAIModule
- **Data Persistence**: SQLite databases for each module's conversation history and learning data
- **Dynamic Loading**: Runtime module discovery and loading from the `moduls` directory

## Key Components

### 1. Core Management Layer
- **ModuleManager**: Discovers, loads, and manages AI modules
- **ChatManager**: Handles conversation storage, learning data, and database operations
- **DatabaseManager**: Utility class for common database operations

### 2. AI Module System
- **BaseAIModule**: Abstract base class defining the AI module interface
- **Module Requirements**: Each module must implement `generate_response()` method
- **Learning Capabilities**: Modules can learn from conversations and store patterns
- **Isolation**: Each module maintains its own database and learning data

### 3. Example AI Module (A.v.A)
- **Local AI**: Advanced virtual Assistant with template-based responses
- **Pattern Recognition**: Extracts learning patterns from user input
- **Response Templates**: Categorized responses for different interaction types
- **Czech Language**: Designed for Czech language interactions

### 4. Data Storage
- **SQLite Databases**: One database per AI module in the `data` directory
- **Tables**:
  - `conversations`: User inputs, AI responses, timestamps, context
  - `learning_data`: Patterns, responses, confidence scores, usage statistics
  - `module_stats`: Module-specific statistics and metrics

## Data Flow

1. **Module Loading**: Application starts by scanning `moduls` directory for `*_module.py` files
2. **Module Selection**: User selects an AI module from the sidebar
3. **Chat Interaction**: User input is processed by the selected module's `generate_response()` method
4. **Response Generation**: Module generates response based on templates, patterns, or learned data
5. **Learning Process**: Conversation is stored in the module's database for future learning
6. **Pattern Storage**: Module extracts patterns from user input for improved responses

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework (v1.46.1+)
- **Python 3.11+**: Runtime environment
- **SQLite**: Embedded database (built into Python)

### Development Environment
- **Nix**: Package management and environment configuration
- **UV**: Python package management and dependency resolution
- **Replit**: Cloud development and deployment platform

## Deployment Strategy

### Replit Platform
- **Runtime**: Python 3.11 with Nix environment
- **Auto-scaling**: Configured for automatic scaling based on demand
- **Port Configuration**: Streamlit server runs on port 5000
- **Deployment Target**: Autoscale deployment for production use

### Local Development
- **Streamlit Command**: `streamlit run app.py --server.port 5000`
- **Module Development**: Add new modules to `moduls` directory following naming convention
- **Database Management**: SQLite files automatically created in `data` directory

## Changelog

```
Changelog:
- June 26, 2025. Initial setup with basic A.v.A module
- June 26, 2025. Enhanced A.v.A to AI-like intelligence with advanced reasoning
- June 26, 2025. Added Bot Builder feature for custom module creation
- June 26, 2025. Platform rebranded to AI Forge with enhanced UI and About section
```

## Recent Changes

- **Platform Rebranding**: Changed from Chat-PC to AI Forge with enhanced branding and visual identity
- **About Section**: Added comprehensive About page featuring The_sun_kitsune as platform developer with platform statistics, feature overview, and version history
- **Enhanced Bot Builder**: Improved UI with 8 configuration tabs, progress tracking, and advanced personality settings including:
  - Avatar selection and bot categorization
  - Advanced interaction modes and memory retention settings
  - Creativity levels and verbosity controls
  - Specialization areas and mood-based responses
  - Enhanced success flow with response testing
- **Error Resolution**: Fixed all ValueError issues in Bot Builder with robust selectbox handling
- **Developer Attribution**: Moved The_sun_kitsune branding from Bot Builder to dedicated About section as requested
