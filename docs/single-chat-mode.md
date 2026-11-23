# Single-chat mode

For ChatGPT, Claude.ai, Gemini or a local model in a chat window, where there are no sub-agents and you are the orchestrator. You run the same stages one after another, each in a fresh message or fresh chat, with a pasted brief.

## How to run it

1. Open a chat and paste `PROMPT.md`. It sets the roles and the output format.
2. **Understand.** Paste your material and ask for a list of facts, open questions and risks. Keep the reply; start a new chat for the next step.
3. **Independent plans.** In two or three separate chats, paste only the goal and the facts. Ask each for a plan. Do not show a chat the other plans.
4. **Judge.** In a new chat, paste the plans and ask for a comparison and one chosen plan, with reasons.
5. **Critic.** In another new chat, paste the chosen plan and ask for the three most likely ways it fails.
6. **You review.** You are the moderator. Decide.
7. **Execute** in small pieces, one brief per piece (use `templates/brief-header.md`). Keep outputs in files or notes, not only in the scrollback.
8. **Adversarial verify** in a fresh chat that has not seen how the work was made. Give it the output and the acceptance test only.
9. **Ship** only after the verifier's list is clear or its defects are fixed and re-checked in a fresh chat.

## Which rules still apply

| Rule | In a single chat |
|---|---|
| Moderator only | Yes: you decide; the chat drafts |
| Tiers | Pick a smaller model for mechanical steps if your tool allows it |
| Plan, judge, critic | Yes, using separate chats so they cannot see each other |
| No self-approval | Yes: verify in a fresh chat, never in the chat that made the work |
| Single owner per file | Yes, for the files you keep. One chat edits a given file |
| Silent-drop guard | Yes: count items before you paste and after the reply, by hand or with a script |
| Shard coverage by list | Yes: number your items and check the numbers returned |
| Never hand-count | Use `tools/` or a spreadsheet formula for totals |
| No facts from memory | Yes, strictly: ask for sources, then check them yourself |
| Never message mid-run | Not applicable |
| Loop caps | Yes: set a number of revision rounds before you start and stop there |

## Practical limits

- Long chats drift. Restart with a short brief rather than adding to a long thread.
- A chat cannot read your disk. Paste what it needs, and say what it must not assume.
- Models may confidently invent references. Verify every reference outside the chat.
