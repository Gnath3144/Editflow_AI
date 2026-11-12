#!/usr/bin/env python3
import os
import yaml
import sys

def main():
    workflows_dir = ".github/workflows"
    files = [f for f in os.listdir(workflows_dir) if f.endswith((".yml", ".yaml"))]
    errors = []

    print(f"Validating {len(files)} workflow files in {workflows_dir}...")
    for f in sorted(files):
        path = os.path.join(workflows_dir, f)
        try:
            with open(path, "r", encoding="utf-8") as stream:
                data = yaml.safe_load(stream)
                if not data or "name" not in data or "jobs" not in data:
                    raise ValueError("Workflow must have 'name' and 'jobs'")
                jobs = list(data["jobs"].keys())
                print(f"[+] {f}: VALID (Jobs: {jobs})")
        except Exception as e:
            errors.append((f, str(e)))

    # Validate dependabot.yml
    try:
        with open(".github/dependabot.yml", "r", encoding="utf-8") as stream:
            dep = yaml.safe_load(stream)
            if not dep or dep.get("version") != 2:
                raise ValueError("Dependabot must be version 2")
            print("[+] dependabot.yml: VALID")
    except Exception as e:
        errors.append(("dependabot.yml", str(e)))

    # Validate issue templates
    templates_dir = ".github/ISSUE_TEMPLATE"
    if os.path.exists(templates_dir):
        for t in sorted(os.listdir(templates_dir)):
            if t == "config.yml":
                try:
                    with open(os.path.join(templates_dir, t), "r", encoding="utf-8") as stream:
                        c_data = yaml.safe_load(stream)
                        if "blank_issues_enabled" not in c_data:
                            raise ValueError("config.yml must specify blank_issues_enabled")
                        print("[+] ISSUE_TEMPLATE/config.yml: VALID")
                except Exception as e:
                    errors.append((f"ISSUE_TEMPLATE/{t}", str(e)))
            elif t.endswith(".yml"):
                try:
                    with open(os.path.join(templates_dir, t), "r", encoding="utf-8") as stream:
                        t_data = yaml.safe_load(stream)
                        if not t_data or "name" not in t_data:
                            raise ValueError("Template must have a name")
                        print(f"[+] ISSUE_TEMPLATE/{t}: VALID")
                except Exception as e:
                    errors.append((f"ISSUE_TEMPLATE/{t}", str(e)))

    if errors:
        print("\n[!] Errors encountered:")
        for name, err in errors:
            print(f"  - {name}: {err}")
        sys.exit(1)
    else:
        print("\nAll GitHub Actions workflows, Dependabot, and Issue Templates verified 100% syntactically VALID.")

if __name__ == "__main__":
    main()
