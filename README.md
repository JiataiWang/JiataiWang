## Hey, I'm Jiatai Wang 👋

PhD candidate @ Nankai University, College of Computer Science | Research on reliable retrieval-augmented LLMs and AI infra.

### Projects

<table>
  <thead>
    <tr>
      <th>Area</th>
      <th>Project</th>
      <th align="center">Stars</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Multimodal parametric RAG</td>
      <td><a href="https://github.com/JiataiWang/SCoRAG">SCoRAG</a></td>
      <td align="center"><a href="https://github.com/JiataiWang/SCoRAG/stargazers">★&nbsp;1</a></td>
      <td>A multimodal parametric RAG framework that compiles retrieved evidence into modality-specific LoRA adapters and routes them to compatible module slots.</td>
    </tr>
    <tr>
      <td>RAG / knowledge-conflict control</td>
      <td><a href="https://github.com/JiataiWang/Swin-VIB">Swin-VIB</a></td>
      <td align="center"><a href="https://github.com/JiataiWang/Swin-VIB/stargazers">★&nbsp;1</a></td>
      <td>Source code for the AAAI 2026 paper <em>Accommodate Knowledge Conflicts in Retrieval-augmented LLMs: Towards Robust Response Generation in the Wild</em>.</td>
    </tr>
    <tr>
      <td>Multi-view representation</td>
      <td><a href="https://github.com/JiataiWang/DistilMVC">DistilMVC</a></td>
      <td align="center"><a href="https://github.com/JiataiWang/DistilMVC/stargazers">★&nbsp;4</a></td>
      <td>Source code for the TNNLS 2024 paper <em>Towards Generalized Multi-stage Clustering: Multi-view Self-distillation</em>.</td>
    </tr>
    <tr>
      <td>Research feed</td>
      <td><a href="https://github.com/JiataiWang/MyArxiv">MyArxiv</a></td>
      <td align="center"><a href="https://github.com/JiataiWang/MyArxiv/stargazers">★&nbsp;0</a></td>
      <td>Personal arXiv tracking and digest setup.</td>
    </tr>
  </tbody>
</table>

### Open Source Contributions

##### Agent frameworks / runtime

<!-- profile-contributions-en -->
<table>
  <thead>
    <tr>
      <th>Project</th>
      <th align="center">Stars</th>
      <th align="center">PR</th>
      <th>What I Did</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><a href="https://github.com/openclaw/openclaw">openclaw</a></td><td align="center"><a href="https://github.com/openclaw/openclaw/stargazers">★&nbsp;391k</a></td><td align="center"><a href="https://github.com/openclaw/openclaw/pull/78288">#78288</a></td><td>Show target node name in exec-tool transparency messages so multi-agent traces stay readable when several agents share an exec channel.</td></tr>
    <tr><td><a href="https://github.com/openclaw/openclaw">openclaw</a></td><td align="center"><a href="https://github.com/openclaw/openclaw/stargazers">★&nbsp;391k</a></td><td align="center"><a href="https://github.com/openclaw/openclaw/pull/113560">#113560</a></td><td>Prevent same-named generated files from overwriting earlier SharePoint uploads so Teams shows the correct current file and retains previous content.</td></tr>
    <tr><td><a href="https://github.com/letta-ai/letta-agent-sdk">letta-ai/letta-agent-sdk</a></td><td align="center"><a href="https://github.com/letta-ai/letta-agent-sdk/stargazers">★&nbsp;104</a></td><td align="center"><a href="https://github.com/letta-ai/letta-agent-sdk/pull/249">#249</a></td><td>Normalize chronological cursors for descending conversation-message pagination, preventing overlapping pages and duplicate messages.</td></tr>
    <tr><td><a href="https://github.com/letta-ai/letta-agent-sdk">letta-ai/letta-agent-sdk</a></td><td align="center"><a href="https://github.com/letta-ai/letta-agent-sdk/stargazers">★&nbsp;104</a></td><td align="center"><a href="https://github.com/letta-ai/letta-agent-sdk/pull/250">#250</a></td><td>Decode file URLs before spawning the MCP test fixture, fixing failures in checkout paths containing spaces or non-ASCII characters.</td></tr>
    <tr><td><a href="https://github.com/ignaciohermosillacornejo/copilot-money-mcp">copilot-money-mcp</a></td><td align="center"><a href="https://github.com/ignaciohermosillacornejo/copilot-money-mcp/stargazers">★&nbsp;83</a></td><td align="center"><a href="https://github.com/ignaciohermosillacornejo/copilot-money-mcp/pull/619">#619</a></td><td>Make privacy comment stripping syntax-aware so comment-like delimiters inside strings, templates, and regular expressions are preserved.</td></tr>
    <tr><td><a href="https://github.com/MemTensor/MemOS">MemTensor/MemOS</a></td><td align="center"><a href="https://github.com/MemTensor/MemOS/stargazers">★&nbsp;12k</a></td><td align="center"><a href="https://github.com/MemTensor/MemOS/pull/2234">#2234</a></td><td>Preserve complete vLLM streaming responses and handle empty or reasoning-only streams safely, preventing truncated output and stream-processing errors.</td></tr>
    <tr><td><a href="https://github.com/vllm-project/vllm">vllm-project/vllm</a></td><td align="center"><a href="https://github.com/vllm-project/vllm/stargazers">★&nbsp;93k</a></td><td align="center"><a href="https://github.com/vllm-project/vllm/pull/53553">#53553</a></td><td>Keep JinaVL image features, cache keys, and prompt positions aligned during cache reuse, preventing mismatched query and document images in multimodal reranking.</td></tr>
    <tr><td><a href="https://github.com/vllm-project/vllm-omni">vllm-project/vllm-omni</a></td><td align="center"><a href="https://github.com/vllm-project/vllm-omni/stargazers">★&nbsp;7.0k</a></td><td align="center"><a href="https://github.com/vllm-project/vllm-omni/pull/6543">#6543</a></td><td>Make MOSS-TTS adapters prioritize request seeds over deployment defaults, restoring request-level control of randomness in Nano speech generation.</td></tr>
    <tr><td><a href="https://github.com/vllm-project/vllm">vllm-project/vllm</a></td><td align="center"><a href="https://github.com/vllm-project/vllm/stargazers">★&nbsp;93k</a></td><td align="center"><a href="https://github.com/vllm-project/vllm/pull/56310">#56310</a></td><td>Enable UUID-based reuse of cached audio without resending payloads, preserving input order when cached and new audio are mixed in a request.</td></tr>
    <tr><td><a href="https://github.com/thedotmack/claude-mem">thedotmack/claude-mem</a></td><td align="center"><a href="https://github.com/thedotmack/claude-mem/stargazers">★&nbsp;95k</a></td><td align="center"><a href="https://github.com/thedotmack/claude-mem/pull/3407">#3407</a></td><td>Align the timeline-report skill&#x27;s schema guidance and recall queries with the actual database, preventing SQL failures and misleading recall statistics.</td></tr>
  </tbody>
