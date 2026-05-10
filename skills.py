from typing import TypedDict


class Skill(TypedDict):
    name: str
    description: str
    content: str


SKILLS: list[Skill] = [
    {
        "name": "mermaid-diagrams",
        "description": (
            "Create Mermaid diagrams including flowcharts, sequence diagrams, "
            "class diagrams, state diagrams, and more. Use when the user wants "
            "to visualize a process, system, or relationship."
        ),
        "content": """
# Mermaid Diagrams Skill

Create valid Mermaid diagram code that can be rendered in any Mermaid viewer.

## Flowcharts

- Direction: `graph TD` (top-down), `graph LR` (left-right), `graph RL`, `graph BT`
- Nodes:
  - Rectangle: `A[Label]`
  - Rounded: `A(Label)` or `A([Label])`
  - Circle: `A((Label))`
  - Diamond: `A{Label}`
  - Subroutine: `A[[Label]]`
- Arrows:
  - Solid: `A --> B`
  - Dashed: `A -.-> B`
  - Thick: `A ==> B`
  - With text: `A -->|text| B`
- Subgraphs:
  ```
  subgraph Title
      A --> B
  end
  ```

## Sequence Diagrams

- Start with: `sequenceDiagram`
- Participants: `participant A as Alice` or `actor A as Alice`
- Arrows:
  - Solid: `A->>B: Message`
  - Dashed: `A-->>B: Message`
  - Solid cross: `A-xB: Message`
  - Async: `A-)B: Message`
- Blocks:
  - `loop condition ... end`
  - `alt condition ... else ... end`
  - `opt condition ... end`
  - `par ... and ... end`
  - `rect rgb(0,0,0) ... end` for color boxes
- Notes: `Note over A,B: text`, `Note left of A: text`

## Class Diagrams

- Start with: `classDiagram`
- Class definition: `class ClassName { +attribute -method() }`
- Relations:
  - Inheritance: `ClassA <|-- ClassB`
  - Composition: `ClassA *-- ClassB`
  - Aggregation: `ClassA o-- ClassB`
  - Association: `ClassA --> ClassB`
  - Dependency: `ClassA ..> ClassB`
- Labels: `ClassA --> ClassB : label`

## State Diagrams

- Start with: `stateDiagram-v2`
- States: `[*] --> State1`, `State1 --> State2 : event`
- Composite states:
  ```
  state Composite {
      [*] --> SubState1
  }
  ```

## General Rules

- Indent with 4 spaces inside blocks
- Node IDs cannot contain spaces unless quoted: `A["My Label"]`
- Colons `:` separate arrows from labels
- Comments: `%% this is a comment`
- Never wrap the entire code in markdown fences - output raw Mermaid syntax only
""",
    },
]
