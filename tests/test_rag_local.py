import sys
import os
import asyncio
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.rag_engine import generate_answer
from app.utils.document_processor import store_chunks

async def test_rag_logic():
    print("\nTesting RAG Logic (Mocking DB Context if needed, but integration test preferred)...")
    
    # Initialize DB first
    print("Initializing DB with chunks...")
    store_chunks()
    
    # Test 1: Zara (Spanish)
    print("\nTest 1: Spanish Query 'Quien es Zara?'")
    response1 = await generate_answer("Quien es Zara?", "TestUser")
    print(f"Response: {response1['answer']}")
    assert 'Zara' in response1['answer']
    
    # Test 2: Emma (English)
    print("\nTest 2: English Query 'What did Emma decide to do?'")
    response2 = await generate_answer("What did Emma decide to do?", "TestUser")
    print(f"Response: {response2['answer']}")
    
    # Test 3: Determinism
    print("\nTest 3: Determinism Check")
    response3 = await generate_answer("Quien es Zara?", "TestUser")
    # Note: Determinism depends on LLM temp=0. Exact string match might vary slightly due to API but should be very close.
    # In a real unit test we might mock LLM. Here we check consistency.
    if response1['answer'] == response3['answer']:
        print("Determinism: OK")
    else:
        print("Determinism: Warning - Responses differ slightly")
        print(f"R1: {response1['answer']}")
        print(f"R3: {response3['answer']}")

if __name__ == "__main__":
    asyncio.run(test_rag_logic())
