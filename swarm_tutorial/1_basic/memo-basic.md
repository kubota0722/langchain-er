# Swarm Basic Folder
メモとか感じたこと、雑多なコメント

## 1. agent_handoff.py
異なる言語（英語とスペイン語）を話す2つのAIエージェント間でメッセージを渡す。
というよりも、英語話者側のAIエージェントがスペイン語で入力されたときにスペイン語話者を呼び出すような感じ。

```python
def transfer_to_spanish_agent():
    """return the spanish agent"""
    return spanish_agent
```
で`"""return the spanish agent"""`って関数の説明を書けば、その用途で使われるってことですか？
いまいちよくわからない。

`english_agent.functions.append(transfer_to_spanish_agent)`で関数を追加してたけど、これagent作るときに入れてもよくね？って思って変えた。別にどっちでもイイ！どっちにしようか悩めば、イイ！

現状、ここの使い分けがどこに生きてくるのかはわからない、agent→function→function内でagentに他のfunctionを追加、みたいな？

入り口と出口は多言語に対応してるけど、内部のゴタゴタは全部英語に統一しちゃうみたいなこともできるかもしれん、wrapってやつですか、知らんけど。

## 2. bare_minimum.py
swarmのagentの最小構成、
agentの振る舞いはinstructionsで色々できた


```python
messages = [
    {"role": "user", "content": "Hello! How are you?"}
]
response = client.run(
    agent=agent,
    messages=messages,
)
```
client.runのとき、messagesとして与えるときの型が気になる。

roleが
- user 
- assistant
- tool

は確認した、swarmでAgent期の伏線回収してると思うんだけど、そのころの追ってないからわからん、要考察

## 3. context_variables.py
関係ないけど、リーダブルコードで読んだ縦整列やってみた
```python
# print account details
user_id = context_variables.get("user_id", None)
name    = context_variables.get("name"   , None)
```
確かに見やすいし、並べるのは楽しいけど、どこ基準で並べるか延々悩む世界線に入りそうだから、なんか言われない限りはやらない

**このpartまじでわからん！！！！！**

client.runのときに与えたcontext_variablesが巡っているのはわかる。

さらっとinstructionsが関数になっているのもヤメテー。
これはまだいい、instructionsとして入れるべき文章をcontext_variablesの要素を使って作成してるから、

context_variablesを更新させてみた、生成されたメッセージには反映された
```
こんにちは、kk0722-latestさん！アカウントの詳細が最新化されました。何か他にお手伝いできることはありますか？
{'name': 'kk0722', 'user_id': 'K0123456789'}
```
その下でシンプルに出力してみたけど、context_variablesには反映されていなかった

いや、当然か、context_variablesはパラメータとして渡されてるだけだから、responseの内容確認してみる

以下responseの中身
```python
messages=[
    {
        'content': None,
        'refusal': None,
        'role': 'assistant',
        'function_call': None,
        'tool_calls': [
            {
                'id': 'call_xb9H5XF06OzhUx4OiDYgsrAy',
                'function': {
                    'arguments': '{}',
                    'name': 'update_account_details'
                },
                'type': 'function'
            }
        ],
        'sender': 'Agent'
    },
    {
        'role': 'tool',
        'tool_call_id': 'call_xb9H5XF06OzhUx4OiDYgsrAy',
        'tool_name': 'update_account_details',
        'content': 'success'
    },
    {
        'content': 'こんにちは、kk0722-latestさん。アカウントの詳細を最新化しました。何か他にお手伝いできることはありますか？',
        'refusal': None,
        'role': 'assistant',
        'function_call': None,
        'tool_calls': None,
        'sender': 'Agent'
    }
]

agent=Agent(
    name='Agent',
    model='gpt-4o',
    instructions=<function instructions at 0x103c525c0>,
    functions=[
        <function print_account_details at 0x103c52660>,
        <function update_account_details at 0x103c52700>
    ],
    tool_choice=None,
    parallel_tool_calls=True
)

context_variables={
    'name': 'kk0722-latest',
    'user_id': 'K0123456789-latest'
}
```

更新されたcontext_variablesはresponse.context_variablesで取得する

よく考えてみれば、そりゃそうだよなって感じではある、
`print_account_datails`、`update_account_details`がなんか直でcontext_variablesを更新してくれるように見えたから勘違いしてた

あと、Agentからのメッセージのnameが更新後なのが気になる

## 4. function_calling.py
作成した関数を呼び出す

さっきはcontext_variablesを渡してあーだこーだだったけど、ここでは引数なんでもイイ！になってる

agentのfunctionsに追加しておけば使ってくれる

どうやって解釈しているんだろ、関数につけたコメントが大事だったりする？
元のコードにはコメントとかついてないんだよな、よくわからん。
Agent期の文脈を読めてないからかもしれん（n回目）

## 5. simple_loop_no_helpers.py
途中
