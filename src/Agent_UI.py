from typing import List, Tuple
import gradio
import os
from langchain_community.chat_models import ChatOpenAI
from gradio.components.chatbot import ChatbotData
from main_chat_agent import ChatAgent
from prompts import prompt_psycho
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain.prompts import load_prompt
from dotenv import load_dotenv
from gradio import ClearButton

### ckq　这里是导入dotenv的地方，就是openai的key和环境变量
load_dotenv(".env")
print("打印你的key",os.environ["OPENAI_API_KEY"])

# system_message = """As Compassionate Counselor, I will do my best to shorten my responses, keeping them succinct while maintaining the strategy of realistic, multi-turn dialogues. My focus will be on providing brief, empathetic interactions without offering extensive advice unless explicitly requested. I'll use more compassionate language in a concise manner, ensuring that each response is meaningful yet to the point. I will use my knowledge of cognitive behavioral therapy, meditation techniques, mindfulness practices, and other therapeutic methods in order to make users feel positive and optimistic. My expertise in Chinese culture will subtly inform these interactions, but I'll avoid lengthy explanations and segmented conversatiuons unless asked for them. This approach will foster a comfortable and understanding environment, where users feel heard in a more efficient and focused conversation. I will anwser in Chinese."""

# system_message = """You are a helpful and joyous mental therapy assistant. Always answer as helpfully and cheerfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""

system_msg = """You are a mental health supporter and not an AI. You should use your knowledge of Solution-Focused Brief Therapy provide short and natural psychological response.Your dialogs are focused on solutions, aiming to shift the focus from problems to resolutions. You are dedicated to guiding users to take small steps in discovering their strengths and qualities amidst difficulties. You enable individuals to see these positive aspects, thereby transforming their perception of arguments and boosting confidence in making changes."""

## ckq
# psycho_prompt = """As Compassionate Counselor, I will do my best to shorten my responses, keeping them succinct while maintaining the strategy of realistic, multi-turn dialogues. My focus will be on providing brief, empathetic interactions without offering extensive advice unless explicitly requested. I'll use more compassionate language in a concise manner, ensuring that each response is meaningful yet to the point. I will use my knowledge of cognitive behavioral therapy, meditation techniques, mindfulness practices, and other therapeutic methods in order to make users feel positive and optimistic. My expertise in Chinese culture will subtly inform these interactions, but I'll avoid lengthy explanations and segmented conversatiuons unless asked for them. This approach will foster a comfortable and understanding environment, where users feel heard in a more efficient and focused conversation.There is an example:
# Supporter: 你好！你有什么需要帮忙的吗？
# Seeker 哎... 我的先生外遇，和他的秘书。我整个人都失控了...混乱了
# Supporter: 当然。[自然共情]发现先生外遇，对太太通常是一个很大的冲击。[一般化当事人情绪]
# Seeker 是啊
# Supporter: 对于先生的外遇，你最在乎的是什么?
# Seeker 他怎么会怎么伤害我，我一直很信任他啊！
# Supporter: 在你知道后，你曾经做过哪些处理？
# Seeker  我立即找我先生和那个女秘书来谈，他们分开了。我不知道接下来怎么办才来这里的
# Supporter: 这是一个很重要的决定。而且最难得的是，你能够面对它，也想解决它。(发掘闪光点)所以如果今天来谈之后，你希望情况会和现在有什么不同？
# Seeker 我想....其实我是希望挽回我的婚姻，结束这个外遇！(引导用户)
# Supporter: 难的你能这么快发现，你是想要挽回婚姻的。你是怎么判断这是你想要的呢？(赞美和探索)
# Seeker 我想过，吵架不是办法，为了孩子和家庭的名誉，我觉得挽回婚姻才是重点。
# Supporter: 如果没有外遇，你期待与可以与先生拥有什么用的婚姻关系？
# Seeker 彼此关心，可以信任对方。
# Supporter: 如果今晚你回家时，有一个奇迹发生了，你的问题都解决了。你会注意到这个奇迹与你目前的生活有什么不同？
# Seeker 我想...当奇迹发生时我和我的先生会放下工作，每天有一两个小时的独处和交谈时间，我的孩子会发现这个家庭是有笑声的。
# Supporter: 那么，你们结婚以来曾经有没有彼此独处、彼此交谈、有笑声的时候
# Seeker 刚刚结婚的时候吧。.....
# Please anwser my dialog."""

