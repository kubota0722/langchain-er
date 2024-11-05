## JsonOutputParserのparseメソッドの内部動作
langchain_core output_parsers json.pyの内容について

by Cursor with o1-mini

## 生成内容
### `parse` メソッドの内部動作について

以下に、提供いただいた `json.py` ファイル内の `JsonOutputParser` クラスの `parse` メソッドに該当する文字列が入力された際に、どのような順番で整形（パース）されていくのか、各操作で何が起こるのかを詳細に説明します。

#### 1. `parse` メソッドの呼び出し

```python
def parse(self, text: str) -> Any:
    """Parse the output of an LLM call to a JSON object.

    Args:
        text: The output of the LLM call.

    Returns:
        The parsed JSON object.
    """
    return self.parse_result([Generation(text=text)])
```

- **入力**: LLM（大規模言語モデル）からの出力テキスト `text`。
- **動作**: 入力テキストを `Generation` オブジェクトとしてラップし、`parse_result` メソッドに渡します。

#### 2. `parse_result` メソッドの実行

```python
def parse_result(self, result: List[Generation], *, partial: bool = False) -> Any:
    """Parse the result of an LLM call to a JSON object.

    Args:
        result: The result of the LLM call.
        partial: Whether to parse partial JSON objects.
            If True, the output will be a JSON object containing
            all the keys that have been returned so far.
            If False, the output will be the full JSON object.
            Default is False.

    Returns:
        The parsed JSON object.

    Raises:
        OutputParserException: If the output is not valid JSON.
    """
    text = result[0].text
    text = text.strip()
    if partial:
        try:
            return parse_json_markdown(text)
        except JSONDecodeError:
            return None
    else:
        try:
            return parse_json_markdown(text)
        except JSONDecodeError as e:
            msg = f"Invalid json output: {text}"
            raise OutputParserException(msg, llm_output=text) from e
```

- **入力**: `Generation` オブジェクトのリスト `result` とオプションのパラメータ `partial`。
- **動作の流れ**:
  1. **テキストの抽出と整形**:
     - `result` リストの最初の要素からテキストを取得し、前後の空白文字を削除します。
     ```python
     text = result[0].text
     text = text.strip()
     ```
  2. **部分パース（`partial=True`）**:
     - `partial` が `True` の場合、`parse_json_markdown` 関数を用いてテキストをパースします。
     - パースに失敗した場合は `None` を返します。
     ```python
     if partial:
         try:
             return parse_json_markdown(text)
         except JSONDecodeError:
             return None
     ```
  3. **完全パース（`partial=False`）**:
     - `partial` が `False` の場合も同様に `parse_json_markdown` 関数を用いますが、パースに失敗した場合は `OutputParserException` を投げます。
     ```python
     else:
         try:
             return parse_json_markdown(text)
         except JSONDecodeError as e:
             msg = f"Invalid json output: {text}"
             raise OutputParserException(msg, llm_output=text) from e
     ```

#### 3. `parse_json_markdown` 関数の実行

```python
def parse_json_markdown(
    json_string: str, *, parser: Callable[[str], Any] = parse_partial_json
) -> dict:
    """Parse a JSON string from a Markdown string.

    Args:
        json_string: The Markdown string.

    Returns:
        The parsed JSON object as a Python dictionary.
    """
    try:
        return _parse_json(json_string, parser=parser)
    except json.JSONDecodeError:
        # Try to find JSON string within triple backticks
        match = _json_markdown_re.search(json_string)

        # If no match found, assume the entire string is a JSON string
        if match is None:
            json_str = json_string
        else:
            # If match found, use the content within the backticks
            json_str = match.group(2)
    return _parse_json(json_str, parser=parser)
```

