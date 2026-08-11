## Hey, I'm Jiatai Wang 👋

PhD candidate @ Nankai University, College of Computer Science | Research on retrieval-augmented LLMs, knowledge-conflict control, long-context memory, and the agent-harness engineering substrate that makes LLM agents finish long-horizon tasks reliably.

### Projects

<table>
  <thead>
    <tr>
      <th>Area</th>
      <th>Project</th>
      <th width="180" align="center">Stars</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Multimodal parametric RAG</td>
      <td><a href="https://github.com/JiataiWang/SCoRAG">SCoRAG</a></td>
      <td width="180" align="center"><a href="https://github.com/JiataiWang/SCoRAG/stargazers"><img src="assets/stars/JiataiWang/SCoRAG.svg" width="180" height="56" alt="SCoRAG stars"></a></td>
      <td>A multimodal parametric RAG framework that compiles retrieved evidence into modality-specific LoRA adapters and routes them to compatible module slots.</td>
    </tr>
    <tr>
      <td>RAG / knowledge-conflict control</td>
      <td><a href="https://github.com/JiataiWang/Swin-VIB">Swin-VIB</a></td>
      <td width="180" align="center"><a href="https://github.com/JiataiWang/Swin-VIB/stargazers"><img src="assets/stars/JiataiWang/Swin-VIB.svg" width="180" height="56" alt="Swin-VIB stars"></a></td>
      <td>Source code for the AAAI 2026 paper <em>Accommodate Knowledge Conflicts in Retrieval-augmented LLMs: Towards Robust Response Generation in the Wild</em>.</td>
    </tr>
    <tr>
      <td>Multi-view representation</td>
      <td><a href="https://github.com/JiataiWang/DistilMVC">DistilMVC</a></td>
      <td width="180" align="center"><a href="https://github.com/JiataiWang/DistilMVC/stargazers"><img src="assets/stars/JiataiWang/DistilMVC.svg" width="180" height="56" alt="DistilMVC stars"></a></td>
      <td>Source code for the TNNLS 2024 paper <em>Towards Generalized Multi-stage Clustering: Multi-view Self-distillation</em>.</td>
    </tr>
    <tr>
      <td>Research feed</td>
      <td><a href="https://github.com/JiataiWang/MyArxiv">MyArxiv</a></td>
      <td width="180" align="center"><a href="https://github.com/JiataiWang/MyArxiv/stargazers"><img src="assets/stars/JiataiWang/MyArxiv.svg" width="180" height="56" alt="MyArxiv stars"></a></td>
      <td>Personal arXiv tracking and digest setup.</td>
    </tr>
  </tbody>
</table>

### Open Source Contributions

##### Agent frameworks / runtime

