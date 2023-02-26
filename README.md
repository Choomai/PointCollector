# Point Collector
Fetch students point report at [Sở GD&DT TTH | Cổng thông tin đào tạo](https://qlttgddt.thuathienhue.edu.vn/).

First, **install** dependencies by running `pip install -r requirements.txt`

Choose one of those methods:

## chrome **(most stable)**
> [Arguments References](https://peter.sh/experiments/chromium-command-line-switches/)

Modify `.env` accordingly to meet your requirements.

Explanation:
> `start_UIDs` is basically it. Same goes for `end_UIDs`
> 
> `log_lvl` idk...
> 
> `year`: Start from 1 to ?, 
> 
> For example, this year is 2022, so if you want to get the latest result, set it to 1, last year is 2, last 2 year is 3, and so on.
> 
> `semester`: 1 or 2
> 
> `write_uid` explain itself.

To save time, the UID range should be set from 3000350000 to 3000399999.

**DO NOT** use `add_argument("--headless")`, otherwise it won't able to interact with Chrome.

Check for missing UIDs: `python name_chrome.py`. It will check for any UIDs missing in `/collected/UIDs and names.txt` and save them as an array string in `/collected/missing.txt`.

You can modify the source code to read that array, or I will do it at the next update.



## fetch **(idk, help)**
> No docs.
## *img* **(abandoned, high error rate)**
> Default settings is for Windows 10, Taskbar put on top, 1366x768 screen reslution.