from .Utils.ai_utils import GPT


plans = [
    {
        "name": "Basic",
        "price_in_USD": ,
        "credits": 250_000,
    },
    {
        "name": "Standard",
        "price in USD": 15,
        "credits": 1_000_000,
    },
    {
        "name": "Premium",
        "price in USD": 30,
        "credits": 3_000_000,
    },
]



class Credit:

    class Operation:
        chat = "chat"
        improvement = "improvement"
        completion = "completion"
        rewrite_wiki_section = "rewrite_wiki_section"

    def calc(
        operation,
        n_tokens,
        model=None
    ):
        
        if operation == Credit.Operation.chat:
            if model == GPT.Models.gpt_35_1106:
                return n_tokens
            elif model in (
                GPT.Models.gpt_4,
                GPT.Models.gpt_4_turbo,
                GPT.Models.gpt_4_vision
            ):
                return n_tokens * 15
        elif operation == Credit.Operation.completion:
            return n_tokens * 2
        elif operation == Credit.Operation.improvement:
            return max((100, n_tokens * 2))
        elif operation == Credit.Operation.rewrite_wiki_section:
            return n_tokens