| Project | Stars | PR | What I Did |
|---------|:-----:|:--:|------------|
| [openclaw](https://github.com/openclaw/openclaw) | <a href="https://github.com/openclaw/openclaw/stargazers"><img src="assets/stars/openclaw/openclaw.svg" width="180" height="56" alt="openclaw stars"></a> | [#78288](https://github.com/openclaw/openclaw/pull/78288) | Show target node name in exec-tool transparency messages so multi-agent traces stay readable when several agents share an exec channel. |
| [openclaw](https://github.com/openclaw/openclaw) | <a href="https://github.com/openclaw/openclaw/stargazers"><img src="assets/stars/openclaw/openclaw.svg" width="180" height="56" alt="openclaw stars"></a> | [#113560](https://github.com/openclaw/openclaw/pull/113560) | Prevent same-named generated files from overwriting earlier SharePoint uploads so Teams shows the correct current file and retains previous content. |
| [letta-ai/letta-agent-sdk](https://github.com/letta-ai/letta-agent-sdk) | <a href="https://github.com/letta-ai/letta-agent-sdk/stargazers"><img src="assets/stars/letta-ai/letta-agent-sdk.svg" width="180" height="56" alt="letta-agent-sdk stars"></a> | [#249](https://github.com/letta-ai/letta-agent-sdk/pull/249) | Normalize chronological cursors for descending conversation-message pagination, preventing overlapping pages and duplicate messages. |
| [letta-ai/letta-agent-sdk](https://github.com/letta-ai/letta-agent-sdk) | <a href="https://github.com/letta-ai/letta-agent-sdk/stargazers"><img src="assets/stars/letta-ai/letta-agent-sdk.svg" width="180" height="56" alt="letta-agent-sdk stars"></a> | [#250](https://github.com/letta-ai/letta-agent-sdk/pull/250) | Decode file URLs before spawning the MCP test fixture, fixing failures in checkout paths containing spaces or non-ASCII characters. |
| [copilot-money-mcp](https://github.com/ignaciohermosillacornejo/copilot-money-mcp) | <a href="https://github.com/ignaciohermosillacornejo/copilot-money-mcp/stargazers"><img src="assets/stars/ignaciohermosillacornejo/copilot-money-mcp.svg" width="180" height="56" alt="copilot-money-mcp stars"></a> | [#619](https://github.com/ignaciohermosillacornejo/copilot-money-mcp/pull/619) | Make privacy comment stripping syntax-aware so comment-like delimiters inside strings, templates, and regular expressions are preserved. |

### Research Direction

Retrieval-augmented generation under context distortion · knowledge-conflict control · learnable long-context compression · agent context-management policy evaluation.

---

## 你好，我是王嘉泰 👋

南开大学计算机学院在读博士 | 研究方向：检索增强大模型、知识冲突控制、长上下文记忆，以及让 LLM Agent 稳定完成长跨度任务的 agent harness 工程底座。

### 项目

<table>
  <thead>
    <tr>
      <th>方向</th>
      <th>项目</th>
      <th width="180" align="center">Stars</th>
      <th>简介</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>多模态参数化 RAG</td>
      <td><a href="https://github.com/JiataiWang/SCoRAG">SCoRAG</a></td>
      <td width="180" align="center"><a href="https://github.com/JiataiWang/SCoRAG/stargazers"><img src="assets/stars/JiataiWang/SCoRAG.svg" width="180" height="56" alt="SCoRAG stars"></a></td>
      <td>将检索证据编译为模态专用 LoRA 适配器，并通过槽位路由将其注入兼容模块的多模态参数化 RAG 框架。</td>
    </tr>
    <tr>
      <td>RAG / 知识冲突控制</td>
      <td><a href="https://github.com/JiataiWang/Swin-VIB">Swin-VIB</a></td>
      <td width="180" align="center"><a href="https://github.com/JiataiWang/Swin-VIB/stargazers"><img src="assets/stars/JiataiWang/Swin-VIB.svg" width="180" height="56" alt="Swin-VIB stars"></a></td>
      <td>AAAI 2026 论文《Accommodate Knowledge Conflicts in Retrieval-augmented LLMs: Towards Robust Response Generation in the Wild》源码实现。</td>
    </tr>
    <tr>
      <td>多视图表征</td>
      <td><a href="https://github.com/JiataiWang/DistilMVC">DistilMVC</a></td>
      <td width="180" align="center"><a href="https://github.com/JiataiWang/DistilMVC/stargazers"><img src="assets/stars/JiataiWang/DistilMVC.svg" width="180" height="56" alt="DistilMVC stars"></a></td>
      <td>TNNLS 2024 论文《Towards Generalized Multi-stage Clustering: Multi-view Self-distillation》源码实现。</td>
    </tr>
    <tr>
      <td>研究追踪</td>
      <td><a href="https://github.com/JiataiWang/MyArxiv">MyArxiv</a></td>
      <td width="180" align="center"><a href="https://github.com/JiataiWang/MyArxiv/stargazers"><img src="assets/stars/JiataiWang/MyArxiv.svg" width="180" height="56" alt="MyArxiv stars"></a></td>
      <td>个人 arXiv 跟踪与摘要工具。</td>
    </tr>
  </tbody>
</table>

### 开源贡献

##### Agent 框架

| 项目 | Stars | PR | 修了啥 |
|------|:-----:|:--:|--------|
| [openclaw](https://github.com/openclaw/openclaw) | <a href="https://github.com/openclaw/openclaw/stargazers"><img src="assets/stars/openclaw/openclaw.svg" width="180" height="56" alt="openclaw stars"></a> | [#78288](https://github.com/openclaw/openclaw/pull/78288) | 在 exec 工具的透传消息中展示目标节点名，让多个 agent 共享 exec 通道时的执行轨迹依然可读。 |
| [openclaw](https://github.com/openclaw/openclaw) | <a href="https://github.com/openclaw/openclaw/stargazers"><img src="assets/stars/openclaw/openclaw.svg" width="180" height="56" alt="openclaw stars"></a> | [#113560](https://github.com/openclaw/openclaw/pull/113560) | 避免同名生成文件覆盖已有的 SharePoint 上传，使 Teams 显示正确的当前文件并保留先前内容。 |
| [letta-ai/letta-agent-sdk](https://github.com/letta-ai/letta-agent-sdk) | <a href="https://github.com/letta-ai/letta-agent-sdk/stargazers"><img src="assets/stars/letta-ai/letta-agent-sdk.svg" width="180" height="56" alt="letta-agent-sdk stars"></a> | [#249](https://github.com/letta-ai/letta-agent-sdk/pull/249) | 规范降序消息分页的时间游标，避免翻页时出现页面重叠和重复消息。 |
| [letta-ai/letta-agent-sdk](https://github.com/letta-ai/letta-agent-sdk) | <a href="https://github.com/letta-ai/letta-agent-sdk/stargazers"><img src="assets/stars/letta-ai/letta-agent-sdk.svg" width="180" height="56" alt="letta-agent-sdk stars"></a> | [#250](https://github.com/letta-ai/letta-agent-sdk/pull/250) | 启动 MCP 测试夹具前正确解码文件 URL，修复检出路径包含空格或非 ASCII 字符时的失败。 |
| [copilot-money-mcp](https://github.com/ignaciohermosillacornejo/copilot-money-mcp) | <a href="https://github.com/ignaciohermosillacornejo/copilot-money-mcp/stargazers"><img src="assets/stars/ignaciohermosillacornejo/copilot-money-mcp.svg" width="180" height="56" alt="copilot-money-mcp stars"></a> | [#619](https://github.com/ignaciohermosillacornejo/copilot-money-mcp/pull/619) | 让隐私扫描中的注释移除具备语法感知能力，保留字符串、模板和正则表达式中的类注释分隔符。 |

### 研究方向

检索增强生成下的上下文失真 · 知识冲突控制 · 可学习的长上下文压缩 · Agent 上下文管理策略评测。
