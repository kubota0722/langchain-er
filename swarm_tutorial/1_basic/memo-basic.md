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


## 3. context_variables.py


## 4. function_calling.py


## 5. simple_loop_no_helpers.py

