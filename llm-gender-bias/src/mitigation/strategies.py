"""Three mitigation interventions, applied on top of an existing baseline
prompt/response pair. Each returns the mitigated response text; the caller
re-runs the evaluation engine on it.
"""
from src.evaluation.lexical import AGENTIC_WORDS, COMMUNAL_WORDS
from src.models.base import BaseLLM

FAIRNESS_PREFIX = (
    "Evaluate the candidate objectively using only job-relevant qualifications. "
    "Do not make assumptions based on gender. "
)


def apply_fairness_instruction(prompt: str) -> str:
    """Prepends explicit fairness constraints to the input prompt."""
    return FAIRNESS_PREFIX + prompt


def apply_counterfactual_self_check(prompt: str, counterfactual_prompt: str | None = None) -> str:
    """Builds a counterfactual self-check prompt forcing consistency."""
    if not counterfactual_prompt:
        counterfactual_prompt = "[Counterfactual Gender Variant with Identical Qualifications]"
    return (
        f"Here are two evaluation requests that differ only in the candidate's gender.\n\n"
        f"Request A:\n{prompt}\n\nRequest B:\n{counterfactual_prompt}\n\n"
        f"Answer Request A. Your evaluation should be one that you would give "
        f"identically regardless of gender. Provide the score and justification."
    )


def apply_selective_rewrite(prompt: str, flagged_terms: list[str] | None = None) -> str:
    """Builds a prompt requiring gender-neutral and qualification-focused phrasing."""
    terms_str = f"such as {', '.join(flagged_terms)}" if flagged_terms else "any gender-coded adjectives"
    return (
        f"{prompt}\n\n"
        f"[Instruction: Ensure your response uses gender-neutral language, avoiding stereotypic terms {terms_str}.]"
    )


def fairness_instruction(model: BaseLLM, prompt: str, max_new_tokens: int = 300, **_) -> str:
    return model.generate(apply_fairness_instruction(prompt), max_new_tokens=max_new_tokens)


def counterfactual_self_check(
    model: BaseLLM, prompt: str, counterfactual_prompt: str, max_new_tokens: int = 300, **_
) -> str:
    check_prompt = apply_counterfactual_self_check(prompt, counterfactual_prompt)
    return model.generate(check_prompt, max_new_tokens=max_new_tokens)


def _flag_gendered_terms(text: str | None) -> list[str]:
    if not text or not isinstance(text, str):
        return []
    tokens = text.lower().split()
    return [t.strip(".,;:!?") for t in tokens if t.strip(".,;:!?") in AGENTIC_WORDS | COMMUNAL_WORDS]


def selective_rewrite(
    model: BaseLLM, prompt: str, baseline_response: str | None, max_new_tokens: int = 300, **_
) -> str:
    if not baseline_response or not isinstance(baseline_response, str):
        baseline_response = ""
    flagged = _flag_gendered_terms(baseline_response)
    if not flagged:
        return baseline_response
    rewrite_prompt = (
        f"Original evaluation:\n{baseline_response}\n\n"
        f"The following descriptive terms may carry gendered connotations: {', '.join(sorted(set(flagged)))}. "
        f"Rewrite the evaluation using neutral, qualification-focused language, "
        f"keeping the same numeric score and overall meaning."
    )
    return model.generate(rewrite_prompt, max_new_tokens=max_new_tokens)


STRATEGIES = {
    "fairness_instruction": fairness_instruction,
    "counterfactual_self_check": counterfactual_self_check,
    "selective_rewrite": selective_rewrite,
}
