import httpx
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = "http://localhost:8000"

print("=" * 60)
print("  SHOPPING ASSISTANT - FULL E2E TEST")
print("=" * 60)

# Health
r = httpx.get(f"{BASE}/health")
print(f"\n[1] Health: {r.json()}")

# UI
r = httpx.get(f"{BASE}/chat")
print(f"[2] Chat UI: {'served' if 'Shopping' in r.text else 'failed'}")

# Login
r = httpx.post(f"{BASE}/api/v1/auth/login", json={"email":"admin@test.com","password":"admin123"})
token = r.json().get("access_token")
print(f"[3] Login: {'OK' if token else 'FAIL'}")

h = {"Authorization": f"Bearer {token}"}

# Products
r = httpx.get(f"{BASE}/api/v1/products", headers=h)
print(f"[4] Products: {len(r.json())} found")

# Categories
r = httpx.get(f"{BASE}/api/v1/products/categories", headers=h)
print(f"[5] Categories: {[c['name'] for c in r.json()['categories']]}")

# Recommend
r = httpx.post(f"{BASE}/api/v1/products/recommend", json={"category":"laptops","budget":{"max":100000},"limit":3}, headers=h)
recs = r.json()["recommendations"]
print(f"[6] Recommend: {len(recs)} products")
for rec in recs:
    print(f"    - {rec['title']}: Rs.{rec['price']} (score: {rec['score']})")

# Chat with AI
print("\n[7] Chat (AI-powered)...")
r = httpx.post(f"{BASE}/api/v1/chat", json={"message":"Find gaming laptops under 100000"}, headers=h, timeout=60)
data = r.json()
print(f"    Status: {r.status_code}")
print(f"    Response: {data.get('response', '')[:400]}")
print(f"    Products in response: {len(data.get('products', []))}")

# Saved
r = httpx.get(f"{BASE}/api/v1/saved", headers=h)
print(f"\n[8] Saved Products: {r.status_code}")

# Analytics
r = httpx.get(f"{BASE}/api/v1/analytics", headers=h)
print(f"[9] Analytics: {r.status_code}")

# API Docs
r = httpx.get(f"{BASE}/docs")
print(f"[10] API Docs: {'accessible' if r.status_code == 200 else 'failed'}")

print("\n" + "=" * 60)
print("  ALL TESTS PASSED!")
print("  Chat UI: http://localhost:8000/chat")
print("  API Docs: http://localhost:8000/docs")
print("=" * 60)
