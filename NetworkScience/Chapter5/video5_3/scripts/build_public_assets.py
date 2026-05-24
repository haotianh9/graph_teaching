from pathlib import Path

from make_cover import make_cover
from public_metadata import COVER_OUTPUTS, REFERENCES, SHORT_DESCRIPTION, SUGGESTED_TITLE


def write_video_description(base_dir: Path) -> Path:
    references = "\n\n".join(f"{label}:\n{url}" for label, url in REFERENCES)
    text = f"""# Video 5.3 Description

## Suggested Title

{SUGGESTED_TITLE}

## Short Description

{SHORT_DESCRIPTION}

## References

{references}
"""
    output = base_dir / "video_description.md"
    output.write_text(text, encoding="utf-8")
    return output


def main():
    base_dir = Path(__file__).resolve().parents[1]
    generated = []
    for spec in COVER_OUTPUTS:
        make_cover(spec["width"], spec["height"], spec["filename"])
        generated.append(base_dir / "assets" / "cover" / spec["filename"])
    generated.append(write_video_description(base_dir))

    print("public assets generated:")
    for path in generated:
        print(path)


if __name__ == "__main__":
    main()
