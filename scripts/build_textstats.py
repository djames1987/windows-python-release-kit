"""Separate worked example using the same deterministic archive helper."""
from build import archive, ROOT, DIST


def build_textstats():
    DIST.mkdir(exist_ok=True)
    source = ROOT / "adaptations/textstats"
    output = DIST / "textstats.pyz"
    archive(output, {name: (source / name).read_bytes() for name in ("__main__.py", "textstats.py")})
    print(output)
    return output


if __name__ == "__main__":
    build_textstats()
