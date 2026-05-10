from langchain.tools import tool


VALID_STARTS = {
    "flowchart": ["graph ", "flowchart "],
    "sequence": ["sequenceDiagram"],
    "class": ["classDiagram"],
    "state": ["stateDiagram", "stateDiagram-v2"],
    "gantt": ["gantt"],
    "er": ["erDiagram"],
    "pie": ["pie"],
    "mindmap": ["mindmap"],
}


@tool
def generate_mermaid_diagram(diagram_type: str, mermaid_code: str) -> str:
    """
    Validate and format a Mermaid diagram.

    Always use the mermaid-diagrams skill to write the code before calling this tool.

    Args:
        diagram_type: Type of diagram - one of: flowchart, sequence, class,
                      state, gantt, er, pie, mindmap
        mermaid_code: The raw Mermaid diagram code (without markdown fences)

    Returns:
        Formatted Mermaid code wrapped in markdown fences for rendering,
        or an error message with fix instructions.
    """
    code = mermaid_code.strip()
    lines = [l.rstrip() for l in code.split("\n") if l.strip()]
    
    if not lines:
        return "Error: Diagram code is empty."
    
    first_line = lines[0].strip().lower()
    
    # Validate diagram type declaration
    valid_prefixes = VALID_STARTS.get(diagram_type, [])
    if not any(first_line.startswith(p.lower()) for p in valid_prefixes):
        expected = ", ".join(valid_prefixes) if valid_prefixes else "unknown type"
        return (
            f"Error: Invalid {diagram_type} diagram declaration. "
            f"First line must start with: {expected}"
        )
    
    # Check for common syntax issues
    issues = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Unbalanced brackets in node definitions
        if "[" in stripped and stripped.count("[") != stripped.count("]"):
            issues.append(f"Line {i}: Unbalanced square brackets")
        
        # Unbalanced parentheses
        if "(" in stripped and stripped.count("(") != stripped.count(")"):
            issues.append(f"Line {i}: Unbalanced parentheses")
        
        # Arrow syntax mismatch
        if diagram_type != "sequence" and "->>" in stripped:
            issues.append(f"Line {i}: Sequence arrow '->>' used in {diagram_type}")
        
        # Missing end for subgraph/state blocks
        if any(
            stripped.startswith(kw)
            for kw in ["subgraph", "state ", "loop ", "alt ", "opt "]
        ):
            # Simple heuristic - can't fully parse without a real parser
            pass
    
    if issues:
        return (
            "Validation issues found:\n"
            + "\n".join(f"- {issue}" for issue in issues)
            + "\n\nPlease fix the code using the mermaid-diagrams skill and retry."
        )
    
    # Return formatted code ready for Mermaid viewer
    return f"```mermaid\n{code}\n```"