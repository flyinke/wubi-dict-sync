#  五笔码表助手同步服务端 Django 版 

本项目是[五笔码表助手 for Rime](https://github.com/KyleBing/wubi-dict-editor) [后台](https://github.com/KyleBing/portal) 的 Django 实现，只包含了五笔字典同步和用户注册/登录功能。感谢原作者[KyleBing](https://github.com/KyleBing)

## 快速开始

### 使用 Docker (推荐)

1. 克隆仓库：
   ```bash
   git clone https://github.com/flyinke/wubi-dict-sync.git
   cd wubi-dict-sync
   ```

2. 使用 Docker Compose 启动：
   ```bash
   docker compose up -d
   ```

3. 访问应用：
   - API: http://localhost:8002/api/
   - Admin: http://localhost:8002/admin/

### 手动安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/flyinke/wubi-dict-sync.git
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行迁移：
   ```bash
   python manage.py migrate
   ```

4. 启动开发服务器：
   ```bash
   python manage.py runserver
   ```

## Docker 镜像

### 从 Docker Hub 拉取镜像

```bash
docker pull flyinke/wubi-dict-sync:latest
```

### 从 GitHub Container Registry 拉取镜像

```bash
docker pull ghcr.io/flyinke/wubi-dict-sync:latest
```

### 运行容器

**使用 Docker Hub 镜像:**
```bash
docker run -d \
  --name wubi-dict-sync \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:password@host:port/dbname" \
  flyinke/wubi-dict-sync:latest
```

**使用 GitHub Container Registry 镜像:**
```bash
docker run -d \
  --name wubi-dict-sync \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:password@host:port/dbname" \
  ghcr.io/flyinke/wubi-dict-sync:latest
```

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
