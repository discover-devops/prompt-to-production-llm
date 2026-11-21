from types import SimpleNamespace
from summariser import calculate_cost, summarise


def test_cost():
    # 1000 input tokens at $2, 500 output tokens at $8 = $0.006
    assert round(calculate_cost(1000, 500, 2.0, 8.0), 6) == 0.006


class DummyChef:
    """A fake OpenAI client. No internet, no cost, same answer every time."""

    def __init__(self):
        self.responses = SimpleNamespace(create=self.create)

    def create(self, model, instructions, input):
        return SimpleNamespace(
            output_text="Payment deducted, order not created.",
            usage=SimpleNamespace(input_tokens=35, output_tokens=10),
        )


def test_summarise_returns_summary_and_tokens():
    summary, input_tokens, output_tokens = summarise(DummyChef(), "any-model", "Paisa kat gaya")
    assert summary == "Payment deducted, order not created."
    assert input_tokens == 35
    assert output_tokens == 10
