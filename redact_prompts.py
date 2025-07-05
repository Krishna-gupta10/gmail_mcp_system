input_file = "prompt_log.md"
output_file = "prompt_log_redacted.md"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        if line.strip().startswith("### Prompt Used:"):
            outfile.write(line)
        elif line.strip():
            outfile.write("[REDACTED PROMPT]\n")
        else:
            outfile.write("\n")
