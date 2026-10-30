"""A deliberately susceptible scripted agent, not an LLM or injection detector."""
import json

from .model import Action

MARKER = "\nUNTRUSTED_ACTION_JSON="


class ScriptedAgent:
    def __init__(self, source, intended, recover=False):
        self.source = source
        self.intended = intended
        self.recover = recover
        self.continue_after_attack = False

    def propose(self, observation):
        # Simulate an agent accepting an attacker-controlled tool-output directive.
        if MARKER in observation:
            payload = json.loads(observation.split(MARKER, 1)[1])
            self.continue_after_attack = payload.get("then_continue", False)
            return Action(payload["tool"], payload["args"])
        return self.intended

    def after_acceptance(self):
        return self.intended if self.continue_after_attack else None

    def after_denial(self):
        # Controlled ablation: fallback to the original trusted task plan.
        return self.intended if self.recover else None
