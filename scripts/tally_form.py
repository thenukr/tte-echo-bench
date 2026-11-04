"""Parse a Tally form ledger (from the Tally MCP load_form tool) into a structured question list."""
import html
import re

UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
OPTION_TYPES = {"DROPDOWN_OPTION": "dropdown", "MULTIPLE_CHOICE_OPTION": "multiple_choice", "CHECKBOX": "checkboxes"}


def _rows(ledger: str):
    blocks = ledger.split("\n## Logic rules")[0]
    for line in blocks.split("\n"):
        if line.startswith("| ") and line.count("|") >= 9:
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if c[0] in ("#", "-"):
                continue
            yield {"text": html.unescape(c[1]), "block": c[2], "type": c[3], "q": c[4], "props": c[7]}


def parse_questions(ledger: str):
    """Return questions in form order with section/subsection, type, options, hidden flag, help text."""
    questions, by_q = [], {}
    section = subsection = None
    for r in _rows(ledger):
        t = r["type"]
        if t == "HEADING_1":
            section, subsection = r["text"], None
        elif t == "HEADING_2":
            subsection = r["text"]
        elif t == "TITLE":
            q = {"uuid": r["q"], "title": r["text"].strip(), "section": section, "subsection": subsection,
                 "kind": None, "options": [], "option_uuids": [], "hidden": "isHidden=true" in r["props"],
                 "help": None, "allow_multiple": False, "optional": False}
            questions.append(q)
            by_q[r["q"]] = q
        elif t == "TEXT" and r["q"] in by_q:
            by_q[r["q"]]["help"] = r["text"].strip()
            if r["text"].strip().lower().startswith("optional"):
                by_q[r["q"]]["optional"] = True
        elif t in OPTION_TYPES and r["q"] in by_q:
            q = by_q[r["q"]]
            q["kind"] = OPTION_TYPES[t]
            q["options"].append(r["text"].strip())
            q["option_uuids"].append(r["block"])
            if "allowMultiple=true" in r["props"]:
                q["allow_multiple"] = True
            if "isRequired=false" in r["props"]:
                q["optional"] = True
        elif t.startswith("INPUT") and r["q"] in by_q:
            by_q[r["q"]]["kind"] = "email" if t == "INPUT_EMAIL" else "text"
            if "isRequired=false" in r["props"]:
                by_q[r["q"]]["optional"] = True
    return questions


def parse_logic(ledger: str):
    """Return SHOW rules as [{"when": [(q_uuid, op, [option_uuid...])], "join": "AND"|"OR", "show": [q_uuid...]}]."""
    section = ledger.split("\n## Logic rules", 1)[1].split("\n--")[0]
    rules = []
    for line in section.split("\n"):
        if not line.startswith("| ") or line.startswith("| logicRule") or line.startswith("| -"):
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        when, then = c[2], c[3]
        join = "OR" if " OR " in when else "AND"
        conds = []
        for part in re.split(r" OR | AND ", when):
            m = re.match(rf"({UUID}) (IS ANY OF|IS|CONTAINS) \(?(.*?)\)?$", part.strip())
            if not m:
                raise ValueError(f"unparsed condition: {part}")
            conds.append((m.group(1), m.group(2), re.findall(UUID, m.group(3))))
        if not then.startswith("SHOW "):
            raise ValueError(f"unexpected action: {then}")
        rules.append({"when": conds, "join": join, "show": re.findall(UUID, then)})
    return rules
