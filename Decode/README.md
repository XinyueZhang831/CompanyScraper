# Decode

### Request .ttf files
 According to the links from the csv file, download new .ttf file.
 
### Convert .ttf to .xml
 Find the relationship between the encoded data and real data.
 
### Create Dictionary
 Change the data from the .csv file.
 
# Logic:
![TTF file](/Decode/WX20200822-143046@2x.png)

Font editor from Baidu.com can help to find the logic inside the ttf file, check [Font Editor](http://fontstore.baidu.com/static/editor/)

![CSV file](/Decode/WX20200822-143158@2x.png)

It is easy to see that 1884-87-70 is not the real time. The numbers in 1884-87-70 is the small size number under each box, and the real number should be in the box.

Real (2006-01-18): 0-1-2-4-5-6-7-8-9

Fake (1884-87-70): 8-7-1-6-2-4-9-0-5

So the real data should be 2006-01-18.

There is no 3 in both lines, so 3 is not encoded in the tff file.

 
## Author:
 Xinyue Zhang

