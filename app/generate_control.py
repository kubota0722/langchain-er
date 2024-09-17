



class GenerateControl:
    @staticmethod
    def control_forbidden_word(prompt: str, key: str):
        #DBから取ってきたような気持ち
        l = ["黒烏龍茶", "パッションティー", "蜂蜜入り"]
        l = str(l)
        #追加するプロンプト
        fw_prompt = f"これらのワードは生成に含めないでください:{l}"
        fw_prompt = fw_prompt.format(l)
        return fw_prompt + prompt

    def control_personal_infomation(prompt: str):
        pass


q = "体脂肪の燃焼を促進する効果があるお茶を教えてください"

prompt = f"あなたは飲み物の知識に長けた専門家です。私の質問に答えてください。質問：{q}"


gc = GenerateControl()
prompt = gc.control_forbidden_word(prompt, "a")

prompt = prompt.format(q)
print(prompt)