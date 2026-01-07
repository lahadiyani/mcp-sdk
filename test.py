import logging
from shell.composition import build_dispatcher
from protocol.request import MCPRequest
from utils.logging import get_logger
from pathlib import Path

logger = get_logger("MCP", level=logging.DEBUG)

OUTPUT_DIR = Path("test_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def test_pollinations_text():
    logger.debug("=== TEST: Pollinations Text ===")
    dispatcher = build_dispatcher()

    request_dict = {
        "tool": "ai",
        "input": {"prompt": "apa itu mcp stateless secara singkat?"},
        "ai": {"provider": "pollinations", "type": "text"}
    }

    logger.debug("Creating MCPRequest with: %s", request_dict)
    request = MCPRequest.from_dict({**request_dict, "tool": "ai"})
    logger.debug("MCPRequest created: %s", request.to_dict())

    response = dispatcher.dispatch(request)
    logger.debug("Dispatcher returned: %s", response.to_dict())
    if response.success:
        print("Text output:", response.data)
    else:
        print("Error:", response.error)


def test_pollinations_image():
    logger.debug("=== TEST: Pollinations Image ===")
    dispatcher = build_dispatcher()

    request_dict = {
        "tool": "generate",
        "input": {
            "prompt": "A cat and a dog kiss on a park bench",
            "negative_prompt": "2D, pixel, cartoon",
            "save_to_file": True,  # tambahkan flag save file
            "file_path": str(OUTPUT_DIR / "cat_dogs.png")
        },
        "ai": {"provider": "pollinations_image", "type": "image"}
    }

    logger.debug("Creating MCPRequest with: %s", request_dict)
    request = MCPRequest.from_dict({**request_dict, "tool": "ai"})
    logger.debug("MCPRequest created: %s", request.to_dict())

    response = dispatcher.dispatch(request)
    logger.debug("Dispatcher returned: %s", response.to_dict())
    if response.success:
        file_path = response.data.get("image")
        if file_path:
            print("Image saved at:", file_path)
            logger.debug("Image saved successfully at %s", file_path)
    else:
        logger.debug("Error: %s", response.error)


# ada bug di Pollinations audio client, jadi test ini di-comment dulu
def test_pollinations_audio():
    logger.debug("=== TEST: Pollinations Audio ===")
    dispatcher = build_dispatcher()

    request_dict = {
        "tool": "generate",
        "input": {
            "prompt": "Halo, bisa jelaskan apa itu mcp stateless secara singkat?",
            "file_path": str(OUTPUT_DIR / "mcp_stateless.mp3"),  # tempat simpan MP3
        },
        "ai": {"provider": "pollinations_audio", "type": "audio"}  # type audio
    }

    logger.debug("Creating MCPRequest with: %s", request_dict)
    request = MCPRequest.from_dict({**request_dict, "tool": "ai"})
    logger.debug("MCPRequest created: %s", request.to_dict())

    response = dispatcher.dispatch(request)
    logger.debug("Dispatcher returned: %s", response.to_dict())

    if response.success:
        mp3_path = response.data.get("audio")  # executor akan simpan path MP3
        if mp3_path:
            print("Audio saved at:", mp3_path)
            logger.debug("Audio saved successfully at %s", mp3_path)
    else:
        logger.debug("Error: %s", response.error)



if __name__ == "__main__":
    test_pollinations_text()
    test_pollinations_image()
    # test_pollinations_audio()
