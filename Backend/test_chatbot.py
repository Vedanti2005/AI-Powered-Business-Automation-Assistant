"""Quick diagnostic for chatbot issues"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_gemini():
    """Test Gemini API"""
    print("🤖 Testing Gemini API...")
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env")
            return False
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-flash-latest")
        response = model.generate_content("Test")
        print(f"✅ Gemini API OK: {response.text[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        return False

async def test_mongodb():
    """Test MongoDB connection"""
    print("\n📦 Testing MongoDB Connection...")
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        import certifi
        
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        print(f"   URI: {mongo_uri[:60]}...")
        
        client = AsyncIOMotorClient(mongo_uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
        await asyncio.wait_for(client.admin.command('ping'), timeout=10)
        print("✅ MongoDB Connection OK")
        client.close()
        return True
    except asyncio.TimeoutError:
        print("❌ MongoDB Connection Timeout (Network/Firewall issue)")
        return False
    except Exception as e:
        print(f"❌ MongoDB Error: {e}")
        return False

async def main():
    print("=" * 60)
    print("CODENIXIA CHATBOT DIAGNOSTIC TEST")
    print("=" * 60)
    
    gemini_ok = await test_gemini()
    mongo_ok = await test_mongodb()
    
    print("\n" + "=" * 60)
    print("RESULTS:")
    print(f"  Gemini API:     {'✅ PASS' if gemini_ok else '❌ FAIL'}")
    print(f"  MongoDB:        {'✅ PASS' if mongo_ok else '❌ FAIL'}")
    print("=" * 60)
    
    if not mongo_ok:
        print("\n⚠️  MONGODB FIXES:")
        print("  1. Check MongoDB Atlas IP whitelist")
        print("  2. Add your IP: https://cloud.mongodb.com → Network Access")
        print("  3. Or add 0.0.0.0/0 for testing (NOT production)")

if __name__ == "__main__":
    asyncio.run(main())
