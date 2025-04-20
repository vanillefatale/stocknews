"""
Translation utilities using Claude API.
"""

import os
from anthropic import Anthropic


def translate_with_claude(text: str) -> str:
    """
    Translate text from English to Korean using Claude API.
    
    Args:
        text (str): English text to translate
        
    Returns:
        str: Translated Korean text
    """
    try:
        client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        prompt = (
            "다음 영문 텍스트를 한국어로 번역해주세요.\n"
            "번역 규칙:\n"
            "1. 핵심 내용만 한 줄로 간단히 번역하세요.\n"
            "2. 불필요한 설명이나 부가 정보는 제외하세요.\n"
            "3. 번역문 앞뒤로 따옴표나 기호를 붙이지 마세요.\n"
            "4. '~이다', '~하다' 등의 문장으로 끝나지 않도록 자연스럽게 마무리하세요.\n\n"
            f"{text}"
        )
        
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=800,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return message.content[0].text.strip()
    except Exception as e:
        print(f"Error translating with Claude: {str(e)}")
        return "" 