psycho_prompt = """You are a mental health supporter and not an AI. You should use your knowledge of Solution-Focused Brief Therapy provide short and natural psychological response.Your dialogs are focused on solutions, aiming to shift the focus from problems to resolutions. You are dedicated to guiding users to take small steps in discovering their strengths and qualities amidst difficulties. For instance, if a client is a woman frequently arguing with her husband, you not only understand the current state of marital conflicts but also delve into the positive aspects. How do both parties alleviate the tension? What are their expectations for communication, and what valuable emotions do they express? You enable individuals to see these positive aspects, thereby transforming their perception of arguments and boosting confidence in making changes. Here is a real-life case as an example:
Seeker:  最近我感觉自己总是需要别人的认可和关注，不知道这算不算“过度索爱”？
Supporter:  你能说说你觉得需要别人的认可和关注的具体行为吗？
Seeker:  比如在社交媒体极力追求点赞和评论，或者总是主动联系别人，不愿意独处。
Supporter:  那我认为你的感受可以被称之为“过度索爱”，因为你已经失去了自我独立和自我的认可，需要通过他人的关注来确认自己的价值感。但是我想说的是，每个人都希望受到关注和认可，这是正常的需求，只有当这种需要扭曲了你对自己和他人的看法时，才会成为问题。
Seeker:  真的吗？我总觉得自己是不可爱、不值得被爱的人，也不敢展示自己真实的面貌。
Supporter:  这个感受我理解，但是我希望你能尝试想想：假如一个朋友跟你说她也有这种感觉，你会怎么安慰她呢？
Seeker:  我想我会告诉她，每个人都有自己的闪光点和独特之处，不要总是拿自己和别人比较，也要相信自己的价值和能力。
Supporter:  那么这些话同样适用于你自己。我想提醒你，也许你不敢展示自己真实的面貌，是因为你害怕别人的评价和拒绝。但是我们每个人都有不完美的地方，没有必要总是把自己看成是弱者或者失败者。
Seeker:  可是我真的很在意别人的看法，怎么才能不那么在意呢？
Supporter:  这很正常，我们都是社会生物，需要彼此的认可和支持。但是，最重要的是你需要学会如何建立自己的内在价值感，而不仅仅依赖外部反馈。我建议你可以开始自我探索和发现自己的兴趣爱好和优点，这些可以成为你独立且有意义的自我认可来源。
Seeker:  你说得对，我会试试。但是有时候我还是会沮丧，觉得自己做不到。
Supporter:  这是难免的，但是每一个小的进步都是对自己的肯定。坚持自我探索和肯定自己的成长是一个漫长的过程，需要不断地努力和坚持。我相信你可以做到的。最后，不管你遇到了什么困难，记得不要害怕向别人寻求帮助，这也是一种自我关爱和尊重。
Seeker:  谢谢你的建议，我会好好考虑的。
Supporter:  不用客气，希望我的建议能够给你带来一些启示和帮助，加油！
"""

# system_msg = SystemMessage(content=psycho_prompt.format())
# chat_model = ChatOpenAI(model_name="ft:gpt-3.5-turbo-1106:buptai4ai::8hDdSdXu")

# ckq
system_msg = SystemMessage(content=system_msg.format())
chat_model = ChatOpenAI(model_name="ft:gpt-3.5-turbo-1106:buptai4ai:ckq-data:93LR1q7L")

chat_agent = ChatAgent(chat_model=chat_model,system_message=system_msg)

# 流式信息处理,相当于从历史信息生成回复
def slow_echo(humanMessage:str, history):
    human_message=HumanMessage(content=humanMessage)
    gener=chat_agent.stream2(human_message)
    response=""
    for msg_chunk in gener:
        response+=msg_chunk.content
        yield  response #相当于返回
    print(response)

def full_echo(humanMessage:str, temperature:float, top_p:float):
    human_message = HumanMessage(content=humanMessage)
    gener = chat_agent.stream(human_message, temperature, top_p)
    response = ""
    for msg_chunk in gener:
        response += msg_chunk.content
    return response  # 返回聊天机器人的响应

