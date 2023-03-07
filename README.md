# Whisper CLI
Whisper CLI is a command-line interface for transcribing and translating audio using OpenAI's Whisper API. It also allows you to manage multiple OpenAI API keys as separate environments.

To install Whisper CLI, simply run:

```sh
pip install whisper-cli
```

## Setup
To get started with Whisper CLI, you'll need to set your OpenAI API key. You can do this using the following command:

```sh
whisper key set <openai_api_key>
```

This will set the API key for the default environment. If you want to use a different API key, you can set up an alternative environment by running:

```sh
whisper key set <openai_api_key> --env <env_name>
```

To activate an alternative environment, run:

```sh
whisper env activate <env_name>
```

## Usage

Whisper CLI supports two main functionalities: translation and transcription.

### Translation
To translate an audio file, simply run:

```sh
whisper translate <file_name>
```

### Transcription
To transcribe an audio file, run:

```sh
whisper transcribe <file_name>
```

## Development
If you'd like to contribute to Whisper CLI, you'll need to set up a development environment with Python 3.10.9.

```sh
python=3.10.9
```

Happy transcribing and translating with Whisper CLI.
