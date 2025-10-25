# 环境变量配置说明

## 📋 概述

本项目使用环境变量来配置 Docker Compose 服务，提供了灵活的配置选项。

## 🔧 配置步骤

### 1. 复制环境变量模板

```bash
cp .env.example .env
```

### 2. 编辑环境变量

编辑 `.env` 文件，根据需要修改以下配置：

```bash
# 数据库配置
POSTGRES_DB=wubi_dict_sync_db          # 数据库名称
POSTGRES_USER=wubi_user                # 数据库用户名
POSTGRES_PASSWORD=wubi_password        # 数据库密码
POSTGRES_PORT=5434                     # 数据库端口（主机端口）

# Django 配置
SECRET_KEY=your-secret-key-here        # Django 密钥（生产环境请修改）
DEBUG=1                                # 调试模式（生产环境设为0）
DATABASE_URL=postgresql://...          # 数据库连接URL

# 应用配置
DB_HOST=db                             # 数据库主机名
DB_PORT=5432                           # 数据库内部端口
APP_PORT=8002                          # 应用端口（主机端口）
```

## 🚀 使用方法

### 启动服务

```bash
# 使用默认配置启动
docker compose up -d

# 使用自定义环境变量启动
POSTGRES_PASSWORD=mypassword docker compose up -d
```

### 验证配置

```bash
# 检查环境变量是否正确加载
docker compose config

# 查看运行中的容器
docker compose ps

# 查看日志
docker compose logs wubi-dict-sync
```

## 🔒 安全注意事项

### 生产环境配置

1. **修改默认密码**：
   ```bash
   POSTGRES_PASSWORD=your-strong-password
   ```

2. **生成安全的 SECRET_KEY**：
   ```bash
   # 使用 Django 生成密钥
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **关闭调试模式**：
   ```bash
   DEBUG=0
   ```

### 环境变量优先级

1. 系统环境变量
2. `.env` 文件
3. `docker-compose.yml` 中的默认值

## 📝 配置示例

### 开发环境

```bash
# .env
POSTGRES_DB=wubi_dict_sync_dev
POSTGRES_USER=dev_user
POSTGRES_PASSWORD=dev_password
DEBUG=1
SECRET_KEY=dev-secret-key
```

### 生产环境

```bash
# .env
POSTGRES_DB=wubi_dict_sync_prod
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=very-strong-password
DEBUG=0
SECRET_KEY=very-secure-secret-key
```

## 🔍 故障排除

### 常见问题

1. **环境变量未生效**：
   ```bash
   # 检查环境变量是否正确加载
   docker compose config
   ```

2. **数据库连接失败**：
   ```bash
   # 检查数据库配置
   echo $DATABASE_URL
   ```

3. **端口冲突**：
   ```bash
   # 修改端口配置
   APP_PORT=8003
   POSTGRES_PORT=5435
   ```

### 调试命令

```bash
# 查看所有环境变量
docker compose exec wubi-dict-sync env

# 测试数据库连接
docker compose exec wubi-dict-sync python manage.py dbshell
```
