import subprocess
from .llm_providers import groq_llm, local_llm  
def run_cli(prompt: str, provider: str = "groq"):
    if provider == "groq":
        command = groq_llm(prompt)
    elif provider == "local":
        command = local_llm(prompt)
    else:
        raise ValueError(f"Unknown provider: {provider}")

    print(f"\nSuggested command:\n{prompt} : \"{command}\"\n")
    choice = input("Press [Enter] to execute, [E] to edit prompt, [C] to cancel: ").strip().lower()

    if choice == "":
        print(f"\n Executing: {command}\n")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("Error:\n", result.stderr)
        except Exception as e:
            print("Execution failed:", e)

    elif choice == "e":
        new_prompt = input("✏️ Enter new prompt: ")
        run_cli(new_prompt)
    else:
        print("Cancelled.")