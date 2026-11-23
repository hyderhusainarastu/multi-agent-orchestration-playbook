# Framework mapping

**Verify APIs against current docs.** Checked 2026-11-23 from general knowledge of each tool, not by running them. Feature names change quickly.

| Concept | Claude Code | Codex CLI | Cursor | Gemini CLI | OpenAI Agents SDK | LangGraph | CrewAI | Plain asyncio |
|---|---|---|---|---|---|---|---|---|
| Moderator loop | main session | main session | main agent | main session | orchestrator agent | supervisor node | manager agent | your `main()` |
| Sub-agent with own brief | subagent | spawned run (`codex exec`) | background agent | a separate CLI run | handoff / agent-as-tool | node or subgraph | Agent + Task | `asyncio.create_task` |
| Tier routing | per-agent model setting | `-m` flag or profile | model picker per agent | `-m` flag | model per agent | model per node | LLM per agent | model name per call |
| Project instructions | `CLAUDE.md` (imports `AGENTS.md`) | `AGENTS.md` | `AGENTS.md` | `GEMINI.md` (imports `AGENTS.md`) | system prompt | prompt per node | backstory / goal | prompt strings |
| Plan, judge, critic | separate sub-agents | separate runs | separate agents | separate runs | separate agents | separate nodes | separate agents in a process | separate coroutines |
| Single owner / write root | path rules in brief | sandbox mode and cwd | worktree per agent | working directory | tool permissions | state keys per node | task output files | directories per task |
| Silent-drop guard | wrap in script, call `guards` | same | same | same | guard in tool wrapper | check in edge condition | task callback | call `guard_non_empty` |
| Resume | read on-disk state | read on-disk state | read on-disk state | read on-disk state | run state from saved trace | checkpointer | task outputs on disk | `state.json` |
| Loop caps | counters in `state.json` | same | same | same | max turns setting | recursion limit | max iterations | counters in code |
| Verify by a different agent | fresh sub-agent | fresh run | fresh agent | fresh run | separate agent | separate node | separate agent | separate call |

## Notes

- In every column the guard scripts work the same way, because they only read and write files and counts.
- "Fresh run" means a new process with no shared conversation, so the verifier cannot see how the work was made.
- Where a framework has built-in state or checkpointing, still write the stage counts to disk. A human must be able to resume without the framework.
- Cloud agents and background agents can write in parallel; give each its own worktree or branch so that single-owner rules hold.
