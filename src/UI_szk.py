import os
import re
import json
import gradio
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from dotenv import load_dotenv
from openai import chat
import sys_msg
from main_chat_agent import ChatAgent

load_dotenv(".env")
print("openai-api-key:",os.environ["OPENAI_API_KEY"])

system_msg = SystemMessage(content=sys_msg.psycho_prompt.format())
chat_model = ChatOpenAI(model_name="ft:gpt-3.5-turbo-1106:buptai4ai::8hDdSdXu")
chat_agent = ChatAgent(chat_model=chat_model,system_message=system_msg)

with gradio.Blocks() as demo:
    gradio.HTML("<h1 align='center'>虚拟心理咨询师</h1> ")
    gradio.HTML("<h4 align='center'>1.使用前请先输入您的姓名学号,并点击新建/读取对话按钮，第一次使用本系统时将新建对话，若使用过本系统则读取用户历史对话数据。2.使用时请在下方文本框中输入问题，点击发送提交消息，如需修改您上一条发送的消息可点击重新编辑以修改，点击清除历史以清除所有的对话历史，底部菜单可下拉以更换对话模型和调节模型生成回复的参数。3.使用完毕可点击保存当前对话按钮保存目前的对话历史，祝您心情愉快^_^</h4>")
    chat_history = []
    with gradio.Row():
        usr_msg = gradio.Textbox(label="请输入学号+姓名，作为管理对话历史的用户凭证（请使用数字开头，如2020123456李华）")
        with gradio.Column():
            create_button = gradio.Button("新建/读取对话")
            save_button = gradio.Button("保存当前对话")
    with gradio.Row():
        chatbot = gradio.Chatbot(value = chat_history, height=450)
    with gradio.Column():
        msg = gradio.Textbox(label="请在此输入您的消息^_^")
        with gradio.Row():
            clear = gradio.Button("清除历史")  
            re_generate = gradio.Button("重新编辑")
            sent_bt = gradio.Button("发送")     
        with gradio.Accordion("对话模型选择及生成参数修改", open=False):
            models_choise = gradio.Dropdown(choices=["ESconv-smile", "psy-insight-Chinese", "psy-insight-English", "ChatGPT3.5-turbo"], label="对话模型选择", value="ESconv-smile", allow_custom_value=True)
            slider_temp = gradio.Slider(minimum=0, maximum=1, label="temperature", value=0.95)
            slider_top_p = gradio.Slider(minimum=0.5, maximum=1, label="top_p", value=0.95)

    # 创建、读取用户对话历史
    def usr_login(name):
        if bool(re.match(r'^\d+.*$|用户(.*?)的对话', name)):
            filename = f'usr_datas/{name}.json'
            if os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    chat_agent.list_to_history(data)
                    chat_history = []
                    for m in range(0,len(data),2):
                        chat_history.append((data[m],data[m+1]))
                    return f'读取用户{name}的对话历史成功！', chat_history
                except:
                    return '用户历史数据损坏！', []
            else:
                initial_content = [['你好','你好呀，我是虚拟心理咨询师！']]
                chat_agent.list_to_history(initial_content[0])
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(initial_content[0], file, ensure_ascii=False, indent=4)
                return f'创建用户{name}的对话成功，欢迎使用！', initial_content
        else:
            return '请输入正确的学号+姓名！', []

    # 保存对话历史
    def usr_save(name):
        filename = re.search("用户(.*?)的对话", name)
        try:
            filepath = f'usr_datas/{filename.group(1)}.json'
            if os.path.exists(filepath):
                history = chat_agent.get_history()
                chat_history = []
                for dias in history[1:]:
                    chat_history.append(dias.content)
                with open(filepath, 'w', encoding='utf-8') as file:
                    json.dump(chat_history, file, ensure_ascii=False, indent=4)
                return f'用户{filename.group(1)}的对话历史保存成功！'          
            else:
                return '用户不存在，请先创建用户！'
        except:
            return '用户不存在，请先创建用户！'

    # 发送按钮
    def send_message(humanMessage, temperature, top_p):
        history = chat_agent.step(humanMessage,temperature,top_p)
        chat_history = []
        for m in range(1,len(history),2):
            chat_history.append((history[m].content,history[m+1].content))
        return chat_history, ''
    
    # 重新编辑按钮
    def re_generate_action(temperature, top_p):
        history = chat_agent.get_history()
        if len(history) > 1:
            last_message = history[len(history)-2].content
            history.pop()
            last_user = history.pop().content
            # history = chat_agent.step(last_message,temperature,top_p)
            history = chat_agent.get_history()
            chat_history = []
            for m in range(1,len(history),2):
                chat_history.append((history[m].content,history[m+1].content))
            return chat_history, last_user
        else:
            return chat_history, ''
        
    # 清除按钮
    def clear_click():
        chat_agent.reset()
        history = chat_agent.get_history()
        chat_history = []
        for m in range(1,len(history),2):
            chat_history.append((history[m].content,history[m+1].content))
        return chat_history, ''

    def model_select(models):
        if models == 'ESconv-smile':
            chat_agent.chat_model = ChatOpenAI(model_name="ft:gpt-3.5-turbo-1106:buptai4ai::8hDdSdXu")
            chat_agent.system_message = SystemMessage(content=sys_msg.psycho_prompt.format())
            chat_agent.change_sys_msg()
        elif models == 'psy-insight-Chinese':
            chat_agent.chat_model = ChatOpenAI(model_name="ft:gpt-3.5-turbo-1106:buptai4ai:ckq-chinese-data:93bvQETV")
            chat_agent.system_message = SystemMessage(content=sys_msg.psy_prompt_chinese.format())
            chat_agent.change_sys_msg()
        elif models == 'psy-insight-English':
            chat_agent.chat_model = ChatOpenAI(model_name="ft:gpt-3.5-turbo-1106:buptai4ai:ckq-data:93LR1q7L")
            chat_agent.system_message = SystemMessage(content=sys_msg.psy_prompt_english.format())
            chat_agent.change_sys_msg()
        elif models == 'ChatGPT3.5-turbo':
            chat_agent.chat_model = ChatOpenAI(model_name="gpt-3.5-turbo-1106")
            chat_agent.system_message = SystemMessage(content=sys_msg.gpt_prompt.format())
            chat_agent.change_sys_msg()
        else:
            pass
    def init_his():
        chat_agent.reset()
        print('init success')
    init_output = gradio.Textbox(value=init_his, visible=False)


    create_button.click(usr_login, inputs=usr_msg, outputs=[usr_msg, chatbot])
    save_button.click(usr_save, inputs=usr_msg, outputs=usr_msg)
    sent_bt.click(send_message, inputs=[msg, slider_temp, slider_top_p], outputs=[chatbot,msg])
    re_generate.click(re_generate_action, inputs=[slider_temp, slider_top_p], outputs=[chatbot,msg])
    clear.click(clear_click, inputs=[], outputs=[chatbot, msg])
    models_choise.change(fn=model_select, inputs=models_choise)


if __name__ == "__main__":
    demo.queue(max_size=8).launch(share=False, debug=True, server_name="0.0.0.0", server_port=55667)
