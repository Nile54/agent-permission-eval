"""Policy receives trusted grants, proposed calls, and its own usage state only."""
import json

from .model import Decision


def fingerprint(action):
    # JSON serialization distinguishes bool/int and ignores dictionary key order.
    return json.dumps(action.as_dict(), sort_keys=True, separators=(",", ":"), allow_nan=False)


class Policy:
    def __init__(self, mode, grants):
        if mode not in MODES:
            raise ValueError("Unknown policy: " + mode)
        self.mode = mode
        self.remaining = {}
        self.tools = set()
        for grant in grants:
            key = fingerprint(grant.action)
            self.remaining[key] = self.remaining.get(key, 0) + grant.uses
            self.tools.add(grant.action.tool)

    def check(self, action):
        if self.mode == "allow_all":
            return Decision(True, "unrestricted baseline")
        if self.mode == "read_only":
            allowed = action.tool in {"notes.read", "email.read"}
            return Decision(allowed, "reads only; all mutations denied")
        if self.mode == "tool_only":
            return Decision(action.tool in self.tools, "tool-name grant only")
        key = fingerprint(action)
        if self.remaining.get(key, 0) <= 0:
            return Decision(False, "no unused grant for this exact tool and arguments")
        self.remaining[key] -= 1
        return Decision(True, "exact task grant consumed")


MODES = ("allow_all", "read_only", "tool_only", "scoped")
