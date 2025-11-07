"""
Agente LinkedIn
Responsável por gerar posts do LinkedIn baseados em blog posts
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from agente_linkedin.config import PROMPT_LINKEDIN

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def gerar_post_linkedin(blog_post_final: str) -> str:
    """
    Gera um post do LinkedIn baseado no blog post final.
    
    Args:
        blog_post_final: Blog post final revisado
        
    Returns:
        str: Post do LinkedIn em formato markdown
    """
    print(f"\n{'='*60}")
    print(f"💼 AGENTE LINKEDIN: Gerando post para LinkedIn")
    print(f"{'='*60}")
    print(f"Adaptando conteúdo para LinkedIn...")
    
    try:
        # Preparar prompt
        prompt = PROMPT_LINKEDIN.format(blog_post=blog_post_final)
        
        # Chamar API da OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um especialista em criação de conteúdo profissional para LinkedIn. Sempre retorne o conteúdo em formato markdown, otimizado para engajamento no LinkedIn."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        post_linkedin = response.choices[0].message.content
        
        print(f"✅ Post do LinkedIn gerado com sucesso!")
        print(f"📊 Tamanho: {len(post_linkedin)} caracteres")
        
        return post_linkedin
        
    except Exception as e:
        print(f"❌ Erro ao gerar post do LinkedIn: {str(e)}")
        raise

