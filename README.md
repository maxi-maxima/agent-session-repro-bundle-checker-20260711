        # Agent Session Repro Bundle Checker

        `agent-session-repro-bundle-checker-20260711` is a small, dependency-light CLI for teams adopting AI agents, MCP tools, and automated developer workflows.

        ## Pain point

        Bug reports from coding agents often miss the exact prompt, command log, git state, and redaction evidence needed to reproduce a failure. Maintainers lose time asking for basics.

        ## Why now

        Terminal agents and cloud teammates are now common in developer workflows; reproducibility and privacy checks need to happen before an agent transcript is pasted into an issue.

        ## Install and run

        ```bash
        python -m pip install -e .
        python -m agent_session_repro_bundle_checker_20260711.cli examples/bundle --json
        ```

        ## Example

        ```bash
mkdir -p examples/bundle
printf "prompt: fix test\n" > examples/bundle/prompt.txt
printf "git status clean\n" > examples/bundle/git-status.txt
printf "pytest ok\n" > examples/bundle/commands.log
python -m agent_session_repro_bundle_checker_20260711.cli examples/bundle
# Score: 86/100, missing: redactions.txt
```

JSON output reports secret-like hit locations with redacted line text, so the
checker can be shared without echoing the suspected credential.

        ## Self-check

        ```bash
        python -m unittest discover -s tests
        ```

        ## Roadmap

        - Add GitHub issue template export
- Support SARIF output
- Detect screenshots and binary attachments
- Integrate with CI artifact checks

        ## License

        MIT
