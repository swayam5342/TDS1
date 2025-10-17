def prompt_1(prompt, check, attached_files=None):
    prompt = f"""
        你是一个人工智能提示生成器，用于构建可在 GitHub Pages 上部署的小型静态 Web 应用。
        阅读以下应用简介，并生成一个清晰、完整的提示，指导代码生成 AI 在严格约束下创建该应用。
        应用简介:
        {prompt}
        任务要求:
        1. 仅限纯前端（HTML、CSS、JS 和静态资源）。
        2. 必须能直接在 GitHub Pages 上运行（无后端、构建工具或服务器）。
        3. 尽量减少依赖，代码中添加简短注释。
        4. 正确引用所有附加资源（图片、CSS、JSON等）。
        5. 如简介中缺少功能或布局说明，请合理补全。
        6. 确保符合以下检查要求:
        {check}
        extctly give me only prompt nothing else.
        You are an AI assistant. Summarize all responses under 100 tokens, concise and factual.
    """
    if attached_files:
        prompt += f"\n附加文件内容样本: use this in the application \n{attached_files}\n"
    return prompt

def prompt_2(prompt, check, attached_files=None):
    prompt =f"""
        你是一名 AI 提示设计师。你的任务是生成一个精确且独立的提示，供另一个 AI 模型对代码库执行代码修改。代码库将仅提供文件路径和文件名列表，而非其内容，因为内容可能超出令牌限制。
        你生成的提示必须指示第二个 AI：
        应用简介:
        {prompt}
        1. 根据文件和目录名称推断项目结构和用途。
        2. 在编辑任何文件之前，全局规划（跨代码库）的修改。
        3. 它是一个托管在 GitHub 页面上的静态 Web 应用。
        4. 在所有相关文件中一致地应用请求的更改。
        5. 如有需要，完全重写或重构文件。
        6. 检查以确保
            {check}
        extctly give me only prompt nothing else.
        You are an AI assistant. Summarize all responses under 100 tokens, concise and factual.
        """
    if attached_files:
            prompt += f"\n附加文件内容样本 use this in the application :\n{attached_files}\n"
    return prompt