from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """Common interface for every model slot.

    The pipeline only ever calls .generate(prompt). Swapping a local model
    for a real provider API means adding one subclass here -- nothing else
    in the pipeline changes.
    """

    name: str
    family: str
    version: str = "local"

    @abstractmethod
    def generate(self, prompt: str, max_new_tokens: int = 96) -> str:
        raise NotImplementedError
