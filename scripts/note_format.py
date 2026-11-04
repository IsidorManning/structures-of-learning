"""Remove obsolete publication banners and isolate generated index content."""
import re

LEGACY_NOTICE = "<!-- Generated from the Obsidian source on main. Do not edit this branch directly. -->"
START = "<!-- literature-index:start -->"
END = "<!-- literature-index:end -->"


def clean_markdown(text: str, *, strip_index: bool = False) -> str:
    text = re.sub(r"(?m)^" + re.escape(LEGACY_NOTICE) + r"\r?\n(?:\r?\n)?", "", text)
    if strip_index and (START in text or END in text):
        if text.count(START) != 1 or text.count(END) != 1 or text.index(START) > text.index(END):
            raise ValueError("invalid literature index markers")
        before, after = text.split(START, 1)
        _, after = after.split(END, 1)
        text = before.rstrip() + "\n" + after.lstrip("\n")
    # A generated trailing region must not turn blank-line differences into edits.
    if strip_index:
        return text.rstrip() + "\n"
    return text if not text or text.endswith("\n") else text + "\n"

