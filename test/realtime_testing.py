import asyncio
import httpx

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImlhdCI6MTY3NjM0OTEwNSwibmJmIjoxNjc2MzQ5MTA1LCJqdGkiOiJiMDI5Mjk5ZC0xNGNmLTRiNWYtYmIwMy1kNzUwYWE5YTNjOWUiLCJleHAiOjE2NzYzNTA5MDUsInR5cGUiOiJhY2Nlc3MiLCJmcmVzaCI6ZmFsc2V9.QKklYPPZeMkqvOWtsPSwFyvSGJ-14P8sGMDwU79_RuQ"



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
            "patient_id": 6,
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
