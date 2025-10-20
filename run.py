# Copyright (c) 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
import json
import os

# Python template directories
python_dirs = [
    "vefaas-native-python3.8-default",
    "vefaas-native-python3.9-default",
    "vefaas-native-python3.10-default",
    "vefaas-native-python3.12-default",
    "vefaas-python-tos-stream-unzip",
    "vefaas-python38-tos-auto-unzip",
]

# Final aggregated result
all_licenses = {}
distinct_licenses = set()

for dir_path in python_dirs:
    print(f"Processing {dir_path} ...")
    dir_abs = os.path.abspath(dir_path)

    site_packages = os.path.join(dir_abs, "site-packages")
    if not os.path.exists(site_packages):
        print(f"  Warning: {site_packages} does not exist. Skipping.")
        all_licenses[dir_path] = []
        continue

    try:
        # Run pip-licenses with PYTHONPATH pointing to site-packages
        result = subprocess.run(
            ["python3", "-m", "piplicenses", "--format=json"],
            capture_output=True,
            text=True,
            check=True,
            env={**os.environ, "PYTHONPATH": site_packages},
        )

        licenses_json = json.loads(result.stdout)
        all_licenses[dir_path] = licenses_json

        # Collect distinct license names
        for pkg in licenses_json:
            if "License" in pkg:
                distinct_licenses.add(pkg["License"])

    except subprocess.CalledProcessError as e:
        print(f"  Error running pip-licenses for {dir_path}: {e}")
        all_licenses[dir_path] = []
    except json.JSONDecodeError:
        print(f"  Error parsing JSON for {dir_path}")
        all_licenses[dir_path] = []

# Create final output with per-directory data + all distinct licenses
final_output = {
    "directories": all_licenses,
    "distinct_licenses": sorted(list(distinct_licenses)),
}

# Write aggregated results
output_file = "all_python_licenses.json"
with open(output_file, "w") as f:
    json.dump(final_output, f, indent=2)

print(f"Done for python! Aggregated license data saved to {output_file}")


# Go template directories
go_dirs = [
    "vefaas-golang-sns-to-rmq",
    "vefaas-native-microservice-kafka-to-es-exporter",
    "vefaas-golang-tos-trigger",
    "vefaas-golang-default",
    "vefaas-native-default",
    "vefaas-golang-cdn-refresh-preload",
]

all_golang_licenses = {}
distinct_golang_licenses = set()

for dir_path in go_dirs:
    print(f"Processing {dir_path} ...")
    dir_abs = os.path.abspath(dir_path)

    go_mod_path = os.path.join(dir_abs, "go.mod")
    if not os.path.exists(go_mod_path):
        print(f"  Warning: go.mod not found in {dir_path}. Skipping.")
        all_golang_licenses[dir_path] = []
        continue

    try:
        # Run go-licenses report, output CSV (module_path, license_type)
        result = subprocess.run(
            ["go-licenses", "report", "./..."],
            cwd=dir_abs,
            capture_output=True,
            text=True,
            check=True,
        )

        licenses_json = []
        output = result.stdout + "\n" + result.stderr  # merge stdout + stderr
        for line in output.strip().split("\n"):
            if not line or line.startswith("E") or line.startswith("W"):
                continue
            # Expected CSV: module_path,license_url,license_type
            parts = line.strip().split(",")
            if len(parts) >= 3:
                module_path = parts[0]
                license_type = parts[2] if parts[2] else "Unknown"
                licenses_json.append({"Module": module_path, "License": license_type})
                if license_type != "Unknown":
                    distinct_golang_licenses.add(license_type)

        all_golang_licenses[dir_path] = licenses_json

    except subprocess.CalledProcessError as e:
        print(f"  Error running `go-licenses report` for {dir_path}: {e}")
        all_golang_licenses[dir_path] = []

# Create final output
final_output = {
    "directories": all_golang_licenses,
    "distinct_licenses": sorted(list(distinct_golang_licenses)),
}

# Write to JSON file
output_file = "all_golang_licenses.json"
with open(output_file, "w") as f:
    json.dump(final_output, f, indent=2)

print(f"Done for golang! License list saved to {output_file}")


# Node.js template directories
node_dirs = [
    "vefaas-native-nodejs20-default",
    "vefaas-native-nodejs20-mcp-server-echo",
    "vefaas-native-nodejs20-nestjs-default",
    "vefaas-native-nodejs20-nextjs-chatbot",
    "vefaas-native-nodejs20-nextjs",
    "vefaas-native-nodejs20-react-default",
    "vefaas-native-nodejs20-vitepress-default",
    "vefaas-native-nodejs20-vue-default",
    "vefaas-nodejs14-default",
    "vefaas-nodejs14-static-server",
    "vefaas-nodejs20-default",
    # "vefaas-nodeprime14-default",
    "vefaas-native-nodejs20-default",
    "vefaas-native-nodejs20-mcp-server-echo",
    "vefaas-native-nodejs20-nestjs-default",
    "vefaas-native-nodejs20-nextjs-chatbot",
    "vefaas-native-nodejs20-nextjs",
    "vefaas-native-nodejs20-react-default",
    "vefaas-native-nodejs20-vitepress-default",
    "vefaas-native-nodejs20-vue-default",
    "vefaas-nodejs14-default",
    "vefaas-nodejs14-static-server",
    "vefaas-nodejs20-default",
    # "vefaas-nodeprime14-default",
]

all_node_licenses = {}
distinct_node_licenses = set()

for dir_path in node_dirs:
    print(f"Processing {dir_path} ...")
    dir_abs = os.path.abspath(dir_path)

    package_json = os.path.join(dir_abs, "package.json")
    if not os.path.exists(package_json):
        print(f"  Warning: package.json not found in {dir_path}. Skipping.")
        all_node_licenses[dir_path] = []
        continue

    try:
        # Run license-checker --json in the directory
        result = subprocess.run(
            ["license-checker", "--json"],
            cwd=dir_abs,
            capture_output=True,
            text=True,
            check=True,
        )

        licenses_data = json.loads(result.stdout)
        licenses_json = []

        for dep, info in licenses_data.items():
            license_type = info.get("licenses", "Unknown")
            licenses_json.append({"Module": dep, "License": license_type})
            if license_type != "Unknown":
                distinct_node_licenses.add(license_type)

        all_node_licenses[dir_path] = licenses_json

    except subprocess.CalledProcessError as e:
        print(f"  Error running license-checker for {dir_path}: {e}")
        all_node_licenses[dir_path] = []
    except json.JSONDecodeError:
        print(f"  Error parsing JSON for {dir_path}")
        all_node_licenses[dir_path] = []

# Create final output
final_output = {
    "directories": all_node_licenses,
    "distinct_licenses": sorted(list(distinct_node_licenses)),
}

# Write aggregated results
output_file = "all_node_licenses.json"
with open(output_file, "w") as f:
    json.dump(final_output, f, indent=2)

print(f"Done! Aggregated Node.js license data saved to {output_file}")
