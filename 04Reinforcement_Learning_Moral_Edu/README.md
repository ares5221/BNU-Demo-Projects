# Reinforcement_Learning_Moral_Edu
项目介绍：
  基于强化学习实现的问答系统实验
  1，安装
  git clone https://github.com/ares5221/Reinforcement_Learning_Moral_Edu.git

  cd /Reinforcement_Learning_Moral_Edu/Moral_Edu_RL

2运行实验
  若os为win可以运行win版本，否则运行linux版本，可以按照自己的需求修改具体文件路径
  python .\src\dialogue_system\run\run_experment_Windows82.py

3，通过设置不同的参数，比较不同参数下实验结果的不同
  实验结果会保存在./src/data文件中test.txt文件中，结果参考success rate 及average rewards, average turns 
  对于结果的处理统计参考.\src\ProcessResultData
  主要可以比较在设置不同的dqn hidden units 在8，16， 32， 64， 128， 256的情况下，不同train。test切分比例中64的效果最好
  比较reward for fail与reward for success的比值在2.0：1.0时候效果较好 3d柱状图展示
  此外还有max turn在30， 50， 100， 150时候50较合适等实验



4, 随着实验的次数增加，learning curve的变化可以通过.\src\dialogue_system\model\dqn\learning_rate04中保存的数据来得到
  将该结果保存后，画出曲线变化及与对比实验random及rule的对比图 .\src\ProcessResultData\draw_learning_curve_result
  为了使得曲线更平滑，可以多跑几次实验，求平均
  实验过程中，训练生成的模型信息会保存在.\src\dialogue_system\model\dqn\model中

 

5，对于对比实验random ，rule
  random的区别在于 agent直接从action space中随机一个状态作为next的操作，效果是最差的，低于rule
  rule通过全部数据的统计结果生成一些规则，agent根据当前state判断那个结果是最可能的，然后从最可能结果的没被问到的slot中选择一个
  在运行random时候，修改agent_id = 3, save_model = 0, warm_start = 0,没有生成模型不需要保存，也没有warm start
  在运行rule时候，修改agent_id = 0, save_model = 0, warm_start = 0,没有生成模型不需要保存，也没有warm start,其规则的统计来自数据中的disease_symptom



6，作为baseline的实验是分类器的实验
  这里用了各种机器学习的分类器.\src\multi-classifier