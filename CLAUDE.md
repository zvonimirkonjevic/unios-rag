# Rules
- Before strating on a task (if it is something really small then you don't have to) creat a new branch in format: <git_username>/<branch_name>, for <git_username> add my git username.
- Think of this project as a swissarmy knife of agent builds. Do not couple stuff together too much. Develop features that can work on their own and can be combined like LEGOs. If you have concerns about tight coupling raise them.
- When you open a PR spawn subagent to review it (do not give him any context outside the PR to avoid bias), when the subagent finished fix based on his feedback and spawn again until clean.
- Think deeply when deciding how and which tests to write, do not overspam me with tests. Make them actually useful. Keep the overall structure of tests make sense and keep them tidy.
- If you are using git worktrees when building stuff delete worktree after PR merge.
- Before making PR always run relevant tests.
- Always check formatting with ruff.