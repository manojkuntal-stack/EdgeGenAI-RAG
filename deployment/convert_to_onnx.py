from transformers import AutoModelForCausalLM
import torch

model_name = "distilgpt2"

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(model_name)
model.eval()

# IMPORTANT FIX
model.config.use_cache = False

print("Creating dummy input...")
dummy_input = torch.randint(0, 1000, (1, 10))

print("Converting to ONNX...")

torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    input_names=["input_ids"],
    output_names=["logits"],
    opset_version=13,
    do_constant_folding=True,
    export_params=True
)

print("✅ model.onnx created successfully!")