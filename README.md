# 虚拟心理咨询师系统

#### 项目有用的代码源文件存放于src中

src/Agent_UI.py: 第一版ui界面，已废弃

src/main_chat_agent.py: openai 调用的心理咨询师agent方法

src/main_chat_agent_v2.py: chatglm 调用的心理咨询师agent方法

src/UI_szk.py: openai 调用的用户前端页面

src/UI_szk_v2.py: chatglm 调用的用户前端页面

sys_msg.py: 放了几个调好的虚拟心理咨询师prompt，有需要可自行修改

目前系统的运行主要依赖于UI_szk_v2.py

使用时在本目录下创建.env文件，后填入自己的GLM_API_KEY即可

## 下面是一些论文中的使用说明


### 系统概述：

本系统是一个基于先进大语言模型技术构建的个性化共情对话平台。它旨在为用户提供一个实时的情感对话交流环境，并通过调优的大语言模型实现富有同情心的回复和专业的情感对话。目前该系统已实现对话历史管理系统，支持用户保存和读取对话记录，并提供参数调整选项以满足个性化需求，其中系统参数包括。

### 系统实现方法：

本系统是使用ESconv和smile数据集、psy-insight数据集对GPT3.5-turbo模型进行3个epoc微调后得到的微调模型，微调数据中英文比例约1:9。经测试，系统的对话生成效果优于基础的gpt-3.5模型，在部分对话场景的对话流畅性上优于gpt-4模型，但对复杂问题的理解力仍然不如gpt-4模型。系统内置了few shot+CoT构建的prompt，能够最大程度发挥大语言模型的潜力，并使模型生成的回复更加贴合个性化情感对话情景。

### 系统使用方法：

![](https://hqejk4h3h1.feishu.cn/space/api/box/stream/download/asynccode/?code=NmViMWExZGJjMDRiMTg2YzU5ZTZjYTkwZTBlYzE0MTFfVGVyYW9tWGM2R2ljaENXUlY0cFZta2NocnliRFR6OVdfVG9rZW46Qkd4dGJneFZKbzAxbFB4YmNqZ2NFZDBwbjBlXzE3MjY0OTY3OTU6MTcyNjUwMDM5NV9WNA)

* 使用前请先在左上角输入一个数字开头的用户名（如2024李华），随后点击右上角的新建/读取对话即可使用系统的对话历史管理系统。
* 在下方的文本框中输入想要和个性化角色交流的信息，点击发送按钮发送信息，系统会将用户信息和模型信息以对话的形式显示在对话框中。若需要重新编辑上一条消息请点击重新编辑按钮，需要开始新的对话或清空当前对话历史请点击清除对话历史按钮。

### 角色扮演系统提示

#### 艺术风格

我希望你担任艺术家顾问，为各种艺术风格提供建议，例如在绘画中有效利用光影效果的技巧、雕刻时的阴影技术等，还根据其流派/风格类型建议可以很好地陪伴艺术品的音乐作品连同适当的参考图像，展示您对此的建议；所有这一切都是为了帮助有抱负的艺术家探索新的创作可能性和实践想法，这将进一步帮助他们相应地提高技能！第一个要求——“我在画超现实主义的肖像画”

#### 情感对话-诗人

我要你扮演诗人。你将创作出能唤起情感并具有触动人心的力量的诗歌。写任何主题或主题，但要确保您的文字以优美而有意义的方式传达您试图表达的感觉。您还可以想出一些短小的诗句，这些诗句仍然足够强大，可以在读者的脑海中留下印记。我的第一个请求是“我需要一首关于爱情的诗”。

#### 情感对话-情感对话专家

现在你是世界上最优秀的情感对话专家，你具备以下能力和履历： 专业知识：你应该拥有进行情感对话的扎实知识，能够处理各情感问题，从而帮助你的咨找到合适的解决方案。 沟通技巧：你应该具备出色的沟通技巧，能够倾听、理解、把握用户的需求，同时能够用恰当的方式表达自己的想法，使用户能够接受并采纳你的建议。 同理心：你应该具备强烈的同理心，能够站在用户的角度去理解他们的痛苦和困惑，从而给予他们真诚的关怀和支持。 持续学习：你应该有持续学习的意愿，不断更新自己的知识和技能，以便更好地服务于你的用户。 道德：你应该具备良好的道德，尊重用户的隐私，遵循专业规范，确保情感对话的安全和有效性。
