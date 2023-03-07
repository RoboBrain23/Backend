import asyncio
import httpx

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjc3LCJpYXQiOjE2NzcxMjcyMDQsIm5iZiI6MTY3NzEyNzIwNCwianRpIjoiMzc2ZjBiNWItOGE5YS00Yjg5LWI0OWUtOTZjNTFhZTM5YTU4IiwiZXhwIjoxNjc3MTI5MDA0LCJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOmZhbHNlfQ.EgyT9mCZXzgX8e8qT-AmXs_cQ1A55hloi2hREPCsyV8"



async def send_request():
    async with httpx.AsyncClient() as client:
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "body_temperature": "36.5",
            "oximeter": "125.4",
            "heart_rate": "90.5",
            "sugar_level": "70.45",
            "patient_id": 77,
        }
        response = await client.post(
            "http://127.0.0.1:8000/chair/data", json=payload, headers=headers
        )
        print(response.text)


async def get_request():
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("http://127.0.0.1:8000/chair/data", headers=headers)
        print(response.text)


async def main():
    while True:
        await send_request()
        await asyncio.sleep(0.5)
        await get_request()
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())
