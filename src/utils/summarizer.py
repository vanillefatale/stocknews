"""
Summarization utilities using Claude API.
"""

import os
from anthropic import Anthropic

def summarize_with_claude(text: str) -> str:
    """
    Summarize text using Claude API.
    
    Args:
        text (str): Text to summarize
        
    Returns:
        str: Summarized text
    """
    try:
        client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        
        prompt = (
            "역할: 너는 금융 뉴스 요약 전문가다.\n"
            "목표: 다음 뉴스의 핵심만 한 줄로 요약해줘.\n"
            "형식: 중립적인 어조로 작성.\n\n"
            f"---\n{text}\n---\n\n"
            "요약:"
        )
        
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=800,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return message.content[0].text.strip()
    except Exception as e:
        print(f"Error summarizing with Claude: {str(e)}")
        return "" 