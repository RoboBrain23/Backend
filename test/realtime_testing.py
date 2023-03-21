import asyncio
import httpx


async def send_request():
    async with httpx.AsyncClient() as client:
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "temperature": "36.5",
            "oximeter": "125.4",
            "pulse_rate": "90.5",
            "sugar_level": "70.45",
            "chair_id": "12315",
        }
        response = await client.post("http://127.0.0.1:8000/chair/data", json=payload)
        print(response.text)


async def get_request():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/chair/data/12315")
        print(response.text)


async def main():
    while True:
        await send_request()
        await asyncio.sleep(0.5)
        await get_request()
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())
