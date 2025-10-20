import os

HEADER_LINES = [
    "Copyright (c) 2024 Bytedance Ltd. and/or its affiliates",
    "",
    'Licensed under the Apache License, Version 2.0 (the "License");',
    "you may not use this file except in compliance with the License.",
    "You may obtain a copy of the License at",
    "",
    "    http://www.apache.org/licenses/LICENSE-2.0",
    "",
    "Unless required by applicable law or agreed to in writing, software",
    'distributed under the License is distributed on an "AS IS" BASIS,',
    "WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.",
    "See the License for the specific language governing permissions and",
    "limitations under the License.",
]

COMMENT_STYLES = {
    "//": {".c", ".cpp", ".h", ".hpp", ".js", ".ts", ".go", ".java", ".rs", ".swift"},
    "#": {".py", ".sh", ".rb", ".yml", ".yaml", ".toml", ".ini"},
    "html": {".html", ".xml"},
    "css": {".css"},
}

SKIP_DIRS = {"node_modules", "site-packages", "venv", ".git", "__pycache__"}


def get_comment_style(ext):
    for style, exts in COMMENT_STYLES.items():
        if ext in exts:
            return style
    return None


def make_header(style):
    if style == "//":
        return "\n".join(f"// {line}" for line in HEADER_LINES) + "\n\n"
    elif style == "#":
        return "\n".join(f"# {line}" for line in HEADER_LINES) + "\n\n"
    elif style == "html":
        return "<!--\n" + "\n".join(HEADER_LINES) + "\n-->\n\n"
    elif style == "css":
        return "/*\n" + "\n".join(HEADER_LINES) + "\n*/\n\n"
    return None


def should_skip(file_path):
    parts = set(file_path.split(os.sep))
    return any(d in SKIP_DIRS for d in parts)


def file_already_tagged(content):
    return "Bytedance Ltd." in content or "Apache License" in content


def add_header_to_file(file_path):
    ext = os.path.splitext(file_path)[1]
    style = get_comment_style(ext)
    if not style:
        return

    if os.path.getsize(file_path) > 1_000_000:  # skip big files
        return

    with open(file_path, "r+", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        if file_already_tagged(content):
            return
        header = make_header(style)
        f.seek(0, 0)
        f.write(header + content)


def add_headers_to_repo(root_dir="."):
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for filename in files:
            add_header_to_file(os.path.join(root, filename))


if __name__ == "__main__":
    add_headers_to_repo(".")
    print("✅ License headers added to source files.")
