#!/usr/bin/env python3
"""Validate Mermaid user flows written for the mermaid-userflow skill.

Usage:
    python3 scripts/validate.py FILE [FILE ...]
    python3 scripts/validate.py -            (read one flow from stdin)

A .md file is checked block by block: every fenced block labelled mermaid.
A block whose node IDs all start with lg is a legend. Every flow in a .md
file needs a legend: right after it, or one shared legend before all flows.
Any other file, or stdin, is treated as one flow and needs no legend.
Exits 1 if any block has an error, 0 otherwise. Warnings never fail.
"""

import re
import sys

# Shapes table from SKILL.md, in table order.
# (name, used for, prefixes, Mermaid shape)
TABLE = [
    ("Terminator", "start or end", ("start", "exit"), "stadium"),
    ("Display", "screen or page", ("scr",), "curv-trap"),
    ("Process", "step or action", ("act",), "rect"),
    ("Decision", "yes or no question", ("dec",), "diam"),
    ("Manual Input", "user enters data", ("in",), "sl-rect"),
    ("Manual Operation", "user acts outside the app", ("man",), "trap-t"),
    ("Predefined Process", "subflow or other flow", ("sub",), "fr-rect"),
    ("Preparation", "setup before a step", ("prep",), "hex"),
    ("Delay", "waiting", ("wait",), "delay"),
    ("Data (I/O)", "data in or out", ("io",), "lean-r"),
    ("Database", "saved records", ("db",), "cyl"),
    ("Stored Data", "any stored data", ("store",), "bow-rect"),
    ("Internal Storage", "session or cache", ("mem",), "win-pane"),
    ("Direct Access Storage", "files on the device", ("disk",), "h-cyl"),
    ("Document", "email, receipt or file", ("doc",), "doc"),
    ("Multiple Documents", "several documents", ("mdoc",), "docs"),
    ("Paper Tape", "physical item", ("tape",), "flag"),
    ("Merge", "two paths rejoin", ("merge",), "flip-tri"),
    ("Summing Junction", "three or more paths rejoin", ("sum",), "cross-circ"),
    ("Connector", "jump within the flow", ("con",), "circle"),
    ("Curly Brace Note", "comment on a node", ("note",), "brace"),
]

# Node type prefix -> Mermaid shape.
SHAPES = {p: shape for _, _, prefixes, shape in TABLE for p in prefixes}
# Node type prefix -> symbol name.
NAME_OF = {p: name for name, _, prefixes, _ in TABLE for p in prefixes}


def legend_id(name):
    return "lg" + re.sub(r"[^A-Za-z]", "", name)


def expected_legend(names):
    """Ordered legend nodes for a set of symbol names: list of (id, shape, label)."""
    nodes = []
    for name, used, _, shape in TABLE:
        if name not in names:
            continue
        lid = legend_id(name)
        if name == "Summing Junction":
            # Mermaid draws no text in a crossed circle, so a text node carries the label.
            nodes.append((lid, shape, " "))
            nodes.append((lid + "Text", "text", f"{name}: {used}"))
        else:
            nodes.append((lid, shape, f"{name}: {used}"))
    return nodes

BLANK_LABEL = {"merge", "sum"}      # label is a single space
END_TYPES = {"exit", "sub", "con"}  # allowed to have no outgoing arrow
MAX_NODE_WORDS = 6
MAX_NOTE_LINES = 3
MAX_EDGE_WORDS = 4

HEADER_RE = re.compile(r"^flowchart (TD|LR)$")
ID = r"[a-z]+[A-Z][A-Za-z0-9]*"
NODE_RE = re.compile(
    r'^(?P<id>' + ID + r')@\{ shape: (?P<shape>[a-z-]+), label: "(?P<label>[^"]*)" \}$'
)
EDGE_RE = re.compile(
    r'^(?P<a>' + ID + r') (?P<arrow>-->|-\.-)'
    r'(?:\|(?P<label>"[^"|]+"|[^"|]+)\|)? (?P<b>' + ID + r')$'
)
LOOSE_ID_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*")
FORBIDDEN_LABEL_CHARS = set('"<>#|`')
PLAIN_EDGE_LABEL_RE = re.compile(r"^[A-Za-z0-9 ]+$")


