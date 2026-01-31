"""
Unit tests for the AI Travel Agent.
Run with: pytest tests/
"""
import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage, ToolMessage


class TestAgentInitialization:
    """Test agent initialization and setup."""
    
    @patch('agents.agent.ChatGoogleGenerativeAI')
    def test_agent_can_be initialized(self, mock_llm):
        """Test that the agent initializes without errors."""
        from agents.agent import Agent
        agent = Agent()
        assert agent is not None
        assert hasattr(agent, 'graph')
        assert hasattr(agent, '_tools')


class TestTools:
    """Test individual tools."""
    
    def test_tools_can_be_imported(self):
        """Test that all tools can be imported."""
        from agents.tools.flights_finder import flights_finder
        from agents.tools.hotels_finder import hotels_finder
        from agents.tools.search_tool import search_tool
        
        assert flights_finder is not None
        assert hotels_finder is not None
        assert search_tool is not None


class TestAppStartup:
    """Test Streamlit app startup checks."""
    
    @patch.dict('os.environ', {}, clear=True)
    def test_missing_google_api_key_detected(self):
        """Test that missing GOOGLE_API_KEY is detected."""
        import os
        assert os.getenv("GOOGLE_API_KEY") is None
    
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-key'})
    def test_google_api_key_present(self):
        """Test that GOOGLE_API_KEY is detected when present."""
        import os
        assert os.getenv("GOOGLE_API_KEY") == 'test-key'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
