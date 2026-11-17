# 多渠道诉求漏报估计业务服务

现有服务只按明确 issue 编号合并诉求，不作模糊身份推断。匿名记录无联系标记；渠道开放期间单独记录，缺少开放记录不代表零问题。问题跟进与覆盖抽样回访使用不同 purpose。`POST /api/report` 保存渠道记录，`POST /api/close` 接受 id，`POST /api/reply` 保存回访结果。当前 coverage 仅描述已登记诉求。

## 启动与核对

使用 Python 3.11 或更高版本。现有服务采用标准库运行；数值分析所需的固定版本工具列在 requirements.txt，部署准备时运行 `python3 -m pip install -r requirements.txt`，之后可以断网运行。无需真实个人信息、凭据或远程数据源。

```sh
python3 -m unittest discover -s tests -v
python3 -m compileall -q complaints tests
python3 -m complaints check
python3 -m complaints demo
python3 -m complaints load --database /tmp/complaints-business.sqlite3 --input examples/operations.json
python3 -m complaints serve --database /tmp/complaints-business.sqlite3
```

服务默认监听本机 8765 端口，`--port` 可指定其他端口。健康检查为 `GET /health`，`GET /api/summary` 返回当前已有业务汇总。未指定数据库时，demo 和 check 使用隔离的临时数据库；serve 若需保留修改须传入数据库路径。已有数据库不重复装载同一类样例。examples/operations.json 是较大的一组历史运营资料，可用 load 命令在事务内载入；按类型和编号更正同名记录，未出现的记录保持不变。所有资料采用固定来源生成且不包含对未来分析结论的预设值。

## 数据与运行边界

fixtures 中均为本地合成业务资料，员工、家庭和院区编号不对应真实对象。JSON 里的空值表示未记录，不代表零；日期采用 ISO 格式。金额以分保存，工时以分钟保存。每类记录有独立编号，写入同编号用于业务更正，revision 用于并发修改核对。

业务状态由 SQLite 保存，记录批量更正在单一事务内提交。接口使用 UTF-8 JSON，未知资源返回 404，非法数据返回 400，版本冲突返回 409。服务不进行临床诊断，也不自动改变实际服务安排。测试使用临时数据库和系统分配的空闲端口，彼此隔离，不访问公网。运行日志、数据库和依赖缓存不应提交到仓库。
