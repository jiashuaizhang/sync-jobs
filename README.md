[TOC]

# 数据同步工具
> mysql表级全量同步 / mongodb全量+增量同步 / redis全量+增量同步

## 方案说明

### MySql同步

#### 方案概述

基于[addax](https://wgzhao.github.io/Addax/latest/),并使用python程序调度。当前仅支持表级全量同步。

#### 配置说明

编辑配置文件`sync-jobs\config\application.properties`,修改以下配置项:

```properties
# 同步周期，单位: 分钟
sync.interval=10

# 源数据库地址，jdbc格式
mysql.0.url=jdbc:mysql://127.0.0.1:2206/perceive?useUnicode=true&characterEncoding=UTF-8
# 源数据库用户名
mysql.0.username=root
# 源数据库密码
mysql.0.password=xxxxx

# 目的数据库地址，jdbc格式
mysql.1.url=jdbc:mysql://127.0.0.1:5506/perceive?useUnicode=true&characterEncoding=UTF-8
# 目的数据库用户名
mysql.1.username=root
# 目的数据库密码
mysql.1.password=xxxxx

# 需要同步的表，','分隔
mysql.sync.tables=iot_target,iot_alarm_fence,iot_alarm_model
```

项目中addax的job配置文件模板地址`sync-jobs\config\mysql\mysql2mysql.json`，其他配置参考: 

[mysql reader](https://wgzhao.github.io/Addax/latest/reader/mysqlreader/)

[mysql writer](https://wgzhao.github.io/Addax/latest/writer/mysqlwriter/)

### MongoDB同步

#### 方案概述

基于[mongo-shake](https://github.com/alibaba/MongoShake)，支持数据库实例级全量+增量同步。

#### 配置说明

编辑配置文件`sync-jobs\docker\mongo-shake.conf`,修改以下配置项:

```properties
# 源数据库地址，与mongo shell格式相同
# 单节点：mongodb://username1:password1@host
# 副本集：mongodb://username1:password1@primaryA,secondaryB,secondaryC
# 分片集：mongodb://username1:password1@primaryA,secondaryB,secondaryC;mongodb://username2:password2@primaryX,secondaryY,secondaryZ
mongo_urls = mongodb://admin:xxxxxxxxxx@127.0.0.1:27018,127.0.0.1:27019

# 目的数据库地址，格式与mongo_urls对齐。
tunnel.address = mongodb://root:xxxxxx@127.0.0.1:27019

# 同步模式，all表示全量+增量同步，full表示全量同步，incr表示增量同步。
sync_mode = all
```

完整配置参考: [mongo-shake wiki](https://github.com/alibaba/MongoShake/wiki/%E9%85%8D%E7%BD%AE%E5%8F%82%E6%95%B0%E8%AF%B4%E6%98%8E)

### Redis同步

#### 方案概述

基于[redis-shake](https://github.com/tair-opensource/RedisShake)，支持数据库实例级全量+增量同步。

#### 配置说明

编辑配置文件`sync-jobs\docker\redis-shake.toml`,修改以下配置项:

```toml
# 源地址
[sync_reader]
cluster = true # 是否为集群模式
address = "127.0.0.1:8001" # 如果是集群，填写其中任意一个节点地址
password = "XXXX" # 访问密码

# 目的
[redis_writer]
cluster = false            # 是否为集群模式
sentinel = false           # 是否为哨兵
master = ""                # 如果是哨兵，填写哨兵监听的master名称
address = "127.0.0.1:8639" # 如果是集群，填写其中任意一个节点地址
password = "XXXX" # 访问密码
```
完整配置参考: [redis-shake config](https://tair-opensource.github.io/RedisShake/zh/guide/config.html)

## 启动同步服务

### 文件准备

1. 将docker目录中的`docker-compose.yml`、`mongo-shake.conf`、`redis-shake.toml`上传到服务器同一目录；
2. 执行以下命令，映射容器内配置文件到宿主机(注意容器tag是否最新): 
	```shell
	docker run --rm -v `pwd`/sync-jobs:/opt/sync-jobs -e SYNC=0 harbor.cuscri.com/tools/sync-jobs:1.0.1
	```

	执行成功后在当前目录会生成`sync-jobs`目录，其中包含python脚本和配置文件；

3. 按照**配置说明**修改必要配置信息。

### 启动服务

使用`docker-compose up -d`启动服务，查看容器日志和目的端数据同步情况。