def prefix_of(node_id):
    return re.match(r"^[a-z]+", node_id).group(0)


def check_flow(lines, start_line):
    """lines: block content. start_line: file line number of lines[0].
    Returns (errors, warnings) as lists of (line_no, message)."""
    errors, warnings = [], []
    nodes = {}          # id -> (line_no, prefix, label)
    edges = []          # (line_no, a, arrow, label, b)
    seen_edge = False

    content = [(start_line + i, l.rstrip()) for i, l in enumerate(lines)]
    content = [(n, l) for n, l in content if l.strip()]
    if not content:
        return [(start_line, "empty block")], warnings

    n0, first = content[0]
    if not HEADER_RE.match(first.strip()):
        errors.append((n0, "first line must be 'flowchart TD' or 'flowchart LR'"))

    for n, raw in content[1:]:
        line = raw.strip()
        m = NODE_RE.match(line)
        if m:
            nid, shape, label = m.group("id"), m.group("shape"), m.group("label")
            p = prefix_of(nid)
            if seen_edge:
                errors.append((n, f"node '{nid}' defined after the first edge; define all nodes first"))
            if nid in nodes:
                errors.append((n, f"node '{nid}' defined twice"))
            if p not in SHAPES:
                errors.append((n, f"'{nid}' has unknown prefix '{p}'"))
            elif SHAPES[p] != shape:
                errors.append((n, f"'{nid}' is a '{p}' node and must use shape {SHAPES[p]}, not {shape}"))
            if p in BLANK_LABEL:
                if label != " ":
                    errors.append((n, f"'{nid}' must have label \" \" (one space)"))
            else:
                if not label.strip():
                    errors.append((n, f"'{nid}' needs a label"))
                # Only notes may break lines, with <br>.
                lines = label.split("<br>") if p == "note" else [label]
                if p == "note" and len(lines) > MAX_NOTE_LINES:
                    errors.append((n, f"note '{nid}' has over {MAX_NOTE_LINES} lines"))
                if p == "note" and any(not x.strip() for x in lines):
                    errors.append((n, f"note '{nid}' has an empty line"))
                bad = FORBIDDEN_LABEL_CHARS & set("".join(lines))
                if bad:
                    errors.append((n, f"'{nid}' label contains {''.join(sorted(bad))}"
                                      + (" (only notes may use <br>)" if "<br>" in label else "")))
                if p == "con" and len(label) > 2:
                    errors.append((n, f"connector '{nid}' label must be 1 or 2 characters"))
                if any(len(x.split()) > MAX_NODE_WORDS for x in lines):
                    warnings.append((n, f"'{nid}' label is over {MAX_NODE_WORDS} words"
                                        + (" on a line" if p == "note" else "")))
            nodes[nid] = (n, p, label)
            continue

        m = EDGE_RE.match(line)
        if m:
            seen_edge = True
            label = m.group("label")
            if label is not None:
                if label.startswith('"'):
                    inner = label[1:-1]
                    bad = FORBIDDEN_LABEL_CHARS & set(inner)
                    if bad:
                        errors.append((n, f"edge label contains {''.join(sorted(bad))}"))
                else:
                    inner = label
                    if not PLAIN_EDGE_LABEL_RE.match(label):
                        errors.append((n, "edge label with punctuation must be quoted: -->|\"No, retry\"|"))
                if not inner.strip():
                    errors.append((n, "empty edge label"))
                if len(inner.split()) > MAX_EDGE_WORDS:
                    warnings.append((n, f"edge label is over {MAX_EDGE_WORDS} words"))
            edges.append((n, m.group("a"), m.group("arrow"), label, m.group("b")))
            continue

        # Not a node, not an edge. Explain the most likely cause.
        if re.match(r"^(subgraph|end|classDef|class|style|linkStyle|click|direction)\b", line) \
                or line.startswith("%%") or ":::" in line:
            errors.append((n, f"not allowed in this skill: '{line}'"))
        elif re.search(r"--\s+\S.*-->|==>|-\.->|--[ox]\b|<-->|---", line):
            errors.append((n, f"use only 'A --> B', 'A -->|Label| B' or 'noteX -.- B': '{line}'"))
        elif re.search(r"(-->|-\.-).*(-->|-\.-)", line):
            errors.append((n, f"one edge per line, no chains: '{line}'"))
        elif "@{" not in line and re.match(r"^[A-Za-z_]\w*\s*[\[\(\{>]", line):
            errors.append((n, f"use the shape syntax id@{{ shape: x, label: \"...\" }}, not brackets: '{line}'"))
        elif "@{" in line:
            mid = LOOSE_ID_RE.match(line)
            hint = ""
            if mid and not re.match("^" + ID + "$", mid.group(0)):
                hint = " (ID must be a lowercase prefix plus PascalCase name, like scrLogin)"
            errors.append((n, f"malformed node definition{hint}: '{line}'"))
        else:
            mid = LOOSE_ID_RE.match(line)
            if mid and not re.match("^" + ID + "$", mid.group(0)):
                errors.append((n, f"bad ID '{mid.group(0)}': use a lowercase prefix plus PascalCase name, like scrLogin"))
            else:
                errors.append((n, f"unrecognised line: '{line}'"))

    # Graph checks.
    out_arrows = {k: 0 for k in nodes}
    in_arrows = {k: 0 for k in nodes}
    linked = set()
    labelled = {k: [] for k in nodes}
    for n, a, arrow, label, b in edges:
        for x in (a, b):
            if x not in nodes:
                errors.append((n, f"'{x}' is used in an edge but never defined with a shape"))
        if a not in nodes or b not in nodes:
            continue
        linked.update((a, b))
        pa, pb = nodes[a][1], nodes[b][1]
        if arrow == "-.-":
            if (pa == "note") == (pb == "note"):
                errors.append((n, "'-.-' links a note to one other node"))
            if label is not None:
                errors.append((n, "note links take no label"))
            continue
        if "note" in (pa, pb):
            errors.append((n, "notes attach with 'noteX -.- nodeY', not an arrow"))
            continue
        out_arrows[a] += 1
        in_arrows[b] += 1
        labelled[a].append(label is not None)

    for nid, (n, p, label) in nodes.items():
        if nid not in linked:
            errors.append((n, f"orphan node '{nid}': not connected to anything"))
            continue
        if p == "note":
            continue
        if p == "start" and in_arrows[nid]:
            errors.append((n, f"start node '{nid}' has incoming arrows"))
        if p == "exit" and out_arrows[nid]:
            errors.append((n, f"exit node '{nid}' has outgoing arrows"))
        if p not in END_TYPES and not out_arrows[nid]:
            errors.append((n, f"dead end at '{nid}': end every path with an exit, sub or con node"))
        if p == "dec":
            if out_arrows[nid] < 2:
                errors.append((n, f"decision '{nid}' needs at least 2 outgoing arrows"))
            if not all(labelled[nid]):
                errors.append((n, f"every arrow out of decision '{nid}' needs a label"))

    if nodes and not any(p == "start" for _, p, _ in nodes.values()):
        errors.append((n0, "flow needs at least one start node"))

    cons = {}
    for nid, (n, p, label) in nodes.items():
        if p == "con":
            cons.setdefault(label, []).append(nid)
    for label, ids in cons.items():
        if len(ids) != 2:
            errors.append((nodes[ids[0]][0], f"connector '{label}' must appear on exactly 2 con nodes, found {len(ids)}"))
        else:
            a, b = ids
            ok = (in_arrows[a] and not out_arrows[a] and out_arrows[b] and not in_arrows[b]) or \
                 (in_arrows[b] and not out_arrows[b] and out_arrows[a] and not in_arrows[a])
            if not ok:
                errors.append((nodes[a][0], f"connector pair '{label}': one node takes arrows in, the other sends them out"))

    return errors, warnings


