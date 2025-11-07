"""
Agente Editor
Responsável por revisar blog posts e fornecer feedback estruturado
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from agente_editor.config import PROMPT_EDITOR

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def revisar_blog_post(blog_post: str) -> str:
    """
    Revisa um blog post e retorna feedback estruturado.
    
    Args:
        blog_post: Conteúdo do blog post a ser revisado
        
    Returns:
        str: Feedback estruturado em formato markdown
    """
    print(f"\n{'='*60}")
    print(f"✏️  AGENTE EDITOR: Revisando blog post")
    print(f"{'='*60}")
    print(f"Analisando conteúdo...")
    
    try:
        # Preparar prompt
        prompt = PROMPT_EDITOR.format(blog_post=blog_post)
        
        # Chamar API da OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um editor chefe experiente e profissional. Sempre forneça feedback estruturado, construtivo e detalhado em formato markdown."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=2000
        )
        
        feedback = response.choices[0].message.content
        
        print(f"✅ Revisão concluída!")
        print(f"📊 Feedback gerado: {len(feedback)} caracteres")
        
        return feedback
        
    except Exception as e:
        print(f"❌ Erro ao revisar blog post: {str(e)}")
        raise

