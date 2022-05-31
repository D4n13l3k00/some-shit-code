import ddgoimages
import asyncio


async def main():
    api = ddgoimages.DuckDuckGoImagesSearchAPI()

    print(await api.getPictures("anime", nsfw=False))


if __name__ == "__main__":
    asyncio.run(main())
