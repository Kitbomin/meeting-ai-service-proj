# import whisperx
# import torch

# device = "cuda" if torch.cuda.is_available() else "cpu"

# print("Device:", device)

# if device == "cuda":
#     print(torch.cuda.get_device_name(0))

# audio_file = "sample.wav"

# model = whisperx.load_model(
#     "base",
#     device=device,
#     compute_type="float32"
# )

# audio = whisperx.load_audio(audio_file)

# result = model.transcribe(audio)

# print(result["segments"])

from app.services.stt_service import transcribe_audio

result = transcribe_audio("sample.wav")

print("\n===== RESULT =====\n")

for item in result:

    print(
        f"[{item['speaker']}] "
        f"{item['text']}"
    )