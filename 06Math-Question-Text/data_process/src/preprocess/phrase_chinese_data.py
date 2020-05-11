import xlrd
import xlutils.copy as copy
from bs4 import BeautifulSoup
import os
import time
import requests

chinese_path = './../../raw_data/语文-公共题库.xlsx'
chinese_target_path = './../../data_source/chinese_source0409.xls'

'''
解析语文题库文件中html标签
'''
def parser(src_path, tar_path, indexs=None):
    wb = xlrd.open_workbook(src_path)
    sheet = wb.sheets()[0]

    new_wb = copy.copy(wb)
    new_sheet = new_wb.get_sheet(0)
    img_id =0
    for i in range(1, sheet.nrows):
        row = sheet.row_values(i)
        for j in indexs:
            html = row[j]

            html = BeautifulSoup(html, 'html.parser')
            img_id = image_process(html,img_id)

            text = html.get_text()
            new_sheet.write(i, j, text)
    new_wb.save(tar_path)

# download image and replace img tag to image file name
def image_process(bs, img_id):
    stem_imgs = bs.find_all('img')
    if stem_imgs is not None:
        for img in stem_imgs:
            src = img['src']
            print(src)
            suffix = os.path.splitext(src)[1]

            name = 'img' + str(img_id) + suffix
            img_path = './../../img_data/chinese/' + name
            img.replace_with('__' + name)
            try:
                image = requests.get(src, timeout=15)
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue
            if '.png?' in img_path or '.jpg?' in img_path \
                    or '.jpeg?' in img_path or '.bmp?' in img_path or '.gif?' in img_path:
                img_path = img_path.split('?')[0]
            with open(img_path, mode='wb') as f:
               f.write(image.content)

            # print(os.path.splitext(src)[1])
            # print('image:', img_id)
            img_id += 1
    return img_id


if __name__ == '__main__':
    print(os.path.abspath('.'))
    print('start phrase...')
    # deal chinese
    parser(chinese_path, chinese_target_path, indexs=[2, 3, 4, 5, 17])
    print('end phrase. ')
    print('curr time: ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
