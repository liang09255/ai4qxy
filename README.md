# ai4qxy

## 环境配置
1. 安装python开发环境及ide 

    python==3.12.*, 推荐使用pycharm, 有社区免费版，也可使用自己熟悉的ide

2. 安装包管理工具pdm

    `pip install pdm==2.10.4`

3. 安装依赖包

    `pdm install`

4. docker部署milvus向量数据库，没docker的可以到时候远程连其他人的数据库

    `docker-compose up -d`

## 检查配置是否成功

1. 检查mivlus是否安装成功

    网页打开attu可视化界面，连接19530端口的数据库，连接成功即可

2. 检查部分依赖包是否安装成功
   
   * 找我拿key填到src/init.py
   * 尝试在src目录下运行 `pdm run python 1.py`
   
Tips: 依赖项安装可能比较麻烦且耗时，建议提前尝试安装，有遇到报错等问题截图给我，可能在周二晚24时后回复
