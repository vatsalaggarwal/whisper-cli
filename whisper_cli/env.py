import os

import toml
import typer
from rich import print

# TODO: factor this further into token setting app?
env_app = typer.Typer(
    name="env", help="Set the current environment.", no_args_is_help=True
)
key_app = typer.Typer(name="key", help="Manage OpenAI API keys.", no_args_is_help=True)

user_config_path: str = os.environ.get("OPENAI_CONFIG_PATH") or os.path.expanduser(
    "~/.openai.toml"
)


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


@key_app.command("set")
def set_key(api_key: str, env: str = "default"):
    """Save OpenAI key."""
    _store_user_config({"api_key": api_key}, env=env)


@env_app.command("activate")
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


@env_app.command("list")
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
