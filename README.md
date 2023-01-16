# Point Collector
Fetch students point report at [Sở GD&DT TTH | Cổng thông tin đào tạo](https://qlttgddt.thuathienhue.edu.vn/).

First, **install** dependencies by running `pip install -r requirements.txt`

Choose one of those methods:

## chrome **(most stable)**
> [Arguments References](https://peter.sh/experiments/chromium-command-line-switches/)

Find the *variable or function* marked with the comment **[CONFIG]** and modify it to meet your requirements.

```python
...
table_sel(1,1) # [CONFIG] Year ?, Semester 1 or 2
...
for user_id in range(3000_350_000, 3000_400_000): # [CONFIG] UID range
...
```

To save time, the UID range should be set from 3000350000 to 3000399999.

**DO NOT** use `add_argument("--headless")`, otherwise it won't able to interact with Chrome.



## fetch **(idk, help)**
> No docs.
## *img* **(abandoned, high error rate)**
> Default settings is for Windows 10, Taskbar put on top, 1366x768 screen reslution.