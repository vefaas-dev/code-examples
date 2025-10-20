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

#!/bin/bash
set -Eeuo pipefail

cd "$(dirname "$0")"

# Get the list of directories that have changes
changed_dirs=$(git diff --name-only HEAD | awk -F'/' '{print $1}' | sort -u)
echo "Changes directory: $changed_dirs"

# Loop through each directory
for d in $changed_dirs ; do
    dir_name=${d%/} # Remove trailing '/'

    # Skip the 'zip' folder and unchanged directories
    if [[ ! -d "$dir_name" ]] || [[ "$dir_name" == "zip" ]]; then
        continue
    fi

    echo "Processing directory: $dir_name"

    # Build
    if [[ -f "./$dir_name/build.sh" ]]; then
        bash "./$dir_name/build.sh"
        cd "$(dirname "$0")"
    fi

    # Zip
    cd "$dir_name"
    rm -f "../zip/$dir_name.zip"
    zip -r "../zip/$dir_name.zip" . -x '*.zip' '*.zip/*' '.venv/*' '*/.venv/*'
    cd ..
done