LEGEND_NODE_RE = re.compile(
    r'^(?P<id>lg[A-Za-z]+)@\{ shape: (?P<shape>[a-z-]+), label: "(?P<label>[^"]*)" \}$'
)
LEGEND_EDGE_RE = re.compile(r"^(?P<a>lg[A-Za-z]+) ~~~ (?P<b>lg[A-Za-z]+)$")
LEGEND_COLUMNS = 3


def is_legend(lines):
    """A legend block is one whose first node line has an lg ID."""
    for line in lines[1:]:
        line = line.strip()
        if line:
            return line.startswith("lg")
    return False


def flow_names(lines):
    """Symbol names used by a flow, from its node lines."""
    names = set()
    for line in lines:
        m = NODE_RE.match(line.strip())
        if m:
            p = prefix_of(m.group("id"))
            if p in NAME_OF:
                names.add(NAME_OF[p])
    return names


def check_legend(lines, start_line):
    """Returns (errors, names listed)."""
    errors = []
    content = [(start_line + i, l.strip()) for i, l in enumerate(lines)]
    content = [(n, l) for n, l in content if l]
    n0 = content[0][0]
    if content[0][1] != "flowchart TD":
        errors.append((n0, "a legend starts with 'flowchart TD'"))
    nodes, edges = [], set()
    by_label = {f"{name}: {used}": name for name, used, _, _ in TABLE}
    names = set()
    for n, line in content[1:]:
        m = LEGEND_NODE_RE.match(line)
        if m:
            nodes.append((n, m.group("id"), m.group("shape"), m.group("label")))
            if m.group("label") in by_label:
                names.add(by_label[m.group("label")])
            elif m.group("label") != " ":
                errors.append((n, f"legend label must be 'Name: used for' exactly as in the Shapes table, got '{m.group('label')}'"))
            continue
        m = LEGEND_EDGE_RE.match(line)
        if m:
            edges.add((m.group("a"), m.group("b")))
            continue
        errors.append((n, f"a legend holds only lg nodes and 'lgA ~~~ lgB' links: '{line}'"))
    want = expected_legend(names)
    got = [(i, s, l) for _, i, s, l in nodes]
    if got != want:
        errors.append((n0, "legend nodes must be, in this order: " +
                       "; ".join(f'{i}@{{ shape: {s}, label: "{l}" }}' for i, s, l in want)))
    ids = [i for i, _, _ in want]
    want_edges = {(ids[k], ids[k + LEGEND_COLUMNS]) for k in range(len(ids) - LEGEND_COLUMNS)}
    if edges != want_edges:
        errors.append((n0, f"legend links must make a {LEGEND_COLUMNS} column grid: " +
                       ", ".join(f"{a} ~~~ {b}" for a, b in sorted(want_edges, key=lambda e: ids.index(e[0])))
                       if want_edges else f"legend with {len(ids)} nodes takes no links"))
    return errors, names


