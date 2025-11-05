import os
from dotenv import load_dotenv

load_dotenv()

def test_environment():
    print("🧪 E2M AI Lead Generation - Environment Test")
    print("=" * 50)
    
    groq_key = os.getenv('GROQ_API_KEY')
    apify_key = os.getenv('APIFY_API_KEY')
    
    print(f"🔑 Groq API Key: {'✅ Found' if groq_key else '❌ Missing'}")
    print(f"🔑 Apify API Key: {'✅ Found' if apify_key else '❌ Missing'}")
    
    if groq_key:
        print(f"   Preview: {groq_key[:20]}...")

if __name__ == "__main__":
    test_environment()