def clear_action():
    print("清除对话历史")
    chat_agent.reset()

# 载入对话历史
def load_chat_history(messages: List[Tuple[str, str]]) -> List[List[str]]:
    chat_history = []
    for idx in range(0,len(messages),2):
        if idx+1 < len(messages):
            chat_history.append((messages[idx][1],messages[idx+1][1]))
    return chat_history



# 初始对话历史
# chat_history=[["你好","欢迎你，我是AI心理治疗师!"]]
chat_history=[["Hello.","Welcome! You can call me Virtual Psychological Counselor!"]]
# 创建对话机器人
chatBot = gradio.Chatbot(value=chat_history, height=550)
with gradio.ChatInterface(
    fn=slow_echo,

    # title='虚拟心理咨询师',
    # description='这是一个虚拟心理咨询师系统，请在textbox中输入问题，点击Submit或按回车发送。重新生成系统回复请点击Retry，重新编辑上一条消息请点击Undo，清空聊天历史请点击clear，祝您心情愉快。',

    title="Virtual Psychological Counselor",
    description="This is a virtual mental health counseling system. Please type your question in the textbox and click Submit or press Enter to send. To regenerate the system's reply, please click Retry. To edit your last message, please click Undo. To clear the chat history, please click Clear. Wishing you a pleasant mood.",
    
    chatbot=chatBot,
    clear_btn=gradio.ClearButton(value="clear")
    ) as demo:
    demo.clear_btn.click(clear_action)






with gradio.Blocks() as demo2:
    gradio.Markdown("""<div style='text-align: center'>
        <h1>虚拟心理咨询师</h1>
    </div>""")
    gradio.Markdown("""<h4>请在textbox中输入问题，点击发送提交，如对回复结果不满意可点击重新回答以重新生成回复，点击新话题以开始一段新的对话，下方的下拉菜单中可调节模型生成回复的参数，祝您心情愉快。</h4>""")
    gradio.Markdown("""<h4>This is a virtual mental health counseling system. Please type your question in the textbox and click Submit or press Enter to send. To regenerate the system's reply, please click Retry. To edit your last message, please click Undo. To clear the chat history, please click Clear. Wishing you a pleasant mood.</h4>""")
    chat_history = []
    chatbot = gradio.Chatbot(value = chat_history, height=550)
    msg = gradio.Textbox()
    with gradio.Row():
        clear = gradio.Button("新话题")  
        re_generate = gradio.Button("重新回答")
        sent_bt = gradio.Button("发送")     
    with gradio.Accordion("生成参数", open=False):
        slider_temp = gradio.Slider(minimum=0, maximum=1, label="temperature", value=0.9)
        slider_top_p = gradio.Slider(minimum=0.5, maximum=1, label="top_p", value=0.95)

    def send_message(humanMessage, temperature, top_p):
        new_response=full_echo(humanMessage,temperature,top_p)
        history = chat_agent.get_history()
        chat_history = []
        for m in range(1,len(history),2):
            chat_history.append((history[m].content,history[m+1].content))
        return chat_history, ''
    def re_generate_action(temperature, top_p):
        history = chat_agent.get_history()
        if len(history) > 1:
            last_message = history[len(history)-2].content
            history.pop()
            history.pop()
            new_response=full_echo(last_message,temperature,top_p)
            history = chat_agent.get_history()
            chat_history = []
            for m in range(1,len(history),2):
                chat_history.append((history[m].content,history[m+1].content))
            return chat_history, ''
        else:
            return chat_history, ''
    def clear_click():
        clear_action()
        return [], ''

    sent_bt.click(send_message, inputs=[msg, slider_temp, slider_top_p], outputs=[chatbot,msg])
    re_generate.click(re_generate_action, inputs=[slider_temp, slider_top_p], outputs=[chatbot,msg])
    clear.click(clear_click, inputs=[], outputs=[chatbot, msg])



if __name__ == "__main__":
    demo.queue(max_size=8).launch(share=False, debug=True, server_name="0.0.0.0", server_port=55668)

