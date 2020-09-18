
1 download_data_from_mysql/qa_data_generator.py 从mysql数据库中下载问答数据
    生成的语文数据保存在cn_qa_data.txt

1.1 download_data_from_mysql/qa_data_generator.py 从mysql数据库中下载问答数据
    生成的数学数据保存在ma_qa_data.txt

2 data_procecss 数据预处理-语文部分
    1 generate_solr_csv_data.py生成double_teacher_ques_ans.csv数据
        格式 id,ques,ans,raw_title,raw_content,clean_title,clean_content
    2 生成问题数据double_teacher_question_data.csv
        格式 id   ques
    3 基于问题数据生成相似句子对及不相似句子对数据
        postive_pairs.csv
        negative_pairs.csv
    4 将数据存放在一个文件double_teacher_train_data.csv中并shuffle
        保存为bert_fine_tuning/data/train.csv dev.csv
        
2.1 ma_data_procecss 数据预处理-数学部分
    1 generate_solr_csv_data.py生成double_teacher_math_ques_ans.csv数据
        格式 id,ques,ans,raw_title,raw_content,clean_title,clean_content
    2 生成问题数据double_teacher_math_question.csv
        格式 id   ques
    3 基于问题数据生成相似句子对及不相似句子对数据
        postive_pairs.csv
        negative_pairs.csv
    4 将数据存放在一个文件double_teacher_train_data.csv中并shuffle
        保存为bert_fine_tuning/data/train.csv dev.csv
        
3 训练模型
    1 train model
        python3 run_classifier_moraldata.py --task_name=MAYI --do_train=true --do_eval=true --data_dir=$DATA_DIR --vocab_file=$BERT_BASE_DIR/vocab.txt --bert_config_file=$BERT_BASE_DIR/bert_config.json --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt --max_seq_length=128 --train_batch_size=32 --learning_rate=2e-5 --num_train_epochs=1.0 --output_dir=./model/moral_output/
    2 export model
        python3 run_classifier_moral_export.py --task_name=MAYI --do_train=False --do_eval=False --do_predict=True --data_dir=$DATA_DIR --vocab_file=$BERT_BASE_DIR/vocab.txt --bert_config_file=$BERT_BASE_DIR/bert_config.json --init_checkpoint=./model/moral_output/ --max_seq_length=128 --train_batch_size=32 --learning_rate=2e-5 --num_train_epochs=3.0 --output_dir=./model/moral_output/ --do_export=True --export_dir=exported
    
4 solr配置
    0 solr配置前停掉solr 服务 ./bin/solr stop -all
    1 复制solr7.4项目，该项目中已经配置ik分词器，solr查询字段为ques
    2 切换/usr/local/solr/solr-double-teacher-qa/bin
    3 创建solr cloud  ./bin/solr start -e cloud
        在创建过程中提示输入node1和node2端口号，分别设置为18993和17584
        运行过程中提示输入collection name ，这里我们输入 doubleteacher 然后回车
        运行中提示设置shards和replicas，我们都直接默认为2
        提示选择配置文件，这里也默认为_default
    4 到此solr cloud设置完成
    5 通过浏览器http://localhost-ip:18993/solr/
    6 上传数据 
        注意设置端口后，无法使用默认的端口，上传的post命令需要指定端口
        double_teacher_ques_ans.csv上传到solr/bin路径下，执行下面的命令，实现上传数据
        ./bin/post -p 18993 -c doubleteacher ./bin/double_teacher_ques_ans.csv
    7 查看验证上传26948条问答数据
    8 删除数据
        solr网页操作页面 documents/xml/
        <delete><query>*:*</query></delete><commit/>

4.1 solr_math配置
    1 复制solr7.4项目，该项目中已经配置ik分词器，solr查询字段为ques
    2 切换/usr/local/solr/solr-double-teacher-qa/bin
    3 创建solr cloud  ./bin/solr start -e cloud
        在创建过程中提示输入node1和node2端口号，分别设置为18993和17584
        运行过程中提示输入collection name ，这里我们输入 doubleteachermath2 然后回车
        运行中提示设置shards和replicas，我们都直接默认为2
        提示选择配置文件，这里也默认为_default
    4 到此solr cloud设置完成
    5 通过浏览器http://localhost-ip:18993/solr/
    6 上传数据 
        注意设置端口后，无法使用默认的端口，上传的post命令需要指定端口
        double_teacher_ques_ans.csv上传到solr/bin路径下，执行下面的命令，实现上传数据
        ./bin/post -p 18993 -c doubleteacher2 ./bin/double_teacher_math_ques_ans.csv
    7 查看验证上传26948条问答数据
    8 删除数据
        solr网页操作页面 documents/xml/
        <delete><query>*:*</query></delete><commit/>
    
    
5 chrome http request
    run: python3 qa_server.py
    # for chinese
        # local api test 
            # with solr+bert fine-tuning
            http://127.0.0.1:9090/chinese?query=%E8%A5%BF%E6%B8%B8%E8%AE%B0
            # with solr only
            http://127.0.0.1:9099/chinese/solr_only?query=ghajhgjkahgh%27GHDLkj
        # server api test
            # with solr+bert fine-tuning
            http://172.24.227.247:9099/chinese?query=朝花夕拾的内容
            # server api test with solr only
            http://172.24.227.247:9099/chinese/solr_only?query=朝花夕拾的内容
    # for math
        # local api test 
            # with solr+bert fine-tuning
            http://127.0.0.1:9090/math?query=%E8%A5%BF%E6%B8%B8%E8%AE%B0
            # with solr only
            http://127.0.0.1:9099/math/solr_only?query=ghajhgjkahgh%27GHDLkj
        # server api test
            # with solr+bert fine-tuning
            http://172.24.227.247:9099/math?query=怎么计算面积直角三角形
            # with solr only
            http://172.24.227.247:9099/math/solr_only?query=怎么计算面积直角三角形
        
        

