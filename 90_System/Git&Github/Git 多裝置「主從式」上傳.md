---
tags: ['Git', 'Sync', 'Multi-device']
---
## 摘要

當你這台電腦改了很多，想推上去 GitHub，但 GitHub 提示「遠端有更新，不讓你 Push」時。

```bash
git add .
git commit -m "Local update (Primary)"
git fetch origin
git merge -X ours origin/main --no-edit
git push origin main
```

### 動作拆解

1. `fetch`: 先把遠端的更新抓下來，但不合併。
2. `merge -X ours`: 將遠端更新與本機合併，若有衝突，以本機為準。
3. `push`: 合併完成後，將這個「本機勝出」的版本推回 GitHub。