from whisper_cli.env import _read_user_config
from typing import Optional


def get_file_type(file_name: str) -> str:
    """Returns the file type of the file_name."""
    return file_name.split(".")[-1]


def _check_response_format(response_format: str | None):
    if response_format is None:
        return None
    elif response_format in ["json", "srt", "verbose_json", "vtt"]:
        return response_format
    else:
        raise ValueError("Response format not supported by OpenAI.")


def get_file_content(file_name: str) -> str:
    """Returns the content of the file_name."""

    if get_file_type(file_name) not in [
        "mp3",
        "mp4",
        "mpeg",
        "mpga",
        "m4a",
        "wav",
        "webm",
    ]:
        raise ValueError("File type not supported.")

    return open(file_name, "rb")


def get_api_key(env: str = "default") -> str:
    """Returns the API key for the current environment."""
    user_config = _read_user_config()
    for key, value in user_config.items():
        if "active" in value:
            return value["api_key"]

    raise ValueError(
        "No active environment found. Activate one using `whisper activate-env`."
    )


def show_result(result, response_format: Optional[str]):
    """Show result."""
    if response_format is None:
        response_format = "json"

    if response_format == "json":
        print(result["text"])
    else:
        print(result)