- **入力**: 整形されたテキスト `json_string` とオプションのパーサ関数 `parser`（デフォルトは `parse_partial_json`）。
- **動作の流れ**:
  1. **全体をJSONとしてパースを試みる**:
     - `_parse_json` 関数を用いて、まず入力全体をJSONとしてパースします。
     - 成功すればその結果を返します。
     ```python
     try:
         return _parse_json(json_string, parser=parser)
     except json.JSONDecodeError:
         ...
     ```
  2. **JSONパースに失敗した場合**:
     - 入力テキスト中からマークダウン形式のJSONコードブロック（```json ... ```）を正規表現で検索します。
     ```python
     match = _json_markdown_re.search(json_string)
     ```
     - **マッチが見つからない場合**:
       - 入力全体を再度JSONとしてパースします（おそらく失敗し、例外が発生する可能性があります）。
       ```python
       if match is None:
           json_str = json_string
       ```
     - **マッチが見つかった場合**:
       - バックティック内のJSON部分のみを抽出し、パースします。
       ```python
       else:
           json_str = match.group(2)
       ```
  3. **再度JSONパースを試みる**:
     - 抽出した `json_str` を `_parse_json` 関数でパースし、結果を返します。
     ```python
     return _parse_json(json_str, parser=parser)
     ```

#### 4. `_parse_json` 関数の実行

```python
def _parse_json(
    json_str: str, *, parser: Callable[[str], Any] = parse_partial_json
) -> dict:
    # Strip whitespace,newlines,backtick from the start and end
    json_str = json_str.strip(_json_strip_chars)

    # handle newlines and other special characters inside the returned value
    json_str = _custom_parser(json_str)

    # Parse the JSON string into a Python dictionary
    return parser(json_str)
```

- **入力**: 整形されたJSON文字列 `json_str` とオプションのパーサ関数 `parser`。
- **動作の流れ**:
  1. **前後の不要な文字の削除**:
     - 空白文字や改行、バックティック（`）、などの不要な文字を文字列の先頭と末尾から削除します。
     ```python
     json_str = json_str.strip(_json_strip_chars)
     ```
  2. **特殊文字の処理**:
     - `_custom_parser` 関数を用いて、改行やタブ、引用符などの特殊文字を適切にエスケープします。
     - これにより、JSONとして正しい形式に整形されます。
     ```python
     json_str = _custom_parser(json_str)
     ```
  3. **JSONのパース**:
     - パーサ関数（デフォルトは `parse_partial_json`）を用いて、整形されたJSON文字列をPythonの辞書オブジェクトに変換します。
     ```python
     return parser(json_str)
     ```

#### 5. 具体的な処理例

例えば、以下のような入力テキストが `parse` メソッドに渡された場合を考えます。

```plaintext
1. aiueo ```json{"key": "value"}```
```

**処理の流れ**:

1. **`parse` メソッドの呼び出し**:
   - 入力テキスト `"1. aiueo ```json{"key": "value"}```"` が `parse` メソッドに渡されます。
   - `Generation` オブジェクトとしてラップされ、`parse_result` が呼び出されます。

2. **`parse_result` メソッド**:
   - テキストから前後の空白を削除します（今回の例では不要）。
   - `partial` がデフォルトの `False` であるため、`parse_json_markdown` が呼び出されます。

3. **`parse_json_markdown` 関数**:
   - まず、全体をJSONとしてパースを試みます。この場合、 `"1. aiueo ```json{"key": "value"}```"` は有効なJSONではないため、`JSONDecodeError` が発生します。
   - 次に、正規表現 `_json_markdown_re` を用いてマークダウン内のJSONブロックを検索します。
     - 現在の正規表現では、具体的なパターンにマッチしない可能性が高く、JSONブロックが適切に抽出されない場合があります。
   - JSONブロックが抽出できなかった場合、元のテキスト全体を再度JSONとしてパースしようとします。この試行でも失敗し、「1」が有効なJSON数値として認識され、パースが成功する可能性があります（ただし、末尾の不正なテキストは無視されるか、エラーとなることがあります）。

4. **結果**:
   - パースが成功した場合、例えば `"1"` が返されることがあります。
   - しかし、期待する `{"key": "value"}` ではなく、先頭の数字 `1` だけがパース結果として返されるため、問題が発生します。

#### 6. 根本原因

- **JSONブロックの適切な抽出が行われていない**:
  - 現在の正規表現 `_json_markdown_re` は、マークダウン形式のJSONブロックを正確に抽出するのに不十分です。そのため、JSONブロックが見つからないまま全体をパースしようとし、先頭の `1` が有効なJSON数値として認識されてしまいます。
  
- **パースの順序が適切でない**:
  - まず全体をパースしようとするため、部分的なJSONブロックが存在してもそれを無視してしまう。
  
#### 7. 解決策

上記の問題を解決するためには、以下のような対策が有効です。

1. **正規表現の修正**:
   - JSONブロックを正確に抽出するために、正規表現を改善します。
   - 例えば、以下のように修正します。
     ```python
     _json_markdown_re = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)
     ```
     - これにより、 ```json``` の後に続く `{` から `}` までのJSONオブジェクトを非貪欲にマッチさせます。

2. **パースの順序の変更**:
   - まずJSONブロックを抽出し、それをパースするように順序を変更します。
   - これにより、不要なプレフィックスや番号付きリストの影響を排除できます。

3. **カスタムパーサの導入**:
   - 出力形式が多様な場合に対応できるよう、柔軟なカスタムパーサを実装します。
   - 例えば、番号付きリストや複数のJSONブロックに対応するパーサを作成します。

#### 8. 修正後の `parse_json_markdown` の例

以下に、正規表現を修正し、パースの順序を変更した `parse_json_markdown` 関数の実装例を示します。

```python:custom_parsers.py
import re
import json
from typing import Any, Callable
from langchain_core.exceptions import OutputParserException

