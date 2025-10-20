# 部署指南

## 发布到 GitHub Container Registry (GHCR) 和 Docker Hub

### 1. 准备工作

#### 1.1 在 Docker Hub 创建仓库
1. 访问 [Docker Hub](https://hub.docker.com/)
2. 登录您的账户
3. 点击 "Create Repository"
4. 仓库名称：`wubi-dict-sync`
5. 设置为公开或私有（根据需求）

#### 1.2 配置 GitHub Secrets
在您的 GitHub 仓库中配置以下 secrets：

1. 进入 GitHub 仓库 → Settings → Secrets and variables → Actions
2. 添加以下 secrets：
   - `DOCKERHUB_USERNAME`: 您的 Docker Hub 用户名
   - `DOCKERHUB_TOKEN`: 您的 Docker Hub 访问令牌

**注意**: GitHub Container Registry (GHCR) 使用 GitHub 的自动生成的 `GITHUB_TOKEN`，无需额外配置。

#### 1.3 获取 Docker Hub Token
1. 登录 Docker Hub
2. 进入 Account Settings → Security
3. 点击 "New Access Token"
4. 设置权限为 "Read, Write, Delete"
5. 复制生成的 token

#### 1.4 GitHub Container Registry 配置
GitHub Container Registry 会自动使用以下配置：
- **Registry URL**: `ghcr.io`
- **用户名**: 您的 GitHub 用户名
- **Token**: 自动使用 `GITHUB_TOKEN`（无需手动配置）

### 2. 自动发布流程

当您推送代码到 GitHub 时，GitHub Actions 会自动：

1. **构建 Docker 镜像**：支持多架构（amd64, arm64）
2. **推送到两个注册表**：
   - GitHub Container Registry (GHCR)
   - Docker Hub
3. **自动打标签**：为两个注册表应用相同的标签
4. **缓存优化**：使用 GitHub Actions 缓存加速构建

#### 2.1 触发条件
- 推送到 `main` 或 `master` 分支
- 创建版本标签（如 `v1.0.0`）
- 创建 Pull Request

#### 2.2 自动标签
- `latest`：主分支的最新版本
- `v1.0.0`：版本标签
- `v1.0`：主版本标签
- `main`：分支名称标签

#### 2.3 镜像地址
发布后，镜像将在以下地址可用：

**GitHub Container Registry:**
- `ghcr.io/flyinke/wubi-dict-sync:latest`
- `ghcr.io/flyinke/wubi-dict-sync:v1.0.0`

**Docker Hub:**
- `flyinke/wubi-dict-sync:latest`
- `flyinke/wubi-dict-sync:v1.0.0`

### 3. 手动发布

#### 3.1 本地构建和推送到 Docker Hub
```bash
# 构建镜像
docker build -t flyinke/wubi-dict-sync:latest .

# 登录 Docker Hub
docker login

# 推送镜像到 Docker Hub
docker push flyinke/wubi-dict-sync:latest
```

#### 3.2 本地构建和推送到 GitHub Container Registry
```bash
# 构建镜像
docker build -t ghcr.io/flyinke/wubi-dict-sync:latest .

# 登录 GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u flyinke --password-stdin

# 推送镜像到 GHCR
docker push ghcr.io/flyinke/wubi-dict-sync:latest
```

#### 3.3 多架构构建（同时推送到两个注册表）
```bash
# 创建构建器
docker buildx create --name multiarch --use

# 登录两个注册表
echo $DOCKERHUB_TOKEN | docker login -u flyinke --password-stdin
echo $GITHUB_TOKEN | docker login ghcr.io -u flyinke --password-stdin

# 构建并推送到两个注册表
docker buildx build --platform linux/amd64,linux/arm64 \
  -t flyinke/wubi-dict-sync:latest \
  -t ghcr.io/flyinke/wubi-dict-sync:latest \
  --push .
```

### 4. 使用发布的镜像

#### 4.1 从 Docker Hub 拉取
```bash
docker pull flyinke/wubi-dict-sync:latest
```

#### 4.2 从 GitHub Container Registry 拉取
```bash
docker pull ghcr.io/flyinke/wubi-dict-sync:latest
```

#### 4.3 运行容器（Docker Hub 镜像）
```bash
docker run -d \
  --name wubi-dict-sync \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:password@host:port/dbname" \
  flyinke/wubi-dict-sync:latest
```

#### 4.4 运行容器（GHCR 镜像）
```bash
docker run -d \
  --name wubi-dict-sync \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:password@host:port/dbname" \
  ghcr.io/flyinke/wubi-dict-sync:latest
```

#### 4.5 使用 Docker Compose

**使用 Docker Hub 镜像:**
```yaml
version: '3.8'
services:
  wubi-dict-sync:
    image: flyinke/wubi-dict-sync:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
    depends_on:
      - db
  
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=wubi_dict_sync_db
      - POSTGRES_USER=wubi_user
      - POSTGRES_PASSWORD=wubi_password
    volumes:
      - postgres_data:/var/lib/postgresql/data/

volumes:
  postgres_data:
```

**使用 GitHub Container Registry 镜像:**
```yaml
version: '3.8'
services:
  wubi-dict-sync:
    image: ghcr.io/flyinke/wubi-dict-sync:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
    depends_on:
      - db
  
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=wubi_dict_sync_db
      - POSTGRES_USER=wubi_user
      - POSTGRES_PASSWORD=wubi_password
    volumes:
      - postgres_data:/var/lib/postgresql/data/

volumes:
  postgres_data:
```

### 5. 版本管理

#### 5.1 创建版本标签
```bash
# 创建并推送标签
git tag v1.0.0
git push origin v1.0.0
```

#### 5.2 查看可用版本
```bash
# 查看所有标签
git tag

# 查看远程标签
git ls-remote --tags origin
```

### 6. 监控和日志

#### 6.1 查看构建状态
- 进入 GitHub 仓库 → Actions 标签
- 查看 "Build and Push Docker Image" 工作流

#### 6.2 查看镜像状态

**Docker Hub:**
- 访问您的 Docker Hub 仓库页面
- 查看 Tags 和 Build History
- 地址：`https://hub.docker.com/r/flyinke/wubi-dict-sync`

**GitHub Container Registry:**
- 访问您的 GitHub 仓库 → Packages 标签
- 查看容器包详情
- 地址：`https://github.com/flyinke/wubi-dict-sync/pkgs/container/wubi-dict-sync`

### 7. 故障排除

#### 7.1 常见问题
1. **认证失败**：检查 Docker Hub 用户名和 token
2. **构建失败**：检查 Dockerfile 语法
3. **推送失败**：检查网络连接和权限

#### 7.2 调试步骤
1. 查看 GitHub Actions 日志
2. 本地测试 Dockerfile
3. 检查 Docker Hub 权限设置
