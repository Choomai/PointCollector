# Point Collector

First, **install** dependencies by running `pip install -r requirements.txt`

#
## **ctt_chrome**

### Fetch at [Sở GD&DT TTH | Cổng thông tin đào tạo](https://qlttgddt.thuathienhue.edu.vn/)

Modify `.env` accordingly to meet your requirements.

Explanation:
> `ctt_start_UID` is basically it. Same goes for `ctt_end_UID`
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

Check for missing UIDs: `python name_chrome.py`. It will check for any UIDs missing in `collected/ctt/UIDs and names.txt` and save them as an array string in `collected/ctt/missing.txt`.
#
## **ts10_fetch**

### Fetch at [Tuyển sinh lớp 10](http://http://khaothi.thuathienhue.edu.vn:8080/)

Modify `.env` accordingly to meet your requirements.

Explanation:
> `ts10_start_ID` is basically it. Same goes for `ts10_end_ID`

### You can combine all JSON file using: `combine_json.py`

This script supported 2 format, JSON and CSV. When typing the path, make sure it doesn't have any `/` at the end.

# Disclaimer

The PointCollector repo contains python scripts that fetch student point reports from websites. The author does not own or guarantee the data or the scripts.

The use of these scripts is at your own risk. You should respect the websites and the laws when you crawl. The author is not liable for any damages or losses from these scripts.