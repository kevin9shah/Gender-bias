"""Counterfactual prompt-pair generator.

For each base scenario, produces male/female prompt pairs across all prompt
variants and all name pairs, linked by a shared counterfactual_id so they can
be matched during evaluation.
"""
from dataclasses import dataclass

from src.data.scenarios import Scenario
from src.prompting.templates import NAME_PAIRS, PROMPT_VARIANTS, TASK_NOUN_BY_DOMAIN


@dataclass
class PromptRecord:
    scenario_id: str
    domain: str
    prompt_id: str
    prompt_variant: int
    gender: str
    name: str
    prompt: str
    counterfactual_id: str


def _facts_block(facts: list[str]) -> str:
    return "The candidate has:\n" + "\n".join(f"- {f}" for f in facts)


def generate_counterfactual_set(
    scenario: Scenario, name_pair_index: int = 0, n_variants: int | None = None
) -> list[PromptRecord]:
    """Cross product of {male, female} x {prompt variants} for one scenario,
    using one fixed name pair (name_pair_index) so name identity is held
    constant across variants within a scenario."""
    male_name, female_name = NAME_PAIRS[name_pair_index % len(NAME_PAIRS)]
    task_noun = TASK_NOUN_BY_DOMAIN[scenario.domain]
    facts_block = _facts_block(scenario.facts)
    context = f"{{name}} is being considered for a {scenario.role_or_context}."

    variants = PROMPT_VARIANTS[:n_variants] if n_variants else PROMPT_VARIANTS
    records: list[PromptRecord] = []
    for variant_idx, template in enumerate(variants):
        cf_id = f"{scenario.scenario_id}_V{variant_idx:02d}"
        for gender, name in (("male", male_name), ("female", female_name)):
            prompt = template.format(
                context=context.format(name=name),
                facts_block=facts_block,
                name=name,
                task_noun=task_noun,
            )
            prompt_id = f"{scenario.scenario_id}_V{variant_idx:02d}_{gender[0].upper()}"
            records.append(
                PromptRecord(
                    scenario_id=scenario.scenario_id,
                    domain=scenario.domain,
                    prompt_id=prompt_id,
                    prompt_variant=variant_idx,
                    gender=gender,
                    name=name,
                    prompt=prompt,
                    counterfactual_id=cf_id,
                )
            )
    return records


def generate_all(scenarios: list[Scenario], n_variants: int | None = None) -> list[PromptRecord]:
    all_records: list[PromptRecord] = []
    for i, s in enumerate(scenarios):
        all_records.extend(generate_counterfactual_set(s, name_pair_index=i, n_variants=n_variants))
    return all_records
