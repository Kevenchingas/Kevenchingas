from pathlib import Path
from urllib.request import urlopen
import xml.etree.ElementTree as ET

url = "https://ghchart.rshah.org/39d353/Kevenchingas"
with urlopen(url, timeout=60) as response:
    root = ET.fromstring(response.read())
ns = "{http://www.w3.org/2000/svg}"
cells = [cell for cell in root.iter(ns + "rect") if "data-score" in cell.attrib]
if len(cells) < 300:
    raise ValueError("Incomplete calendar; preserving existing image")
for cell in cells:
    score = int(cell.attrib["data-score"])
    color = "#21262d" if score == 0 else ("#0e4429" if score == 1 else "#006d32" if score <= 3 else "#26a641" if score <= 6 else "#39d353")
    cell.set("style", "fill:" + color + ";shape-rendering:crispEdges")
    cell.set("rx", "2")
for label in root.iter(ns + "text"):
    label.set("style", label.get("style", "").replace("#767676", "#8b949e"))
root.set("viewBox", "0 0 663 104")
ET.register_namespace("", "http://www.w3.org/2000/svg")
Path("assets/contributions.svg").write_text(ET.tostring(root, encoding="unicode"), encoding="utf-8")
