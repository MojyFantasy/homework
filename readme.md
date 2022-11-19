# 项目运行及部署

## 准备工作

```text
Python >= 3.7.0
Mysql >= 5.7.0 (可选，默认数据库sqlite3)
```

## 运行预览

### 下载代码

- 通过 `git clone https://github.com/MojyFantasy/homework.git` 下载到工作目录

### 本地运行

1. 进入项目目录:`cd backend `
2. 在项目根目录中，复制 `.env.example` 文件另存为 `.env`，重命名为`.env`
3. 在 `.env` 中配置数据库信息(默认数据库为sqlite3，如果使用MySQL数据库，则只需要将`.env`中的sqlite相关的`DATABASE_ENGINE`和`DATABASE_NAME`配置注释掉，然后将MySQL的`DATABASE_ENGINE`和`DATABASE_NAME`取消注释即可)
4. 安装依赖环境: `pip3 install -r requirements.txt`，也可以使用pipenv包管理工具安装依赖环境，命令：`pipenv install`
5. 执行迁移命令: `python manage.py makemigrations` `python manage.py migrate`
6. 初始化数据: `python manage.py init`，初始化后，系统为默认创建一个超级用户和一个测试的普通用户。
7. 启动项目: `python manage.py runserver 0.0.0.0:8000`

### 访问项目

- API 请求入口：http://127.0.0.1:8000/api/1.0/
- API文档地址：http://127.0.0.1:8000/api/redoc/
- API文档地址（swagger）：http://127.0.0.1:8000/api/swagger/
- 系统默认创建的管理员账号：`admin` 密码：`admin`
- 系统默认创建的普通用户账号：`test_user` 密码：`test_user`

# 环境部署

## docker-compose一键部署

### 构建

```text
# 先安装docker-compose (自行百度安装)
# 通过 `git clone https://github.com/MojyFantasy/homework.git` 下载到工作目录，执行此命令等待安装
docker-compose up -d
docker exec -it homework-web-1 /bin/bash start.sh
```

### 访问项目

- 访问地址：http://localhost:8000
- 账号：`admin`密码：`admin`

