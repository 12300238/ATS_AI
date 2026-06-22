from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Iterable

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

DEFAULT_MODEL_ID = "openai-community/gpt2"

SYSTEM_PROMPT = """Tu es un assistant IA specialise dans l'accompagnement professionnel.
Tu aides les candidats a ameliorer leur CV, leurs lettres de motivation, leur portfolio
et leur preparation aux entretiens.

Regles de reponse:
- Reponds en francais, avec un ton clair, encourageant et professionnel.
- Donne des conseils concrets, actionnables et adaptes au contexte donne.
- Quand une information manque, explique l'hypothese que tu fais ou pose une question courte.
- Pour un CV ou une lettre, propose des formulations precises et ameliorables.
- Ne promets jamais une embauche. Parle en termes de probabilite, pertinence et amelioration.
- Si la question sort du domaine carriere/recrutement, redirige poliment vers ton domaine."""


@dataclass(frozen=True)
class GenerationConfig:
    max_new_tokens: int = 500
    temperature: float = 0.4
    top_p: float = 0.9
    repetition_penalty: float = 1.08


class CVAdvisorModel:
    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        generation_config: GenerationConfig | None = None,
    ) -> None:
        self.model_id = model_id
        self.generation_config = generation_config or GenerationConfig()
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        self.generator = pipeline(
            "text-generation",
            model=AutoModelForCausalLM.from_pretrained(
                model_id,
                device_map="auto",
                dtype=self._torch_dtype(),
                trust_remote_code=True,
            ),
            tokenizer=self.tokenizer,
        )

    def ask(self, question: str, context: str | None = None) -> str:
        prompt = self._build_prompt(question=question, context=context)
        outputs = self.generator(
            prompt,
            max_new_tokens=self.generation_config.max_new_tokens,
            temperature=self.generation_config.temperature,
            top_p=self.generation_config.top_p,
            repetition_penalty=self.generation_config.repetition_penalty,
            do_sample=self.generation_config.temperature > 0,
            return_full_text=False,
        )
        return outputs[0]["generated_text"].strip()

    def _build_prompt(self, question: str, context: str | None = None) -> str:
        user_content = self._format_user_content(question=question, context=context)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]

        if hasattr(self.tokenizer, "apply_chat_template") and self.tokenizer.chat_template:
            return self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )

        return (
            f"{SYSTEM_PROMPT}\n\n"
            f"Question du candidat:\n{user_content}\n\n"
            "Reponse du conseiller:"
        )

    @staticmethod
    def _format_user_content(question: str, context: str | None = None) -> str:
        if context:
            return f"Contexte:\n{context.strip()}\n\nQuestion:\n{question.strip()}"
        return question.strip()

    @staticmethod
    def _torch_dtype() -> torch.dtype:
        if torch.cuda.is_available():
            return torch.float16
        return torch.float32


def interactive_chat(model: CVAdvisorModel) -> None:
    print("Assistant carriere pret. Tape 'quit' pour quitter.")
    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() in {"quit", "exit", "q"}:
            break
        if not question:
            continue
        print("\n" + model.ask(question))


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assistant IA CV et candidatures.")
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID)
    parser.add_argument("--question", "-q")
    parser.add_argument("--context", "-c")
    parser.add_argument("--max-new-tokens", type=int, default=GenerationConfig.max_new_tokens)
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> None:
    args = parse_args(argv)
    model = CVAdvisorModel(
        model_id=args.model_id,
        generation_config=GenerationConfig(max_new_tokens=args.max_new_tokens),
    )

    if args.question:
        print(model.ask(question=args.question, context=args.context))
        return

    interactive_chat(model)


if __name__ == "__main__":
    main()
