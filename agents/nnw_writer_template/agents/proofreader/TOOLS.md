## write file tool
**Both `file_path` AND `content` are required.** Never call `write` without `content`
```
✅ write(file_path="novel/ch01.md", content="# 第一章\n\n正文...")
❌ write(file_path="novel/ch01.md")  ← WRONG!
```