def blocks_from_markdown(text):
    """Yield (start_line, lines) for every ```mermaid block."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == "```mermaid":
            start = i + 2
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                body.append(lines[i])
                i += 1
            yield start, body
        i += 1


def check_numbered_headings(text, legend_lines):
    """If a file uses numbered ## flow headings, they must run 1, 2, 3 and
    each hold exactly one flow block. The shared legend sits above them."""
    errors = []
    lines = text.splitlines()
    heads = [(i + 1, l) for i, l in enumerate(lines) if l.startswith("## ")]
    numbered = [(n, l) for n, l in heads if re.match(r"^## \d+\. \S", l)]
    if not numbered:
        return errors
    if len(numbered) != len(heads):
        return [(heads[0][0], "mix of numbered and unnumbered ## headings")]
    for k, (n, l) in enumerate(numbered, 1):
        num = int(re.match(r"^## (\d+)\.", l).group(1))
        if num != k:
            errors.append((n, f"flow heading should be number {k}, found {num}"))
        end = numbered[k][0] - 1 if k < len(numbered) else len(lines)
        opens = [j + 1 for j in range(n, end) if lines[j].strip() == "```mermaid"]
        flows = [j for j in opens if j + 1 not in legend_lines]
        if len(flows) != 1:
            errors.append((n, f"flow section has {len(flows)} flow blocks, needs exactly 1"))
        if len(flows) != len(opens):
            errors.append((n, "in a saved file the legend sits once under the # title, not inside a flow section"))
    first = numbered[0][0]
    if not any(start < first for start in legend_lines):
        errors.append((first, "a saved file needs one shared legend under the # title, before ## 1"))
    return errors


def check_coverage(blocks):
    """blocks: list of (start, kind, names). Every flow needs a legend that
    lists exactly the shapes it uses. Either each flow is followed by its own
    legend, or one legend comes first and covers every flow after it."""
    errors = []
    flows = [b for b in blocks if b[1] == "flow"]
    legends = [b for b in blocks if b[1] == "legend"]
    if not flows:
        return errors
    if blocks[0][1] == "legend" and len(legends) == 1:
        used = set().union(*(f[2] for f in flows))
        listed = legends[0][2]
        if used != listed:
            errors.append((legends[0][0], _diff("shared legend", used, listed)))
        return errors
    for k, (start, kind, names) in enumerate(blocks):
        if kind != "flow":
            continue
        nxt = blocks[k + 1] if k + 1 < len(blocks) else None
        if not nxt or nxt[1] != "legend":
            errors.append((start, "flow needs a legend block right after it, or one shared legend before all flows"))
        elif nxt[2] != names:
            errors.append((nxt[0], _diff("legend", names, nxt[2])))
    return errors


def _diff(what, used, listed):
    parts = []
    if used - listed:
        parts.append("missing " + ", ".join(sorted(used - listed)))
    if listed - used:
        parts.append("lists unused " + ", ".join(sorted(listed - used)))
    return f"{what} must list exactly the shapes used: " + "; ".join(parts)


def report(name, errors, warnings=()):
    for n, msg in sorted(errors):
        print(f"{name}:{n}: error: {msg}")
    for n, msg in sorted(warnings):
        print(f"{name}:{n}: warning: {msg}")
    return bool(errors)


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
    failed = False
    total = 0
    for path in argv[1:]:
        if path == "-":
            text, name = sys.stdin.read(), "<stdin>"
        else:
            with open(path, encoding="utf-8") as f:
                text, name = f.read(), path
        if not name.endswith(".md"):
            total += 1
            failed |= report(name, *check_flow(text.splitlines(), 1))
            continue
        blocks = list(blocks_from_markdown(text))
        if not blocks:
            print(f"{name}: no mermaid blocks found")
        kinds = []
        for start, body in blocks:
            total += 1
            if is_legend(body):
                errors, names = check_legend(body, start)
                failed |= report(name, errors)
                kinds.append((start, "legend", names))
            else:
                failed |= report(name, *check_flow(body, start))
                kinds.append((start, "flow", flow_names(body)))
        legend_lines = {start for start, kind, _ in kinds if kind == "legend"}
        failed |= report(name, check_numbered_headings(text, legend_lines))
        failed |= report(name, check_coverage(kinds))
    print(f"{total} block(s) checked: {'FAIL' if failed else 'OK'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
