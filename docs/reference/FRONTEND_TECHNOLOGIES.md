# 前端技术栈

本文档概述了 xxxx 项目中所使用的前端技术。

## 核心框架与库

- **[Tailwind CSS](https://tailwindcss.com/)**: 一个功能优先的 CSS 框架，用于快速构建自定义设计。本项目使用 Tailwind CSS 进行所有样式设计。编译后的 CSS 文件位于 `backend/static/output.css`。
- **[Alpine.js](https://alpinejs.dev/)**: 一个轻量级的 JavaScript 框架，用于在 HTML 中直接实现交互功能。
- **[htmx](https://htmx.org/)**: 一个让你可以直接通过 HTML 属性而不是 JavaScript 来使用现代浏览器功能的库。

## UI 组件与图标

- **[DaisyUI](https://daisyui.com/)**: Tailwind CSS 的一个插件，提供了一系列预设样式的组件，如按钮、卡片和表单，有助于更快地构建用户界面。
- **[Lucide](https://lucide.dev/)**: 一套简洁美观的图标库。

## 文件上传

- **[tus](https://tus.io/)**: 一种可续传文件上传协议。项目中使用 `tus.min.js` 作为客户端实现。
- **[Uppy](https://uppy.io/)**: 一个优雅的、模块化的文件上传工具，与 `tus` 集成。项目中包含了 Uppy 的 CSS 和 JavaScript 文件。

## 其他库

- **[Toastify JS](https://apvarun.github.io/toastify-js/)**: 一个轻量级、非阻塞的通知提示库。
- **[Marked](https://marked.js.org/)**: 一个 Markdown 解析和编译器，用于渲染 Markdown 内容。
- **[qrcode.js](https://github.com/davidshimjs/qrcodejs)**: 一个用于生成二维码的 JavaScript 库。

## 前端资源管理

前端资源通过 `npm` 进行管理。`frontend/package.json` 文件列出了所有前端依赖项。`tailwindcss` 的命令行工具被用来将 `frontend/input.css` 文件编译成 `backend/static/output.css`。
