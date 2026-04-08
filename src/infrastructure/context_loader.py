from pathlib import Path
from typing import List


class ContextLoader:
    @staticmethod
    def load_system_prompt() -> str:
        path = Path("system_prompt/asistente.md")
        if not path.exists():
            return "Eres un asistente de cafetería."
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()

    @staticmethod
    def load_rules() -> str:
        path = Path("rules/comportamiento.md")
        if not path.exists():
            return ""
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()

    @staticmethod
    def load_knowledge_files() -> List[str]:
        knowledge_dir = Path("knowledge")
        if not knowledge_dir.exists():
            return []
        knowledge_files = list(knowledge_dir.glob("*.md"))
        contents = []
        for file_path in knowledge_files:
            with open(file_path, "r", encoding="utf-8") as f:
                contents.append(f.read().strip())
        return contents

    @staticmethod
    def load_full_context() -> str:
        system_prompt = ContextLoader.load_system_prompt()
        rules = ContextLoader.load_rules()
        knowledge = ContextLoader.load_knowledge_files()
        full_context = system_prompt + "\n\n" + rules + "\n\n" + "\n\n".join(knowledge)
        return full_context