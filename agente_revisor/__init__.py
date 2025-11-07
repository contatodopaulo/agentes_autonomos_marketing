"""
Agente Revisor
Responsável por aplicar as sugestões do editor e gerar a versão final
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from agente_revisor.config import PROMPT_REVISOR

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def aplicar_revisoes(blog_post: str, feedback: str) -> str:
    """
    Aplica as sugestões do editor chefe ao blog post.
    
    Args:
        blog_post: Blog post original
        feedback: Feedback do editor chefe
        
    Returns:
        str: Blog post revisado em formato markdown
    """
    print(f"\n{'='*60}")
    print(f"🔍 AGENTE REVISOR: Aplicando revisões")
    print(f"{'='*60}")
    print(f"Processando sugestões do editor...")
    
    try:
        # Preparar prompt
        prompt = PROMPT_REVISOR.format(blog_post=blog_post, feedback=feedback)
        
        # Chamar API da OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um revisor final profissional. Sempre retorne apenas o conteúdo revisado em formato markdown, sem comentários ou explicações adicionais."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=2500
        )
        
        blog_post_revisado = response.choices[0].message.content
        
        print(f"✅ Revisões aplicadas com sucesso!")
        print(f"📊 Tamanho final: {len(blog_post_revisado)} caracteres")
        
        return blog_post_revisado
        
    except Exception as e:
        print(f"❌ Erro ao aplicar revisões: {str(e)}")
        raise