# 修正した正規表現
_json_markdown_re = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)

def parse_json_markdown(
    json_string: str, *, parser: Callable[[str], Any] = parse_partial_json
) -> dict:
    """Parse a JSON string from a Markdown string."""
    # まずJSONコードブロックを検索
    match = _json_markdown_re.search(json_string)
    if match:
        json_str = match.group(1)
        try:
            return _parse_json(json_str, parser=parser)
        except json.JSONDecodeError as e:
            msg = f"無効なJSON出力: {json_str}"
            raise OutputParserException(msg, llm_output=json_str) from e
    else:
        # JSONコードブロックが見つからない場合、全体をパース
        try:
            return _parse_json(json_string, parser=parser)
        except json.JSONDecodeError as e:
            msg = f"有効なJSONコードブロックが見つかりません: {json_string}"
            raise OutputParserException(msg, llm_output=json_string) from e
```

- **変更点**:
  1. **正規表現の修正**:
     - JSONブロックを正確に抽出できるよう、正規表現を改善しました。
  2. **パースの順序変更**:
     - まずJSONコードブロックを抽出し、それをパースします。
     - JSONコードブロックが見つからない場合のみ、全体をパースしようとします。

#### 9. まとめ

`JsonOutputParser` クラスの `parse` メソッドにおいて、先頭の「1」が有効なJSONとして認識されてしまう原因は、以下の通りです。

1. **不適切な正規表現によるJSONブロックの抽出失敗**:
   - 現在の正規表現 `_json_markdown_re` がJSONコードブロックを正確に抽出できておらず、結果として全体をパースしようとするため、先頭の数値が有効なJSONとして認識されてしまう。

2. **パースの順序が不適切**:
   - まず全体をパースしようとするため、部分的なJSONブロックの存在を無視してしまう。

**解決策**としては、正規表現の改善とパースの順序変更、及び必要に応じてカスタムパーサの導入が挙げられます。これにより、LLMの出力形式に柔軟に対応し、期待するJSONデータを正確に取得できるようになります。

今後、`JsonOutputParser` を使用する際には、出力形式に応じて適切にパーサをカスタマイズすることを推奨します。これにより、安定したデータパースとエラーの回避が可能となります。