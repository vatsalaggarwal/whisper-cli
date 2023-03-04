import typer
import os
import toml

import openai
from rich import print

user_config_path: str = os.environ.get("OPENAI_CONFIG_PATH") or os.path.expanduser(
    "~/.openai.toml"
)

app = typer.Typer()


def _read_user_config():
    if os.path.exists(user_config_path):
        with open(user_config_path) as f:
            return toml.load(f)
    else:
        return {}


def _write_user_config(user_config):
    with open(user_config_path, "w") as f:
        toml.dump(user_config, f)


def _store_user_config(new_settings, env="default"):
    user_config = _read_user_config()
    user_config.setdefault(env, {}).update(**new_settings)
    _write_user_config(user_config)


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


@app.command()
def set_key(api_key: str, env: str = "default"):
    """Save OpenAI key."""
    _store_user_config({"api_key": api_key}, env=env)


@app.command()
def activate_env(env: str = "default"):
    """Activate environment."""
    config = _read_user_config()

    if env not in config:
        raise ValueError(
            f"Environment {env} not found. Create it using `whisper set-key`."
        )

    for key, value in config.items():
        if "active" in value:
            del config[key]["active"]
    config[env]["active"] = True
    _write_user_config(config)


@app.command()
def list_envs():
    """List all environments."""
    config = _read_user_config()

    # print config.keys each on a new line
    print("[bold]Environments[/bold]")
    for key in config.keys():
        if "active" in config[key]:
            print(f" * [bold red]\[active][/bold red] {key}")
        else:
            print(f" * {key}")


def get_api_key(env: str = "default") -> str:
    """Returns the API key for the current environment."""
    user_config = _read_user_config()
    for key, value in user_config.items():
        if "active" in value:
            return value["api_key"]

    raise ValueError(
        "No active environment found. Activate one using `whisper activate-env`."
    )


def show_result(result, response_format: str | None):
    """Show result."""
    if response_format is None:
        response_format = "json"

    if response_format == "json":
        print(result["text"])
    else:
        print(result)


@app.command()
def transcribe(
    file_name: str,
    model: str = "whisper-1",
    prompt: str | None = None,
    response_format: str | None = None,
    temperature: float = 0,
    language: str | None = None,
):
    """Transcribe audio file using whisper."""
    openai.api_key = get_api_key()

    transcript = openai.Audio.transcribe(
        model,
        get_file_content(file_name),
        prompt=prompt,
        response_format=_check_response_format(response_format),
        temperature=temperature,
        language=language,
    )

    # TODO: return based on response_format
    show_result(transcript, response_format)


@app.command()
def translate(
    file_name: str,
    model: str = "whisper-1",
    prompt: str | None = None,
    response_format: str | None = None,
    temperature: float = 0,
):
    """Translate audio file using whisper."""
    openai.api_key = get_api_key()

    translation = openai.Audio.translate(
        model,
        get_file_content(file_name),
        prompt=prompt,
        response_format=_check_response_format(response_format),
        temperature=temperature,
    )

    show_result(translation, response_format)


if __name__ == "__main__":
    app()
