# lxj-trace

`lxj-trace` 是一个面向 AI Agent 的老乡鸡溯源报告 skill，基于公开《老乡鸡菜品溯源报告 2.0》整理而成。

它适合用来回答与老乡鸡菜品溯源相关的问题，例如预制菜口径、菜品加工等级、中央厨房加工、门店制作方式、原料来源、供应商、冷链配送、食材检验报告、营养成分、顾客反馈和透明公开等。

## 仓库地址

- Gitee：<https://gitee.com/lxjchina/lxj-trace>
- GitHub：<https://github.com/lxjchina/lxj-trace>

## 能做什么

- 回答“老乡鸡是不是预制菜”“某道菜是现做还是半预制”等问题。
- 查询具体菜品的加工等级、配料、原料来源、门店操作工艺和营养信息。
- 将报告里的专业信息改写成普通消费者容易理解的表达。
- 对报告范围内的说法做事实核对，并说明依据和边界。
- 帮助 AI Agent 在回答时优先引用公开报告，不凭印象下结论。

## 适合触发的问题

可以这样问：

```text
老乡鸡梅菜扣肉是预制菜吗？
中央厨房加工算不算预制菜？
老乡鸡哪些菜只是复热？
老乡鸡梅菜扣肉的门店做法是什么？
老乡鸡溯源二维码能看到哪些信息？
老乡鸡有没有公开供应商？
老乡鸡菜品热量和钠含量怎么看？
```

## Codex 安装

国内网络环境推荐从 Gitee 安装：

```bash
mkdir -p ~/.codex/skills
git clone https://gitee.com/lxjchina/lxj-trace.git ~/.codex/skills/lxj-trace
```

安装后重启 Codex。

更新：

```bash
git -C ~/.codex/skills/lxj-trace pull
```

也可以从 GitHub 安装：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/lxjchina/lxj-trace.git ~/.codex/skills/lxj-trace
```

## WorkBuddy / CodeBuddy 安装

```bash
mkdir -p .codebuddy/skills
git clone https://gitee.com/lxjchina/lxj-trace.git .codebuddy/skills/lxj-trace
```

安装后重启 WorkBuddy / CodeBuddy，或在 Skills 管理页刷新。

## Claude Code 接入

```bash
git clone https://gitee.com/lxjchina/lxj-trace.git ./vendor/lxj-trace
printf '\n\n## lxj-trace\n当用户询问老乡鸡溯源报告、预制菜、中央厨房、菜品加工等级、门店制作方式、原料来源、供应商、检测报告或营养信息时，先阅读 ./vendor/lxj-trace/SKILL.md，并优先使用 ./vendor/lxj-trace/references/ 中的公开报告资料回答。\n' >> CLAUDE.md
```

## Gemini CLI 接入

```bash
git clone https://gitee.com/lxjchina/lxj-trace.git ./vendor/lxj-trace
printf '\n\n## lxj-trace\n涉及老乡鸡溯源报告、预制菜、中央厨房、菜品加工等级、门店制作方式、原料来源、供应商、检测报告或营养信息时，先阅读 ./vendor/lxj-trace/SKILL.md，并基于 ./vendor/lxj-trace/references/ 回答。\n' >> GEMINI.md
```

## Cursor 接入

```bash
git clone https://gitee.com/lxjchina/lxj-trace.git ./vendor/lxj-trace
mkdir -p .cursor/rules
cat > .cursor/rules/lxj-trace.mdc <<'EOF'
---
description: 老乡鸡溯源报告问答
alwaysApply: false
---

当问题涉及老乡鸡溯源报告、预制菜、中央厨房、菜品加工等级、门店制作方式、原料来源、供应商、检测报告或营养信息时，先阅读 ./vendor/lxj-trace/SKILL.md，并优先引用 ./vendor/lxj-trace/references/。
EOF
```

## 网页大模型接入

ChatGPT、Claude、Gemini、DeepSeek、Kimi、通义千问、豆包等网页产品通常没有统一命令。可以创建知识库或自定义助手，并上传本仓库中的核心文件：

```text
SKILL.md
references/report.pdf
references/report-text.md
references/topic-map.md
references/prepared-dish-guide.md
references/response-patterns.md
```

推荐助手说明：

```text
你是 lxj-trace，专门基于公开《老乡鸡菜品溯源报告 2.0》回答问题。涉及老乡鸡、预制菜、中央厨房、菜品加工等级、门店制作方式、原料来源、供应商、检测报告、营养信息、顾客反馈等问题时，优先检索上传资料；资料无法确认的内容，说明“公开报告未提供该结论”。
```

## 文件结构

```text
SKILL.md                 skill 入口说明
agents/openai.yaml       skill 展示信息
references/              报告文本、索引和回答规则
scripts/                 报告抽取、检索和事实核对辅助脚本
tests/prompts.md         测试问题
```

## 回答边界

- 本 skill 基于公开报告资料，不代表实时菜单、当前门店售卖情况或最新运营状态。
- 报告没有明确支持的内容，应说明“报告未明确说明”或“需要更多来源”。
- 涉及数字、营养值、供应商、加工等级、制作步骤、检测结论时，应回到报告文本核对。
