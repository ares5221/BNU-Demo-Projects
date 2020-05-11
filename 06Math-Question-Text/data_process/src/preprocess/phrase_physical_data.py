import os.path
import xlrd
import xlutils.copy
import requests
from bs4 import BeautifulSoup

import os
import time

physical_path = './../../raw_data/物理公共题库.xlsx'
physical_target_path = './../../data_source/physical_source0422.xls'
'''
解析物理题库文件中html标签
'''


def process(src_path, tar_path):
    wb = xlrd.open_workbook(src_path)
    table = wb.sheets()[0]

    new_wb = xlutils.copy.copy(wb)
    new_table = new_wb.get_sheet(0)

    img_id = 0

    for i in range(2, table.nrows):
        row = table.row_values(i)
        stem = row[2]
        item = row[3]
        sub_item = row[4]
        answer = row[5]

        bs_stem = BeautifulSoup(stem, 'html.parser')
        bs_item = BeautifulSoup(item, 'html.parser')
        bs_sub_item = BeautifulSoup(sub_item, 'html.parser')
        bs_answer = BeautifulSoup(answer, 'html.parser')

        # stem = bs_stem.get_text()
        # print(stem)

        img_id = image_process(bs_stem, img_id)
        img_id = image_process(bs_item, img_id)
        img_id = image_process(bs_sub_item, img_id)
        img_id = image_process(bs_answer, img_id)

        stem = bs_stem.get_text()
        item = bs_item.get_text()
        sub_item = bs_sub_item.get_text()
        answer = bs_answer.get_text()

        # print(stem)

        new_table.write(i, 2, stem)
        new_table.write(i, 3, item)
        new_table.write(i, 4, sub_item)
        new_table.write(i, 5, answer)

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
            img_path = './../../img_data/physical/' + name
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
                    or '.jpeg?' in img_path or '.bmp?' in img_path or '.gif?' in img_path or '.PNG?' in img_path:
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
    # deal math
    process(physical_path, physical_target_path)
    print('end phrase. ')
    print('curr time: ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
