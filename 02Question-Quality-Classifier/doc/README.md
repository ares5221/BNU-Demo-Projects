
1,第一步 通过docx文档生成用于分类的数据
将质量较好的问题的docx文本 放到\Question-Quality-Classifier\data\data_origin\good_docx
将质量较差的问题的docx文本 放到\Question-Quality-Classifier\data\data_origin\bad_docx
执行\Question-Quality-Classifier\src\step1_process_data.py
在\Question-Quality-Classifier\data\data_clean 中生成可查看的json格式数据

2，第二步 通过json 生成用于分类器训练的数据
执行 \Question-Quality-Classifier\src\step2_process_train_data.py
在 Question-Quality-Classifier\data\train_data 中生成用于训练模型的数据
共40条数据，20条正例 20条负例
在过程中对学科信息编码，对问题等内容通过BERT encoding， 然后拼接向量，
最后保存数据

3，第三步 通过mlp训练分类模型
执行 Question-Quality-Classifier\src\step3_question_quality_classifier.py
可设置训练参数，测试数据与训练数据相同
输出训练过程及显示训练过程曲线

