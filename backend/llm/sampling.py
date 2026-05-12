import torch
import torch.nn.functional as F

def apply_sampling(logits, temperature=0.8, top_k=50, top_p=0.95):

    logits = logits / temperature

    # Top-K filtering
    top_k_values, top_k_indices = torch.topk(logits, top_k)

    probs = F.softmax(top_k_values, dim=-1)

    # Top-P filtering
    sorted_probs, sorted_indices = torch.sort(
        probs,
        descending=True
    )

    cumulative_probs = torch.cumsum(sorted_probs, dim=-1)

    sorted_probs[cumulative_probs > top_p] = 0

    sorted_probs = sorted_probs / sorted_probs.sum()

    sampled_index = torch.multinomial(
        sorted_probs,
        1
    )

    next_token = sorted_indices[sampled_index]

    return next_token