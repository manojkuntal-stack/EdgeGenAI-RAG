import torch
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("distilgpt2")

quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)

torch.save(quantized_model.state_dict(), "quantized_model.pth")

print("Quantized model saved!")