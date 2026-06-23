#!/usr/bin/env python
"""
Shopping Assistant - One-click Startup
Run this file to start everything: python start.py
"""
import os
import sys
import subprocess
import time
import webbrowser
import threading

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_deps():
    required = ["fastapi", "uvicorn", "sqlalchemy", "aiosqlite", "bcrypt", "httpx"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"[SETUP] Installing missing packages: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing + ["-q"])

def seed_database():
    from dotenv import load_dotenv
    load_dotenv(".env", override=True)
    from config import get_settings
    get_settings.cache_clear()

    if os.path.exists("shopping.db"):
        print("[DB] Database already exists, skipping seed.")
        return

    print("[DB] Seeding database with demo products...")
    import asyncio
    from database.connection import init_db, async_session_factory
    from database.models import Product, User
    from services.auth import get_password_hash

    async def seed():
        await init_db()
        async with async_session_factory() as db:
            admin = User(name="Admin", email="admin@test.com",
                         password_hash=get_password_hash("admin123"), role="admin")
            db.add(admin)
            products = [
                Product(title="ASUS ROG Strix G15", price=89990, original_price=99990, rating=4.5, review_count=1250, category="laptops", brand="ASUS", specifications={"ram":"16GB","storage":"512GB SSD","gpu":"RTX 3060"}),
                Product(title="MSI Katana GF76", price=74990, original_price=84990, rating=4.3, review_count=890, category="laptops", brand="MSI", specifications={"ram":"16GB","storage":"512GB SSD","gpu":"RTX 3050"}),
                Product(title="Lenovo IdeaPad Gaming 3", price=64990, original_price=74990, rating=4.2, review_count=1500, category="laptops", brand="Lenovo", specifications={"ram":"8GB","storage":"256GB SSD","gpu":"RTX 3050"}),
                Product(title="Acer Nitro 5", price=69990, rating=4.4, review_count=2000, category="laptops", brand="Acer", specifications={"ram":"16GB","storage":"512GB SSD","gpu":"RTX 3050 Ti"}),
                Product(title="HP Pavilion Gaming 15", price=72990, rating=4.1, review_count=1100, category="laptops", brand="HP", specifications={"ram":"16GB","storage":"512GB SSD","gpu":"GTX 1650"}),
                Product(title="Dell G15 5520", price=78990, rating=4.3, review_count=950, category="laptops", brand="Dell", specifications={"ram":"16GB","storage":"512GB SSD","gpu":"RTX 3050"}),
                Product(title="iPhone 15 Pro Max", price=159900, rating=4.7, review_count=2500, category="smartphones", brand="Apple", specifications={"ram":"8GB","storage":"256GB","camera":"48MP"}),
                Product(title="Samsung Galaxy S24 Ultra", price=134999, rating=4.6, review_count=1800, category="smartphones", brand="Samsung", specifications={"ram":"12GB","storage":"256GB","camera":"200MP"}),
                Product(title="OnePlus 12", price=64999, rating=4.5, review_count=1200, category="smartphones", brand="OnePlus", specifications={"ram":"16GB","storage":"256GB","camera":"50MP"}),
                Product(title="Google Pixel 8 Pro", price=89999, rating=4.5, review_count=1000, category="smartphones", brand="Google", specifications={"ram":"12GB","storage":"128GB","camera":"50MP"}),
                Product(title="Sony WH-1000XM5", price=29990, original_price=34990, rating=4.8, review_count=3000, category="headphones", brand="Sony", specifications={"type":"Over-ear","noise_cancellation":"Yes"}),
                Product(title="Samsung Odyssey G7 32", price=42990, original_price=49990, rating=4.6, review_count=800, category="monitors", brand="Samsung", specifications={"size":"32 inch","resolution":"1440p","refresh_rate":"240Hz"}),
                Product(title="LG 27GP850-B UltraGear", price=34990, rating=4.5, review_count=650, category="monitors", brand="LG", specifications={"size":"27 inch","resolution":"1440p","refresh_rate":"165Hz"}),
            ]
            db.add_all(products)
            await db.commit()
            print(f"[DB] Seeded {len(products)} products + admin user")

    asyncio.run(seed())

def open_browser():
    time.sleep(2)
    webbrowser.open("http://localhost:8000/chat")

def start_server():
    print("[SERVER] Starting backend at http://localhost:8000")
    print("[SERVER] Chat UI at http://localhost:8000/chat")
    print("[SERVER] API Docs at http://localhost:8000/docs")
    print("[SERVER] Press Ctrl+C to stop\n")
    subprocess.run([sys.executable, "-m", "uvicorn", "api.main:app",
                     "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    print("=" * 50)
    print("  AI Shopping Assistant - Starting...")
    print("=" * 50)
    check_deps()
    seed_database()
    threading.Thread(target=open_browser, daemon=True).start()
    start_server()
