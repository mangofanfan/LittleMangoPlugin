from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类

from .lib import *


async def list_commands(ctx: EventContext):
    help_list = ["芒果帆帆给小芒果帆帆写的插件能干啥？"]
    for cmd, msg in COMMANDS:
        help_list.append(f"{cmd} -> {msg}")
    help_list.append("使用以下格式「小芒果 XX」调用插件命令嗷！")
    help_list.append("小芒果帆帆目前只装载这一个插件。若消息不以「小芒果」开头则默认调用DS模型输出回答哦！")
    ctx.add_return("reply", ["\n\n".join(help_list)])


def debug_msg(ctx: EventContext):
    return (f"调试模式数据返回："
            f"\n\n"
            f"Sender ID：{ctx.event.sender_id}"
            f"\n\n"
            f"Launcher ID：{ctx.event.launcher_id}")



COMMANDS = [
    ["帮助", "列出小芒果帆帆的 LittleMango 插件能帮你做的事情！"],
    ["调试数据", "获取当前对话的调试数据。"],
]

HELLO = ("你输入了能够召唤小芒果插件的神秘指令！"
         "\n\n"
         "使用「小芒果 帮助」获取小芒果 LittleMango 插件的全部功能！")
COMMAND_NOT_FOUND = ("小芒果帆帆命令似乎出错辣，请输入「小芒果 帮助」查看命令列表！"
                     "\n\n"
                     "如果需要和DS大模型聊天，请避免消息以「小芒果」开头哦！")


# 注册插件
@register(name="LittleMango", description="Little Mango ~", version="0.1", author="MangoFanFan")
class MyPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):
        pass

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        await self.commonHandler(ctx)

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        await self.commonHandler(ctx)

    # 通用处理函数
    async def commonHandler(self, ctx: EventContext):
        msg = ctx.event.text_message  # 这里的 event 即为 PersonNormalMessageReceived / GroupNormalMessageReceived 的对象

        if msg == "小芒果":
            ctx.add_return("reply", [HELLO])

        if msg.startswith("小芒果 "):
            self.ap.logger.info(f"用户召唤小芒果： {ctx.event.sender_id}")

            msg = msg.removeprefix("小芒果 ")
            # 判断指令
            if msg == COMMANDS[0][0]:  # 帮助
                await list_commands(ctx)
            elif msg == COMMANDS[1][0]:  # 调试数据
                ctx.add_return("reply", [debug_msg(ctx)])
            else:
                ctx.add_return("reply", [COMMAND_NOT_FOUND])

        # 阻止该事件默认行为（向接口获取回复）
        ctx.prevent_default()

    # 插件卸载时触发
    def __del__(self):
        pass
