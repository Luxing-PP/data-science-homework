# 数据科学大作业

协同工具：Gitee

懒得更新这个了，助教可以当README不存在

## PartA——数据获取

1. 数据源分类（是随便选个API爬下来就行吗？）

- 央媒(详见下文)
- 自媒体 （微博微信，打算甩锅给**阿伟**）【**TODO** 反正我还没做】
- 新闻平台API: 
  - 筛选 新闻来源来 获取央媒 (**可行性 CHECK**)



[TODO] 定义重点新闻（指评论量远超（考虑数据分布）其它新闻的新闻） 都没什么评论= =

[TODO] 找一个新闻平台评论的替代品（知乎？）



2. 内容

- 标题 内容（**CHECK**）
- **时间戳分析（分成不同阶段）** （CHECK）
- **来源分类**（CHECK）
- 迭代查找 （新浪和荔枝 **CHECK**）

- 评论：爬下来的评论抽象成vector（time,emotion1,emotion2,...,emotion n）（n+1维向量）
  - **TODO**：我爬不到评论= =，根本就没有哪个新闻平台有多少评论咋办
  - 问题A：如果只有四个阶段，那数据分布是不是不太适合直角坐标系，所以用极坐标
    - （呆滞：还没学机器学习听不懂，不过我数据库做成能保留到月日的时间了）



3. 具体数据获取

- 新浪API CHECK 【目前主要使用】
- 荔枝API CHECK 【弃用】



已实现基本自动化



--> PPT 10页以后内容

## **数据库存储：**

- 目前

  表 “url” ： 		 
  ![url](https://images.gitee.com/uploads/images/2020/1225/210253_74154c36_7410521.png "Snipaste_2020-12-25_21-02-19.png")

  表"eLexicon":  
  ![eLexicon](https://images.gitee.com/uploads/images/2020/1225/210408_c2d2f0a8_7410521.png "Snipaste_2020-12-25_21-03-34.png")
  
  表"comments"：
  ![comments](https://images.gitee.com/uploads/images/2020/1225/210643_78caadf1_7410521.png "Snipaste_2020-12-25_21-06-01.png")

- 需求（**TODO** 你们填格式同上我能看懂就行DOGE）：


## 机器学习分析：

### 心态词典：

- 直接使用**NRC词语情绪词典**

- 原始TXT处理成CSV格式后导入表“eLexicon”待用

  

问题：数据库->机器学习（什么接口，怎么把这些数据放到机器学习迭代程序里面）  

神经网络（感觉不至于用到神经网络），机器学习开源库（pandas，scipy（好像是），numpy（线性代数相关），tensorflow（这个用起来爽啊））

- 具体检验：
  - 提取出频率最高的心态词与心态词典**碰撞**——作为主体思想评估的标准



- 自动打标签？？？
- 最后一步，把数据水成PPT
- HanLP 拆解词汇
- 打标签：词频，向量夹角（还是单纯的0 1 标识有无此情绪，那词频（特征词语出现次数/总词语数）勉强作为情绪强度的度量应该是可以的），所谓情绪词典【芜湖】
- 问题：情绪词典这东西怎么得到呢...【**TODO**】
- 数据集划分——训练集：预测集：验证集=6：3：1（大概）
- 取决于多少个维度的情绪，machine learning or deep learning ，参数选取，调优化方法，降维，主成分分析...（回去好好看书，复习这部分代码和知识）



## 水报告：

【TODO】

数据量级 

3.10 前 （KEY）  30%不到占比

836 篇  5W 评论[ 每阶段100+，安啦]



3.10-6.1 （一堆）

新闻应该是6K+

评论大概是25W+



以上部分都没筛选



PS：{还有一些一开始因为超时没爬的LOG，我看数据溢出了就懒得再筛查了= =}

| 任务\人 | 呆滞 | 阿伟 | 劼哥哥 |
| ------- | ---- | ---- | ------ |
| 爬      | 2/3  | 1/3  | 0      |
| 库      | 1/3  | 1/3  | 1/3    |
| 机      | 0    | 1/3  | 2/3    |



[1]: http://sentiment.nrc.ca/lexicons-for-research/ [1]Saif, Mohammad. "Colourful Language: Measuring Word-Colour Associations, 2011a." In Proceedings of the ACL 2011 Workshop on Cognitive Modeling and Computational Linguistics (CMCL). 2011. [2]Mohammad, Saif M., and Peter D. Turney. "Crowdsourcing a word–emotion association lexicon." Computational Intelligence 29, no. 3 (2013): 436-465.