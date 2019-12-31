
###本项目用于案例数据的多分类模型
## data_clean部分
主要处理标注数据存在的一些纠正工作，某些维度会对分类结果造成扰动，导致准确度下降
有些分类数据，X一样，但Y不一致，对其重新处理


##1 demo部分
将案例原因归结为5种不同的心理缺失问题，即多分类类别为5类
##2 pro部分
将案例原因标注为12种不同的需求缺失类别，即多分类类别为12类

# 数据清理
preprocess将数据从表格中读取处理为用于多分类的one hot表示

## 多分类器
\multi-classifier\multi_classifier_demo\run_single_multiclassify.py
\multi-classifier\multi_classifier_demo\run_ensemble_multiclassify.py
分别使用单一分类器及集成学习分类器对数据做多分类，其中单一分类器LR, KNN, DT, SVM, NB五种
集成学习四种 AdaBoost, BaggingClassifier, GradientBoosting, RF, 其中AdaBoost, BaggingClassifier的基分类器分别为LR, NB, DT, SVM

##todo 多分类器默认参数，调参需要继续处理


##结果分析
数据处理中将10%作为test set
对于剩余的train set 每次分别选50%， 60% 70% 80% 90%来训练分类器，比较结果
每个分类器运行10次求平均值
生成的结果保存在multi-classifier-55.txt等文件中
通过single-classifier-result-save-excel.py将对应的Precision Recall F1-score Accuracy_score 结果保存在对应的表格中

##Features_Impact
目前共有19个维度的信息，依次每次去除其中一个维度的信息，选用以上其中一种分类器算法，对其做多分类
结果保存在data50.xlsx等
对于结果按照Precision的升序做排序，比较分析那个因素去除后对分类精度的影响最小，排在越前面一般表明对结果的影响最大

