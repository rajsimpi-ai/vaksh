import sys
import argparse
from .cli import run_cli

def main():
    parser = argparse.ArgumentParser(
        prog="vak",
        description="VakSh — Text to Shell, Words to Power"
    )

    parser.add_argument(
        "prompt",
        nargs="*",
        help="Instruction to process, e.g. vak \"make a folder named images\""
    )

    parser.add_argument(
        "--provider",
        choices=["groq", "local"],
        default="groq",
        help="Choose which LLM provider to use (default: groq)"
    )

    args = parser.parse_args()

    if not args.prompt:
        parser.print_help()
        sys.exit(1)

    user_prompt = " ".join(args.prompt)
    run_cli(user_prompt, provider=args.provider)
