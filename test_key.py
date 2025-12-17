import streamlit as st
import json
import google.generativeai as genai
from datetime import datetime
from typing import Dict, List, Any

print("=" * 60)
print("Testing Gemini API Key & Available Models")
print("=" * 60)

GEMINI_API_KEY = "AIzaSyCuUJDB6N5OtalskED03Ebo9hGZJpp554s"
API_WORKING = False

try:
    print("\n1. Configuring API...")
    genai.configure(api_key=GEMINI_API_KEY)
    print("   ✅ Configuration successful")
    
    print("\n2. Listing available models...")
    models = genai.list_models()
    print("   ✅ Available models:")
    
    available_models = []
    for model in models:
        if "generateContent" in model.supported_generation_methods:
            available_models.append(model.name)
            print(f"      • {model.name}")
    
    if available_models:
        print(f"\n3. Testing with first available model: {available_models[0]}")
        model = genai.GenerativeModel(available_models[0])
        response = model.generate_content("Say 'API is working'")
        print(f"   ✅ Response: {response.text[:50]}")
        
        API_WORKING = True
        print("\n" + "=" * 60)
        print("✅ SUCCESS! API Key is WORKING!")
        print("=" * 60)
    else:
        print("   ❌ No models available for this API key")
        
except Exception as e:
    print("\n" + "=" * 60)
    print(f"❌ ERROR! {type(e).__name__}")
    print(f"Message: {str(e)}")
    print("=" * 60)

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Smart Farming Assistant - AgroNova",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Show status in sidebar
if not API_WORKING:
    st.sidebar.error("⚠️ API Key Error - Some features may not work")
else:
    st.sidebar.success("✅ API Connected")