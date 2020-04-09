

项目介绍：
一、 数据处理部分

1，获取到未处理的原始题库数据文件存储在raw_data,
通过src/preprocess/phrase_chinese_data.py处理语文后，
通过src/preprocess/phrase_math_data.py处理数学后，
生成data_source中文件

2，将data_source中的数据进一步处理，通过src/preprocess/split.py区分其中套题或者id为空等情况，
将便于处理的存储在data_split中对应表格文件的 正常 sheet中

3，将data_split中的数据分别通过preprocess文件处理，生成的结果存放在data/preprocess_result_xxx/中
按照题目类型存放在不同的csv文件中