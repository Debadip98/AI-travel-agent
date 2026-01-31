"""
Test script to verify the AI Travel Agent is working correctly.
Run this before deploying to production.
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_env_variables():
    """Check if all required environment variables are set."""
    print("🔍 Testing Environment Variables...")
    required_vars = ['GOOGLE_API_KEY', 'SERPAPI_API_KEY']
    missing = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
            print(f"  ❌ {var} is MISSING")
        else:
            print(f"  ✅ {var} is set")
    
    if missing:
        print(f"\n⚠️ Missing variables: {', '.join(missing)}")
        return False
    print("✅ All environment variables are set!\n")
    return True

def test_gemini_connection():
    """Test connection to Gemini API."""
    print("🔍 Testing Gemini API Connection...")
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage
        
        llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp')
        response = llm.invoke([HumanMessage(content="Say 'Hello from Gemini!' and nothing else.")])
        print(f"  ✅ Gemini Response: {response.content}")
        print("✅ Gemini API connection successful!\n")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}\n")
        return False

def test_agent_initialization():
    """Test that the agent can be initialized."""
    print("🔍 Testing Agent Initialization...")
    try:
        from agents.agent import Agent
        agent = Agent()
        print("  ✅ Agent initialized successfully")
        print("✅ Agent setup complete!\n")
        return True
    except Exception as e:
        print(f"  ❌ Error initializing agent: {e}\n")
        return False

def test_tools():
    """Test that all tools can be imported."""
    print("🔍 Testing Tools Import...")
    try:
        from agents.tools.flights_finder import flights_finder
        from agents.tools.hotels_finder import hotels_finder
        from agents.tools.search_tool import search_tool
        print("  ✅ All tools imported successfully")
        print("✅ Tools are ready!\n")
        return True
    except Exception as e:
        print(f"  ❌ Error importing tools: {e}\n")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 AI Travel Agent - Pre-Deployment Tests")
    print("=" * 50 + "\n")
    
    results = []
    results.append(("Environment Variables", test_env_variables()))
    results.append(("Gemini Connection", test_gemini_connection()))
    results.append(("Tools Import", test_tools()))
    results.append(("Agent Initialization", test_agent_initialization()))
    
    print("=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Ready for deployment.")
    else:
        print("\n⚠️ SOME TESTS FAILED. Please fix issues before deploying.")
    
    print("=" * 50)
