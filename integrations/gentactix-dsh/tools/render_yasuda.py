"""Render 安田讲堂攻防战 teaching records into the existing catalog and CSVs.

    python tools/render_yasuda.py
    python tools/render_yasuda.py --check

No network, model, live state, or AGENTS.md access. Historical data are references,
not scheduled mutations of simulation state. Edit data/yasuda/*.json first.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.render_long_march import render as render_series

DATA = ROOT / "data/yasuda"


def render():
    return render_series(
        DATA, "yasuda_anchors.json", "安田讲堂攻防战", "战后日本・全共斗期（1968—1969）",
        "render_yasuda.py",
        "街垒修补、催泪弹与放水、逐层争夺、跨区抽兵及各派互不增援")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for path, text in render().items():
        if args.check:
            if not path.exists() or path.read_bytes() != text.encode("utf-8"):
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.encode("utf-8"))
    if stale:
        print("Out of date:\n" + "\n".join(stale))
        return 1
    print("Yasuda documents checked" if args.check else "Yasuda documents rendered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