</table>

### Research Direction

Retrieval-augmented generation under context distortion · knowledge-conflict control · learnable long-context compression · agent context-management policy evaluation.

---

## 你好，我是王嘉泰 👋

南开大学计算机学院在读博士 | 研究方向：可靠的检索增强大模型与 AI 基础设施。

### 项目

<table>
  <thead>
    <tr>
      <th>方向</th>
      <th>项目</th>
      <th align="center">Stars</th>
      <th>简介</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>多模态参数化 RAG</td>
      <td><a href="https://github.com/JiataiWang/SCoRAG">SCoRAG</a></td>
      <td align="center"><a href="https://github.com/JiataiWang/SCoRAG/stargazers">★&nbsp;1</a></td>
      <td>将检索证据编译为模态专用 LoRA 适配器，并通过槽位路由将其注入兼容模块的多模态参数化 RAG 框架。</td>
    </tr>
    <tr>
      <td>RAG / 知识冲突控制</td>
      <td><a href="https://github.com/JiataiWang/Swin-VIB">Swin-VIB</a></td>
      <td align="center"><a href="https://github.com/JiataiWang/Swin-VIB/stargazers">★&nbsp;1</a></td>
      <td>AAAI 2026 论文《Accommodate Knowledge Conflicts in Retrieval-augmented LLMs: Towards Robust Response Generation in the Wild》源码实现。</td>
    </tr>
    <tr>
      <td>多视图表征</td>
      <td><a href="https://github.com/JiataiWang/DistilMVC">DistilMVC</a></td>
      <td align="center"><a href="https://github.com/JiataiWang/DistilMVC/stargazers">★&nbsp;4</a></td>
      <td>TNNLS 2024 论文《Towards Generalized Multi-stage Clustering: Multi-view Self-distillation》源码实现。</td>
    </tr>
    <tr>
      <td>研究追踪</td>
      <td><a href="https://github.com/JiataiWang/MyArxiv">MyArxiv</a></td>
      <td align="center"><a href="https://github.com/JiataiWang/MyArxiv/stargazers">★&nbsp;0</a></td>
      <td>个人 arXiv 跟踪与摘要工具。</td>
    </tr>
  </tbody>
</table>

### 开源贡献

##### Agent 框架

