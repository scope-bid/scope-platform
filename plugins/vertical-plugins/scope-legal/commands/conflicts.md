---
name: conflicts
description: Run a conflict check standalone, without dispatching.
---

When the user runs `/conflicts`, fire the conflict-check-workflow skill
from scope-core. Useful when the lawyer wants to clear a matter
through conflicts before the rest of the team starts intake work.

If the user passes args like `/conflicts party Acme Corp; party John
Smith`, parse the parties from the args. If the user passes no args,
ask once for the party list.

When the check completes, surface the result in plain English. If
clear, say so once. If a hit is found, halt and surface the matter
ID, conflict source, and date of prior representation if known. Do
not advise on whether the lawyer can proceed.
