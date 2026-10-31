with open("stage6.txt", "r", encoding="utf-8") as f:
    sample = [f.readline() for _ in range(100)]

with open("sample_view.txt", "w", encoding="utf-8") as f:
    f.writelines(sample)

print("Saved first 100 lines to sample_view.txt — open it now!")