<!-- profile-contributions-zh -->
<table>
  <thead>
    <tr>
      <th>项目</th>
      <th align="center">Stars</th>
      <th align="center">PR</th>
      <th>修了啥</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><a href="https://github.com/openclaw/openclaw">openclaw</a></td><td align="center"><a href="https://github.com/openclaw/openclaw/stargazers">★&nbsp;391k</a></td><td align="center"><a href="https://github.com/openclaw/openclaw/pull/78288">#78288</a></td><td>在 exec 工具的透传消息中展示目标节点名，让多个 agent 共享 exec 通道时的执行轨迹依然可读。</td></tr>
    <tr><td><a href="https://github.com/openclaw/openclaw">openclaw</a></td><td align="center"><a href="https://github.com/openclaw/openclaw/stargazers">★&nbsp;391k</a></td><td align="center"><a href="https://github.com/openclaw/openclaw/pull/113560">#113560</a></td><td>避免同名生成文件覆盖已有的 SharePoint 上传，使 Teams 显示正确的当前文件并保留先前内容。</td></tr>
    <tr><td><a href="https://github.com/letta-ai/letta-agent-sdk">letta-ai/letta-agent-sdk</a></td><td align="center"><a href="https://github.com/letta-ai/letta-agent-sdk/stargazers">★&nbsp;104</a></td><td align="center"><a href="https://github.com/letta-ai/letta-agent-sdk/pull/249">#249</a></td><td>规范降序消息分页的时间游标，避免翻页时出现页面重叠和重复消息。</td></tr>
    <tr><td><a href="https://github.com/letta-ai/letta-agent-sdk">letta-ai/letta-agent-sdk</a></td><td align="center"><a href="https://github.com/letta-ai/letta-agent-sdk/stargazers">★&nbsp;104</a></td><td align="center"><a href="https://github.com/letta-ai/letta-agent-sdk/pull/250">#250</a></td><td>启动 MCP 测试夹具前正确解码文件 URL，修复检出路径包含空格或非 ASCII 字符时的失败。</td></tr>
    <tr><td><a href="https://github.com/ignaciohermosillacornejo/copilot-money-mcp">copilot-money-mcp</a></td><td align="center"><a href="https://github.com/ignaciohermosillacornejo/copilot-money-mcp/stargazers">★&nbsp;83</a></td><td align="center"><a href="https://github.com/ignaciohermosillacornejo/copilot-money-mcp/pull/619">#619</a></td><td>让隐私扫描中的注释移除具备语法感知能力，保留字符串、模板和正则表达式中的类注释分隔符。</td></tr>
    <tr><td><a href="https://github.com/MemTensor/MemOS">MemTensor/MemOS</a></td><td align="center"><a href="https://github.com/MemTensor/MemOS/stargazers">★&nbsp;12k</a></td><td align="center"><a href="https://github.com/MemTensor/MemOS/pull/2234">#2234</a></td><td>修复 vLLM 流式响应丢失分块的问题，并妥善处理空流与纯推理流，避免输出截断和流处理异常。</td></tr>
    <tr><td><a href="https://github.com/vllm-project/vllm">vllm-project/vllm</a></td><td align="center"><a href="https://github.com/vllm-project/vllm/stargazers">★&nbsp;93k</a></td><td align="center"><a href="https://github.com/vllm-project/vllm/pull/53553">#53553</a></td><td>保证 JinaVL 复用缓存时图像特征、缓存键与提示词位置一致，避免多模态重排序中查询与文档图像错配。</td></tr>
    <tr><td><a href="https://github.com/vllm-project/vllm-omni">vllm-project/vllm-omni</a></td><td align="center"><a href="https://github.com/vllm-project/vllm-omni/stargazers">★&nbsp;7.0k</a></td><td align="center"><a href="https://github.com/vllm-project/vllm-omni/pull/6543">#6543</a></td><td>让 MOSS-TTS 适配器优先采用请求指定的随机种子，恢复 Nano 语音生成的请求级随机性控制。</td></tr>
    <tr><td><a href="https://github.com/vllm-project/vllm">vllm-project/vllm</a></td><td align="center"><a href="https://github.com/vllm-project/vllm/stargazers">★&nbsp;93k</a></td><td align="center"><a href="https://github.com/vllm-project/vllm/pull/56310">#56310</a></td><td>支持通过 UUID 复用已缓存音频，无需重复传输音频数据，并保持缓存音频与新音频混合请求中的输入顺序。</td></tr>
    <tr><td><a href="https://github.com/thedotmack/claude-mem">thedotmack/claude-mem</a></td><td align="center"><a href="https://github.com/thedotmack/claude-mem/stargazers">★&nbsp;95k</a></td><td align="center"><a href="https://github.com/thedotmack/claude-mem/pull/3407">#3407</a></td><td>将时间线报告 skill 的数据库结构说明和记忆召回查询与实际表结构对齐，避免 SQL 执行失败及误导性的召回统计。</td></tr>
  </tbody>
</table>

### 研究方向

检索增强生成下的上下文失真 · 知识冲突控制 · 可学习的长上下文压缩 · Agent 上下文管理策略评测。
