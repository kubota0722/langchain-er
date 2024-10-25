from langchain_core.output_parsers import JsonOutputParser
# todo: 中で使ってる正規表現が変なのかも、isinstanceらへんで追うの頓挫してたからいつか克服する

text = """
1. あいうえお

```json
{
    "key": "キー"
}
```
"""

p = JsonOutputParser()
print(p.parse(text))