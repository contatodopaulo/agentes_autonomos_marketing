"""
Agente Escritor
Responsável por gerar blog posts baseados em títulos
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from agente_escritor.config import PROMPT_ESCRITOR

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def gerar_blog_post(titulo: str) -> str:
    """
    Gera um blog post baseado no título fornecido.
    
    Args:
        titulo: Título do blog post a ser criado
        
    Returns:
        str: Conteúdo do blog post em formato markdown
    """
    print(f"\n{'='*60}")
    print(f"📝 AGENTE ESCRITOR: Gerando blog post")
    print(f"{'='*60}")
    print(f"Título: {titulo}")
    print(f"Processando...")
    
    try:
        # Preparar prompt
        prompt = PROMPT_ESCRITOR.format(titulo=titulo)
        
        # Chamar API da OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um escritor profissional de conteúdo de marketing digital. Sempre retorne o conteúdo em formato markdown."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        blog_post = response.choices[0].message.content
        
        print(f"✅ Blog post gerado com sucesso!")
        print(f"📊 Tamanho aproximado: {len(blog_post)} caracteres")
        
        return blog_post
        
    except Exception as e:
        print(f"❌ Erro ao gerar blog post: {str(e)}")
        raise

