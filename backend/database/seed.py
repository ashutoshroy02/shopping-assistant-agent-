import asyncio
import uuid
from datetime import datetime

from sqlalchemy import select

from config import get_settings
from database.connection import async_session_factory, init_db
from database.models import Product, User
from services.auth import get_password_hash


async def seed_database():
    await init_db()

    async with async_session_factory() as db:
        existing_admin = await db.execute(
            select(User).where(User.email == "admin@shopping-assistant.com")
        )
        if existing_admin.scalar_one_or_none():
            print("Database already seeded.")
            return

        admin = User(
            id=uuid.uuid4(),
            name="Admin",
            email="admin@shopping-assistant.com",
            password_hash=get_password_hash("admin123"),
            role="admin",
        )
        db.add(admin)

        demo_user = User(
            id=uuid.uuid4(),
            name="Demo User",
            email="demo@shopping-assistant.com",
            password_hash=get_password_hash("demo123"),
            role="user",
            preferences={"categories": ["laptops", "phones"], "budget": 100000},
        )
        db.add(demo_user)

        products = [
            Product(
                title="ASUS ROG Strix G15 Gaming Laptop",
                description="High-performance gaming laptop with RTX 3060",
                price=89990,
                original_price=99990,
                rating=4.5,
                review_count=1250,
                category="laptops",
                brand="ASUS",
                specifications={
                    "ram": "16GB DDR4",
                    "storage": "512GB NVMe SSD",
                    "gpu": "NVIDIA RTX 3060 6GB",
                    "processor": "AMD Ryzen 7 5800H",
                    "display": "15.6 inch 144Hz",
                },
                images=["https://example.com/asus-rog.jpg"],
            ),
            Product(
                title="MSI Katana GF76 Gaming Laptop",
                description="Powerful gaming laptop with RTX 3050",
                price=74990,
                original_price=84990,
                rating=4.3,
                review_count=890,
                category="laptops",
                brand="MSI",
                specifications={
                    "ram": "16GB DDR4",
                    "storage": "512GB NVMe SSD",
                    "gpu": "NVIDIA RTX 3050 4GB",
                    "processor": "Intel Core i7-11800H",
                    "display": "17.3 inch 144Hz",
                },
                images=["https://example.com/msi-katana.jpg"],
            ),
            Product(
                title="Lenovo IdeaPad Gaming 3",
                description="Budget gaming laptop with RTX 3050",
                price=64990,
                original_price=74990,
                rating=4.2,
                review_count=1500,
                category="laptops",
                brand="Lenovo",
                specifications={
                    "ram": "8GB DDR4",
                    "storage": "256GB NVMe SSD",
                    "gpu": "NVIDIA RTX 3050 4GB",
                    "processor": "AMD Ryzen 5 5600H",
                    "display": "15.6 inch 120Hz",
                },
                images=["https://example.com/lenovo-ideapad.jpg"],
            ),
            Product(
                title="iPhone 15 Pro Max",
                description="Latest Apple flagship with A17 Pro chip",
                price=159900,
                original_price=159900,
                rating=4.7,
                review_count=2500,
                category="smartphones",
                brand="Apple",
                specifications={
                    "ram": "8GB",
                    "storage": "256GB",
                    "processor": "A17 Pro",
                    "display": "6.7 inch OLED 120Hz",
                    "camera": "48MP + 12MP + 12MP",
                },
                images=["https://example.com/iphone15.jpg"],
            ),
            Product(
                title="Samsung Galaxy S24 Ultra",
                description="Premium Android flagship with S Pen",
                price=134999,
                original_price=134999,
                rating=4.6,
                review_count=1800,
                category="smartphones",
                brand="Samsung",
                specifications={
                    "ram": "12GB",
                    "storage": "256GB",
                    "processor": "Snapdragon 8 Gen 3",
                    "display": "6.8 inch AMOLED 120Hz",
                    "camera": "200MP + 12MP + 50MP + 10MP",
                },
                images=["https://example.com/s24ultra.jpg"],
            ),
        ]

        for product in products:
            db.add(product)

        await db.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())
