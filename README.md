# codex-loop-lab

这是一个用于测试多 Agent / Codex 交接工作流的命令行 Todo 项目。

任务数据使用 JSON 文件保存。一条任务的数据结构类似：

```json
{
  "id": 1,
  "title": "买牛奶",
  "done": false
}
```

第一轮功能提供新增和列出任务：

```text
python -m tasklist add "买牛奶"
python -m tasklist list
```

以上命令可直接在仓库根目录运行，无需设置 `PYTHONPATH`。测试使用临时数据文件，不会污染用户真实数据文件。

## 运行测试

在仓库根目录执行：

```text
pytest -q
```
