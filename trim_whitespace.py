from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import minify_html
from bs4 import BeautifulSoup
import json
import lxml
import lxml.html.clean as clean
import pandas as pd
from time import sleep
table_raw = '''<table>
    <tbody>
        <tr class=Dong_TieuDe>
            <td class=Cot_TieuDe style=width:20px;>STT</td>
            <td class=Cot_TieuDe>Tên môn học</td>
            <td class=Cot_TieuDe style=width:70px;>Đánh giá cuối kỳ 1</td>
            <td class=Cot_TieuDe colspan=4 style=width:200px;>Đánh giá thường xuyên</td>
            <td class=Cot_TieuDe colspan=1 style=width:50px;>Đánh giá giữa kỳ</td>
            <td class=Cot_TieuDe style=width:70px;>Đánh giá cuối kỳ</td>
            <td class=Cot_TieuDe style=width:70px;>ĐTB HK2</td>
            <td class=Cot_TieuDe style=width:70px;>TB Môn CN</td>
            <td class=Cot_TieuDe style=width:70px;>Đánh giá cả năm</td>
        </tr>
        <tr class=Dong_Chan onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this);
            onmouseover=Css_Mouse_ON(this);>
            <td align=center>1</td>
            <td>Toán</td>
            <td align=center>7.2</td>
            <td align=center style=width:50px;>8</td>
            <td align=center style=width:50px;>8</td>
            <td align=center style=width:50px;>9</td>
            <td align=center style=width:50px;>9</td>
            <td align=center style=width:50px;>9</td>
            <td align=center style=width:50px;>5.3</td>
            <td align=center>7.5</td>
            <td align=center>7.4</td>
            <td align=center>Khá</td>
        </tr>
        <tr class=Dong_Le onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this); onmouseover=Css_Mouse_ON(this);>
            <td align=center>2</td>
            <td>Vật lý</td>
            <td align=center>9.9</td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;>9</td>
            <td align=center style=width:50px;>10</td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;>8.5</td>
            <td align=center style=width:50px;>10</td>
            <td align=center>9.4</td>
            <td align=center>9.6</td>
            <td align=center>Giỏi</td>
        </tr>
        <tr class=Dong_Chan onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this);
            onmouseover=Css_Mouse_ON(this);>
            <td align=center>3</td>
            <td>Hóa học</td>
            <td align=center>7.7</td>
            <td align=center style=width:50px;>7</td>
            <td align=center style=width:50px;>6</td>
            <td align=center style=width:50px;>8</td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;>7</td>
            <td align=center style=width:50px;>8.5</td>
            <td align=center>7.6</td>
            <td align=center>7.6</td>
            <td align=center>Khá</td>
        </tr>
        <tr class=Dong_Le onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this); onmouseover=Css_Mouse_ON(this);>
            <td align=center>4</td>
            <td>Sinh học</td>
            <td align=center>7</td>
            <td align=center style=width:50px;>8</td>
            <td align=center style=width:50px;>7</td>
            <td align=center style=width:50px;>7</td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;>5</td>
            <td align=center style=width:50px;>7</td>
            <td align=center>6.6</td>
            <td align=center>6.7</td>
            <td align=center>Khá</td>
        </tr>
        <tr class=Dong_Chan onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this);
            onmouseover=Css_Mouse_ON(this);>
            <td align=center>5</td>
            <td>Ngữ văn</td>
            <td align=center>5.4</td>
            <td align=center style=width:50px;>6</td>
            <td align=center style=width:50px;>7</td>
            <td align=center style=width:50px;>7</td>
            <td align=center style=width:50px;>8</td>
            <td align=center style=width:50px;>4.8</td>
            <td align=center style=width:50px;>2</td>
            <td align=center>4.8</td>
            <td align=center>5</td>
            <td align=center>Trung bình</td>
        </tr>
        <tr class=Dong_Le onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this); onmouseover=Css_Mouse_ON(this);>
            <td align=center>6</td>
            <td>Lịch sử</td>
            <td align=center>7.4</td>
            <td align=center style=width:50px;>8</td>
            <td align=center style=width:50px;>9</td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;>7.5</td>
            <td align=center style=width:50px;>8.8</td>
            <td align=center>8.3</td>
            <td align=center>8</td>
            <td align=center>Giỏi</td>
        </tr>
        <tr class=Dong_Chan onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this);
            onmouseover=Css_Mouse_ON(this);>
            <td align=center>7</td>
            <td>Địa lý</td>
            <td align=center>7.9</td>
            <td align=center style=width:50px;>7</td>
            <td align=center style=width:50px;>6</td>
            <td align=center style=width:50px;>8</td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;>7.5</td>
            <td align=center style=width:50px;>8.5</td>
            <td align=center>7.7</td>
            <td align=center>7.8</td>
            <td align=center>Khá</td>
        </tr>
        <tr class=Dong_Le onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this); onmouseover=Css_Mouse_ON(this);>
            <td align=center>8</td>
            <td>Tiếng Anh</td>
            <td align=center>5.8</td>
            <td align=center style=width:50px;>4</td>
            <td align=center style=width:50px;>4</td>
            <td align=center style=width:50px;>6</td>
            <td align=center style=width:50px;>6</td>
            <td align=center style=width:50px;>7.3</td>
            <td align=center style=width:50px;>7</td>
            <td align=center>6.2</td>
            <td align=center>6.1</td>
            <td align=center>Trung bình</td>
        </tr>
        <tr class=Dong_Chan onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this);
            onmouseover=Css_Mouse_ON(this);>
            <td align=center>9</td>
            <td>Công nghệ</td>
            <td align=center>6.9</td>
            <td align=center style=width:50px;>10</td>
            <td align=center style=width:50px;>6</td>
            <td align=center style=width:50px;>8</td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;>7.5</td>
            <td align=center style=width:50px;>6.5</td>
            <td align=center>7.3</td>
            <td align=center>7.2</td>
            <td align=center>Khá</td>
        </tr>
        <tr class=Dong_Le onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this); onmouseover=Css_Mouse_ON(this);>
            <td align=center>10</td>
            <td>Âm nhạc</td>
            <td align=center>Đ</td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center></td>
            <td align=center></td>
            <td align=center>Đ</td>
        </tr>
        <tr class=Dong_Chan onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this);
            onmouseover=Css_Mouse_ON(this);>
            <td align=center>11</td>
            <td>Mỹ thuật</td>
            <td align=center>Đ</td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center></td>
            <td align=center></td>
            <td align=center>Đ</td>
        </tr>
        <tr class=Dong_Le onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this); onmouseover=Css_Mouse_ON(this);>
            <td align=center>12</td>
            <td>Thể dục</td>
            <td align=center>Đ</td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;></td>
            <td align=center></td>
            <td align=center></td>
            <td align=center>Đ</td>
        </tr>
        <tr class=Dong_Chan onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this);
            onmouseover=Css_Mouse_ON(this);>
            <td align=center>13</td>
            <td>Tin học</td>
            <td align=center>9.1</td>
            <td align=center style=width:50px;>10</td>
            <td align=center style=width:50px;>8</td>
            <td align=center style=width:50px;>10</td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;>10</td>
            <td align=center style=width:50px;>10</td>
            <td align=center>9.8</td>
            <td align=center>9.6</td>
            <td align=center>Giỏi</td>
        </tr>
        <tr class=Dong_Le onclick=SetCssDongChon(this); onmouseout=Css_Mouse_OUT(this); onmouseover=Css_Mouse_ON(this);>
            <td align=center>14</td>
            <td>Giáo dục công dân</td>
            <td align=center>7.2</td>
            <td align=center style=width:50px;>7</td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;>6</td>
            <td align=center style=width:50px;></td>
            <td align=center style=width:50px;>5</td>
            <td align=center style=width:50px;>5</td>
            <td align=center>5.4</td>
            <td align=center>6</td>
            <td align=center>Trung bình</td>
        </tr>
    </tbody>
</table>'''
# Ignore common attrib maybe ? https://stackoverflow.com/questions/7470333/remove-certain-attributes-from-html-tags
cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=frozenset({'colspan'}))
table_raw = cleaner.clean_html(table_raw) # Removed all attrib.

table = BeautifulSoup(table_raw, "lxml")

table_head = table.tr.extract()
table_head.name = "thead"
for elem in table_head.find_all("td"): elem.name = "th" # Replace all td with th

table_body = table.tbody.extract()
table.table.append(table_head)
table.table.append(table_body)

df = pd.read_html(str(table))
with open("./collected/3000377451.json", "w", encoding="utf-8") as f:
    f.write(df[0].to_json(orient='records', force_ascii=False))
    f.close()