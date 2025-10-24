#  五笔码表助手同步服务端 Django 版 

本项目是[五笔码表助手 for Rime](https://github.com/KyleBing/wubi-dict-editor) [后台](https://github.com/KyleBing/portal) 的 Django 实现，只包含了五笔字典同步和用户注册/登录功能。感谢原作者[KyleBing](https://github.com/KyleBing)

## 快速开始

### 快速部署 (推荐)

这是最简单快捷的部署方式，使用预构建的 Docker 镜像，适合生产环境和快速部署。

1. 创建项目目录：
   ```bash
   mkdir wubi-dict-sync && cd wubi-dict-sync
   ```

2. 创建 `docker-compose.yml` 文件：
   ```yaml
   version: '3.8'

   services:
     db:
       image: postgres:16-alpine
       volumes:
         - postgres_data:/var/lib/postgresql/data/
       environment:
         - POSTGRES_DB=${POSTGRES_DB:-wubi_dict_sync_db}
         - POSTGRES_USER=${POSTGRES_USER:-wubi_user}
         - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-wubi_password}
       ports:
         - "${POSTGRES_PORT:-5434}:5432"

     wubi-dict-sync:
       image: flyinke/wubi-dict-sync:latest
       ports:
         - "${APP_PORT:-8002}:8000"
       environment:
         - SECRET_KEY=${SECRET_KEY:-django-insecure-fallback-key-for-development}
         - DEBUG=${DEBUG:-0}
         - DATABASE_URL=${DATABASE_URL:-postgresql://${POSTGRES_USER:-wubi_user}:${POSTGRES_PASSWORD:-wubi_password}@${DB_HOST:-db}:${DB_PORT:-5432}/${POSTGRES_DB:-wubi_dict_sync_db}}
         - DB_HOST=${DB_HOST:-db}
         - DB_PORT=${DB_PORT:-5432}
       env_file:
         - .env
       depends_on:
         - db

   volumes:
     postgres_data:
   ```

3. 创建 `.env` 文件：
   ```bash
   # 数据库配置
   POSTGRES_DB=wubi_dict_sync_db
   POSTGRES_USER=wubi_user
   POSTGRES_PASSWORD=your-strong-password-here
   POSTGRES_PORT=5434

   # Django 配置
   SECRET_KEY=your-secret-key-here-change-this-in-production
   DEBUG=0
   DATABASE_URL=postgresql://wubi_user:your-strong-password-here@db:5432/wubi_dict_sync_db

   # 应用配置
   DB_HOST=db
   DB_PORT=5432
   APP_PORT=8002
   ```

4. 启动服务：
   ```bash
   docker compose up -d
   ```

5. 访问应用：
   - API: http://localhost:8002/api/
   - Admin: http://localhost:8002/admin/

#### Docker Compose 常用命令

```bash
# 查看服务状态
docker compose ps

# 查看日志
docker compose logs wubi-dict-sync
docker compose logs db

# 重启服务
docker compose restart wubi-dict-sync

# 停止服务
docker compose down

# 重新构建并启动
docker compose up --build -d

# 进入容器
docker compose exec wubi-dict-sync bash

# 执行 Django 命令
docker compose exec wubi-dict-sync python manage.py createsuperuser
```

### 开发环境启动

适合二次开发和调试，支持热重载和实时修改。

> **注意**: 只有在需要进行二次开发时才需要克隆仓库。如果只是使用服务，请使用上面的快速部署方式。

#### 方式一：使用 Docker Compose 开发版本

1. 克隆仓库：
   ```bash
   git clone https://github.com/flyinke/wubi-dict-sync.git
   cd wubi-dict-sync
   ```

2. 配置环境变量：
   ```bash
   # 复制环境变量模板
   cp .env.example .env
   
   # 编辑配置文件（可选）
   nano .env
   ```

3. 启动开发服务：
   ```bash
   docker compose up -d
   ```

4. 访问应用：
   - API: http://localhost:8002/api/
   - Admin: http://localhost:8002/admin/

#### 方式二：本地开发环境

这种方式不需要 Docker，会自动使用 `SQLite` 数据库。

1. 克隆仓库：
   ```bash
   git clone https://github.com/flyinke/wubi-dict-sync.git
   cd wubi-dict-sync
   ```

2. 创建虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate    # Windows
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 运行数据库迁移：
   ```bash
   python manage.py migrate
   ```

5. 启动开发服务器：
   ```bash
   python manage.py runserver
   ```

#### 开发环境常用命令

```bash
# 创建超级用户
python manage.py createsuperuser

# 查看数据库迁移状态
python manage.py showmigrations

# 运行测试
python manage.py test

# 查看 Django shell
python manage.py shell

# 检查项目配置
python manage.py check
```

## Docker 镜像

本项目提供预构建的 Docker 镜像，支持从以下注册表获取：

- **Docker Hub**: `flyinke/wubi-dict-sync:latest`
- **GitHub Container Registry**: `ghcr.io/flyinke/wubi-dict-sync:latest`

> **推荐**: 使用上面的快速部署方式，它已经包含了完整的 docker-compose.yml 配置。如果您需要自定义部署，可以参考 [部署指南](DEPLOYMENT.md)。

## 使用

可用的 API 接口如下：

*   `POST /api/user/register`
*   `POST /api/user/login`
*   `GET /api/dict/pull`
*   `PUT /api/dict/push`

### 用户注册

要注册新用户，请向 `/api/user/register` 发送 `POST` 请求，请求体如下：

```json
{
    "nickname": "你的昵称",
    "email": "your-email@example.com",
    "password": "你的密码"
}
```

### 用户登录

要登录，请向 `/api/user/login` 发送 `POST` 请求，请求体如下：

```json
{
    "email": "your-email@example.com",
    "password": "你的密码"
}
```

### 推送字典

要推送字典，请向 `/api/dict/push` 发送 `PUT` 请求，请求体如下：

```json
{
    "title": "你的字典标题",
    "content": "你的字典内容",
    "content_size": 123,
    "word_count": 456
}
```

### 拉取字典

要拉取字典，请向 `/api/dict/pull?title=你的字典标题` 发送 `GET` 请求。
