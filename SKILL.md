---
name: mermaid-userflow
description: Draws user flows as Mermaid flowcharts with standard flowchart symbols. Use when someone asks for a user flow, task flow, screen flow, flow diagram of how a user moves through a product (login, signup, onboarding, checkout, password reset), or the happy path and error branches of a feature. Every node uses a fixed shape for its type, and a legend lists the shapes used. Not for sequence diagrams, user journey maps, architecture diagrams, ERDs or wireframes.
---

# Mermaid User Flow

Draw user flows as Mermaid flowcharts. Every node uses the shape defined for its type, taken from the standard flowchart symbols. A legend lists the shapes the flow uses, and every block is validated before output.

This skill is plain markdown plus one optional Python script. It works in any agent that can read files.

## Hard rules

1. Start every flow with `flowchart TD`. Use `flowchart LR` only when the user asks for left to right.
2. Define every node on its own line with the shape syntax: `id@{ shape: x, label: "Text" }`. Never use bracket shapes like `A[Text]`, never a bare node, never a shape outside the table below.
3. The node ID prefix sets the type, and the type sets the shape. Use the exact pair from the table.
4. Define all nodes first, then all edges. One edge per line, no chains like `a --> b --> c`.
5. Use one arrow, `-->`, and one edge label form, `-->|Label|`. Quote labels that contain punctuation: `-->|"No, retry"|`. The only other link is `noteX -.- nodeY` for notes.
6. No subgraphs, `classDef`, `style`, `class`, `linkStyle`, `click`, `%%` comments or init blocks.
7. Every node connects to something. Every path ends at an exit, sub or connector node. Every arrow out of a decision has a label.
8. Every flow gets a legend that lists only the shapes it uses. See Legend.
9. Before output, validate. See Validation.

Requires Mermaid 11.3 or newer, which GitHub and mermaid.live render. Older renderers fail the whole diagram, because the shape syntax is new.

## Shapes

Every shape comes from the standard flowchart symbol set (ISO 5807, as in the Figma flowchart symbols). Name is the symbol's name. Used for is what it means in a user flow, and doubles as its legend text. Details and examples for each in `references/shapes.md`.

| Name | Used for | Prefix | Mermaid shape |
|---|---|---|---|
| Terminator | start or end | `start`, `exit` | `stadium` |
| Display | screen or page | `scr` | `curv-trap` |
| Process | step or action | `act` | `rect` |
| Decision | yes or no question | `dec` | `diam` |
| Manual Input | user enters data | `in` | `sl-rect` |
| Manual Operation | user acts outside the app | `man` | `trap-t` |
| Predefined Process | subflow or other flow | `sub` | `fr-rect` |
| Preparation | setup before a step | `prep` | `hex` |
| Delay | waiting | `wait` | `delay` |
| Data (I/O) | data in or out | `io` | `lean-r` |
| Database | saved records | `db` | `cyl` |
| Stored Data | any stored data | `store` | `bow-rect` |
| Internal Storage | session or cache | `mem` | `win-pane` |
| Direct Access Storage | files on the device | `disk` | `h-cyl` |
| Document | email, receipt or file | `doc` | `doc` |
| Multiple Documents | several documents | `mdoc` | `docs` |
| Paper Tape | physical item | `tape` | `flag` |
| Merge | two paths rejoin | `merge` | `flip-tri` |
| Summing Junction | three or more paths rejoin | `sum` | `cross-circ` |
| Connector | jump within the flow | `con` | `circle` |
| Curly Brace Note | comment on a node | `note` | `brace` |

Special cases:

- Merge and Summing Junction nodes always have the label `" "` (one space).
- Connectors come in pairs with the same 1 or 2 character label. One takes arrows in, the other sends them out.
- A note links to one node with `noteX -.- nodeY`. Add notes only when the user asks.
- Three Figma symbols have no Mermaid shape: Or, Off-Page Link and the bracket Note. Use Predefined Process to jump to another flow.

Prefer the common types. Most flows need only Terminator, Display, Process, Decision, Manual Input and Predefined Process. Use the others when they say something the common ones can't.

## Naming

- **IDs**: prefix plus a PascalCase name, letters and digits only. `scrLogin`, `decEmailValid`, `inPassword`. Unique within the block.
- **Node labels**: double quoted, 6 words or fewer, sentence case. No `"`, `<`, `>`, `#`, `|` or backticks.
- **Note labels** follow the same rules as any other label. Mermaid wraps and centres them.
- **Screens** are nouns: "Login screen", "Order summary". **Steps** start with a verb: "Taps Sign in", "Sends reset link". **Decisions** end with a question mark: "Email registered?"
- **Edge labels**: 4 words or fewer. Decisions use Yes and No unless the options need names.

## Legend

The legend is its own `mermaid` block. It lists only the shapes its flow uses, each drawn as the real shape with the label `Name: used for`.

