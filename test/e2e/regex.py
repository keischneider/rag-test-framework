# A wrapper evaluator for rule-based assertion
# This module provides functionality to evaluate with regular expressions
# against input data and assert expected outcomes.

from typing import Dict, Any
import re

class RegexEvaluator:
    def __init__(self, pattern: str, must_match: bool = True):
        self.pattern = re.compile(pattern)
        self.must_match = must_match

    def evaluate(self, output: str) -> Dict[str, Any]:
        match = bool(self.pattern.search(output))
        if self.must_match and not match:
            return {"score": 0, "error": f"Pattern {self.pattern.pattern} not found in: {output}"}
        return {"score": 1 if match else 0, "output": output}

# Example use
evaluator = RegexEvaluator(r"\d+%")  # must contain interest rate
result = evaluator.evaluate("The savings rate is 3%.")
print(result)  # {"score": 1, "output": "..."}