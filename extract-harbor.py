import os
import json
import re

base_dir = f"jobs/mmau-gpt4o"

with open(f"mmau-test-mini.json", "r", encoding="utf-8") as f:
    data = json.load(f)

echo_pat = re.compile(r'echo\s+-n\s+([\'"])(.*?)\1\s*>')

for item in data:
    prefix = item["id"]
    answer = None

    for dirname in os.listdir(base_dir):
        if not dirname.startswith(prefix[:-4]):
            continue

        traj_path = os.path.join(base_dir, dirname, "agent", "trajectory.json")
        if not os.path.exists(traj_path):
            continue

        with open(traj_path, "r", encoding="utf-8") as f:
            traj = json.load(f)

        for step in traj.get("steps", []):
            for tc in step.get("tool_calls", []):
                cmd = tc.get("arguments", {}).get("keystrokes", "")
                if cmd.startswith("echo -n"):
                    m = echo_pat.search(cmd)
                    if m:
                        answer = m.group(2)
                        break
            if answer:
                break

        break

    item["model_output"] = answer

out_path = f"mmau-gpt4o-output.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