```
flowchart TD
  lgTerminator@{ shape: stadium, label: "Terminator: start or end" }
  lgDisplay@{ shape: curv-trap, label: "Display: screen or page" }
  lgDecision@{ shape: diam, label: "Decision: yes or no question" }
  lgManualInput@{ shape: sl-rect, label: "Manual Input: user enters data" }

  lgTerminator ~~~ lgManualInput
```

- Start with `flowchart TD`.
- One node per shape used, in Shapes table order. Start and exit nodes share one Terminator entry.
- ID is `lg` plus the Name with spaces and punctuation removed: `lgManualInput`, `lgDataIO`.
- Label is `Name: used for`, exactly as in the Shapes table.
- Summing Junction takes two nodes, because Mermaid draws no text in a crossed circle: `lgSummingJunction@{ shape: cross-circ, label: " " }`, then `lgSummingJunctionText@{ shape: text, label: "Summing Junction: three or more paths rejoin" }`.
- Lay it out as a 3 column grid: link each node to the node 3 places after it with `~~~`, which draws nothing. With 3 nodes or fewer, no links.
- When an edit adds or removes a shape type, update the legend too.

## Workflow

1. Name the flow and its goal. Find the start (trigger) and the outcomes (exits).
2. Open `references/diagrams.md` and use the closest example as a model.
3. List the happy path first, then the branches: errors, empty states, edge cases.
4. Pick each node's type from the Shapes table, then write all node lines, then all edge lines.
5. Write the legend from the types you used.
6. Validate. Fix. Validate again.
7. Output. See Output format.

## Validation

For every block, before output:

1. A flow starts with `flowchart TD` or `flowchart LR`.
2. Every node line matches `id@{ shape: x, label: "Text" }`, and the shape matches the ID prefix in the Shapes table.
3. Every ID used in an edge is defined above it with a shape.
4. Every edge is `a --> b`, `a -->|Label| b` or `noteX -.- b`. Nothing else.
5. No orphans, no dead ends, at least one start node, every decision has two or more labelled arrows out.
6. The legend lists exactly the shape types used, in table order, with the exact labels and the grid links.

If you can run code, run the script and treat its output as the source of truth:

```
python3 scripts/validate.py flow.md
python3 scripts/validate.py references/diagrams.md
```

It accepts a markdown file (it checks every fenced block labelled `mermaid`, and that every flow has its legend), any other file (the whole file is one flow, no legend), or `-` for stdin. It exits with a non zero code on any error. Warnings, like a long label, don't fail.

## Library map

Read only what the request needs.

| File | Read it when |
|---|---|
| `references/shapes.md` | Always, first. Every shape with its Name, Used for, prefix, syntax and legend entry. |
| `references/diagrams.md` | Any single flow. Two complete examples (signup, checkout) with their legends. |
| `references/flows.md` | The user wants several flows together, or wants them saved to a file. A full onboarding file: 6 linked flows from first launch to home, one shared legend. |

## Output format

Reply with exactly this, nothing else:

1. One line naming the flow, 10 words or fewer. For example: Password reset, with expired link branch.
2. The legend in its own `mermaid` block.
3. The flow in a fenced code block labelled `mermaid`.

No summary, explanation or follow-up question after the blocks, unless the user asks for one. When asked to change a flow, rewrite its whole block, update the legend if the shapes changed, and validate again.

### Multiple flows

When the user asks for several flows at once, for example login, signup and first-time user:

1. One line naming the set, 10 words or fewer.
2. One shared legend block listing every shape used across all the flows.
3. For each flow: one bold line with its number, name and a short description, for example **1. Login**: returning user signs in, then its `mermaid` block.

Link flows to each other with `sub` nodes named after the other flow, for example `subSignup@{ shape: fr-rect, label: "Signup flow" }`. Validate every flow on its own. When asked to change one flow, rewrite that flow's block, replace only that block, and update the shared legend if the shapes changed.

### Saving to a file

Only when the user asks to save, download or export:

- Save a `.md` file named after the flow or feature, lowercase with hyphens, for example `password-reset.md`. For several flows, name it after the feature, for example `auth.md`.
- Use the folder the user names, otherwise the current working directory.
- File content: a `#` title, the shared legend block, then each flow as a numbered `##` heading, one short line and its `mermaid` block. Use this layout even for a single flow, so the legend stays put when flows are added. See `references/flows.md`.
- If a file with that name exists and you didn't create it in this conversation, ask before overwriting it.
- Once saved, later changes in the conversation update the same file. Replace only the changed flow's block, and the legend if the shapes changed. Add a new flow as the next number. If a flow is removed, renumber the rest.
- Reply with one line: the file path and what changed. For example: Saved to auth.md, signup flow now email only. Ask one short question only if the change affects another flow. This applies after every edit too. Don't list the changes.
- If you can't write files, put the same markdown in the reply inside a block fenced with four backticks, so the inner `mermaid` fences survive.
