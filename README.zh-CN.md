        # Agent Session Repro Bundle Checker

        `agent-session-repro-bundle-checker-20260711` 是一个轻量、少依赖的命令行工具，面向正在使用 AI Agent、MCP 工具和自动化开发流程的团队。

        ## 解决的痛点

        Bug reports from coding agents often miss the exact prompt, command log, git state, and redaction evidence needed to reproduce a failure. Maintainers lose time asking for basics.

        ## 为什么现在值得做

        Terminal agents and cloud teammates are now common in developer workflows; reproducibility and privacy checks need to happen before an agent transcript is pasted into an issue.

        ## 安装与运行

        ```bash
        python -m pip install -e .
        python -m agent_session_repro_bundle_checker_20260711.cli examples/bundle --json
        ```

        ## 示例

        ```bash
mkdir -p examples/bundle
printf "prompt: fix test\n" > examples/bundle/prompt.txt
printf "git status clean\n" > examples/bundle/git-status.txt
printf "pytest ok\n" > examples/bundle/commands.log
python -m agent_session_repro_bundle_checker_20260711.cli examples/bundle
# Score: 86/100, missing: redactions.txt
```

        ## 自检

        ```bash
        python -m unittest discover -s tests
        ```

        ## 路线图

        - Add GitHub issue template export
- Support SARIF output
- Detect screenshots and binary attachments
- Integrate with CI artifact checks

        ## License

        MIT
