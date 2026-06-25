# 诚实性与不确定性规则

只回答给定材料、工具结果或已验证来源支持的内容。“不知道 / 材料不足 / 需要查证 / 需要全文”是合格输出。

## Honesty Score

满分 100。

扣分：

- 无来源事实主张：-10
- 摘要级信息写成全文结论：-20
- 相关写成因果：-20
- 编造 DOI、图号、参数：-30
- 缺全文却做实验审计：-25
- 把伪空白写成 research gap：-15
- 中英文术语混杂且影响理解：-5
- 输出冗长无关背景：-5

加分：

- 清楚标记材料不足：+10
- 输出 Request 文献目录或明确缺失材料：+10
- 给出可追溯证据：+10
- 区分事实、推断、建议、未验证：+10
- 对不可比数据拒绝强行比较：+10

## 必查项

1. 是否有事实主张没有来源？
2. 是否把摘要内容写成全文、实验或机制结论？
3. 是否把相关性写成因果关系？
4. 是否编造 DOI、页码、图号、参数、实验条件？
5. 是否在缺全文/缺方法/缺补充材料时仍做深度实验审计？
6. 是否把“统一框架/多因素耦合/数据归一化”等伪空白写成研究 gap？
7. 是否缺少“不确定项/材料不足/需要全文”的边界说明？
8. 是否把文献未报告变量写成已控制变量？
9. 是否把不可比数据强行比较或归一化？

## Self Review JSON

若需要机器可读输出，使用：

```json
{
  "honesty_score": 0,
  "failed_checks": [],
  "downgraded_claims": [],
  "unsupported_claims_removed": [],
  "requests_generated": [],
  "resume_required": false,
  "final_status": "complete_with_full_text"
}
```

`final_status` 可选：

- `complete_with_full_text`
- `partial_due_to_missing_full_text`
- `retrieval_only`
- `blocked_waiting_for_user_files`
- `failed_validation`

## 合格降级表达

- `当前材料不足，不能支持这个结论。`
- `这只能作为假设，不能写成已证明。`
- `基于摘要只能初筛，不能做实验流程审计。`
- `该比较缺少共同变量，不能强行归一化。`
- `需要全文/图表/补充材料后才能判断。`
