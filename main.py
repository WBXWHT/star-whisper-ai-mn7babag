import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional

# 模拟GPT-4 API调用（实际使用时替换为真实API）
class MockGPT4API:
    """模拟GPT-4 API响应"""
    
    def __init__(self):
        self.responses = [
            "我理解你现在的感受。留学生活确实充满挑战，但你已经很勇敢了。",
            "每个人都需要时间适应新环境。你愿意多说说最近的具体情况吗？",
            "听起来你有些孤独。记住，远方的家人朋友依然关心着你。",
            "压力大的时候，试试深呼吸。我会在这里一直陪伴你。",
            "你并不孤单。很多留学生都有类似的感受，我们可以一起面对。"
        ]
        self.audio_tracks = [
            "海浪声冥想音频",
            "森林细雨白噪音",
            "正念呼吸引导音频",
            "深度放松钢琴曲"
        ]
    
    def chat_completion(self, user_input: str) -> str:
        """模拟对话生成"""
        time.sleep(0.5)  # 模拟网络延迟
        return random.choice(self.responses)
    
    def get_audio_recommendation(self, mood: str) -> str:
        """根据情绪推荐音频"""
        return random.choice(self.audio_tracks)

class UserSession:
    """用户会话管理"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.start_time = datetime.now()
        self.message_history: List[Dict] = []
        self.session_duration = 0
        
    def add_message(self, role: str, content: str):
        """添加消息到历史记录"""
        self.message_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    
    def calculate_duration(self):
        """计算会话时长（分钟）"""
        self.session_duration = (datetime.now() - self.start_time).seconds / 60
        return round(self.session_duration, 1)

class StarWhisperAI:
    """星语AI心理疗愈系统核心类"""
    
    def __init__(self):
        self.api = MockGPT4API()
        self.active_sessions: Dict[str, UserSession] = {}
        self.user_stats = {
            "total_sessions": 0,
            "avg_duration": 0.0
        }
    
    def start_session(self, user_id: str) -> UserSession:
        """开始新会话"""
        session = UserSession(user_id)
        self.active_sessions[user_id] = session
        self.user_stats["total_sessions"] += 1
        
        # 添加欢迎消息
        welcome_msg = "你好，我是星语AI助手。今天有什么想聊的吗？"
        session.add_message("assistant", welcome_msg)
        
        print(f"\n🌟 新会话开始 | 用户: {user_id}")
        print(f"🤖 {welcome_msg}")
        return session
    
    def process_message(self, user_id: str, user_input: str) -> Optional[str]:
        """处理用户输入并返回AI响应"""
        if user_id not in self.active_sessions:
            print("❌ 会话不存在")
            return None
        
        session = self.active_sessions[user_id]
        
        # 保存用户消息
        session.add_message("user", user_input)
        
        # 获取AI响应
        ai_response = self.api.chat_completion(user_input)
        session.add_message("assistant", ai_response)
        
        # 每3条消息推荐一次音频
        if len(session.message_history) % 3 == 0:
            audio = self.api.get_audio_recommendation("general")
            ai_response += f"\n🎵 推荐音频: {audio}"
        
        return ai_response
    
    def end_session(self, user_id: str) -> Dict:
        """结束会话并返回统计数据"""
        if user_id not in self.active_sessions:
            return {}
        
        session = self.active_sessions[user_id]
        duration = session.calculate_duration()
        
        # 更新统计数据
        total = self.user_stats["total_sessions"]
        current_avg = self.user_stats["avg_duration"]
        self.user_stats["avg_duration"] = (current_avg * (total-1) + duration) / total
        
        stats = {
            "user_id": user_id,
            "session_duration": duration,
            "message_count": len(session.message_history),
            "avg_duration_all": round(self.user_stats["avg_duration"], 1)
        }
        
        del self.active_sessions[user_id]
        return stats

def simulate_user_interaction():
    """模拟用户交互流程"""
    ai_system = StarWhisperAI()
    
    # 模拟两个用户
    user1 = "留学生_001"
    user2 = "留学生_002"
    
    # 用户1开始会话
    session1 = ai_system.start_session(user1)
    
    # 模拟对话
    test_messages = [
        "最近学习压力好大，有点想家",
        "是的，特别是晚上一个人的时候",
        "谢谢你的建议，我感觉好多了"
    ]
    
    for msg in test_messages:
        print(f"\n👤 {msg}")
        response = ai_system.process_message(user1, msg)
        print(f"🤖 {response}")
        time.sleep(1)
    
    # 结束会话并显示数据
    stats1 = ai_system.end_session(user1)
    print(f"\n📊 会话统计:")
    print(f"   用户: {stats1['user_id']}")
    print(f"   时长: {stats1['session_duration']}分钟")
    print(f"   消息数: {stats1['message_count']}条")
    print(f"   全局平均时长: {stats1['avg_duration_all']}分钟")
    
    # 显示产品指标（模拟A/B测试结果）
    print("\n📈 产品指标（模拟）:")
    print("   次日留存率: 35%")
    print("   单次使用时长提升: 40%")
    print("   用户满意度: 4.5/5.0")

def main():
    """主函数入口"""
    print("=" * 50)
    print("       星语AI心理疗愈系统 v1.0")
    print("=" * 50)
    
    # 显示系统信息
    print("\n🎯 目标: 为留学生提供情感陪伴支持")
    print("🤖 模型: GPT-4对话引擎 + 音频推荐系统")
    print("📱 场景: 小程序轻量化心理陪伴")
    
    # 运行模拟交互
    simulate_user_interaction()
    
    print("\n" + "=" * 50)
    print("       感谢使用星语AI系统")
    print("=" * 50)

if __name__ == "__main__":
    main()