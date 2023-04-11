import openai
import typer
from rich import print

import whisper_cli.env as env
from whisper_cli.utils import (_check_response_format, get_api_key,
                               get_file_content, show_result)

app = typer.Typer(no_args_is_help=True)
app.add_typer(env.env_app)
app.add_typer(env.key_app)


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
