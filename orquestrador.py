"""
Orquestrador Principal
Coordena a execução sequencial dos 4 agentes de IA
"""

import os
import pandas as pd
from pathlib import Path
from agente_escritor import gerar_blog_post
from agente_editor import revisar_blog_post
from agente_revisor import aplicar_revisoes
from agente_linkedin import gerar_post_linkedin


def sanitizar_titulo(titulo: str) -> str:
    """
    Sanitiza um título para ser usado como nome de arquivo.
    
    Args:
        titulo: Título original
        
    Returns:
        str: Título sanitizado
    """
    # Remove caracteres especiais e espaços
    sanitizado = titulo.lower()
    sanitizado = sanitizado.replace(" ", "_")
    sanitizado = sanitizado.replace("ç", "c")
    sanitizado = sanitizado.replace("á", "a")
    sanitizado = sanitizado.replace("à", "a")
    sanitizado = sanitizado.replace("â", "a")
    sanitizado = sanitizado.replace("ã", "a")
    sanitizado = sanitizado.replace("é", "e")
    sanitizado = sanitizado.replace("ê", "e")
    sanitizado = sanitizado.replace("í", "i")
    sanitizado = sanitizado.replace("ó", "o")
    sanitizado = sanitizado.replace("ô", "o")
    sanitizado = sanitizado.replace("õ", "o")
    sanitizado = sanitizado.replace("ú", "u")
    sanitizado = sanitizado.replace("ü", "u")
    
    # Remove caracteres especiais restantes
    caracteres_permitidos = "abcdefghijklmnopqrstuvwxyz0123456789_"
    sanitizado = "".join(c for c in sanitizado if c in caracteres_permitidos)
    
    # Remove underscores múltiplos
    while "__" in sanitizado:
        sanitizado = sanitizado.replace("__", "_")
    
    # Remove underscores no início e fim
    sanitizado = sanitizado.strip("_")
    
    return sanitizado


def salvar_arquivo(conteudo: str, caminho: Path):
    """
    Salva conteúdo em um arquivo markdown.
    
    Args:
        conteudo: Conteúdo a ser salvo
        caminho: Caminho do arquivo
    """
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"💾 Arquivo salvo: {caminho}")


def processar_blog_post(titulo: str, indice: int, total: int):
    """
    Processa um blog post completo através de todos os agentes.
    
    Args:
        titulo: Título do blog post
        indice: Índice atual (1-based)
        total: Total de posts a processar
    """
    print(f"\n{'#'*60}")
    print(f"# PROCESSANDO BLOG POST {indice}/{total}")
    print(f"{'#'*60}")
    print(f"Título: {titulo}\n")
    
    # Sanitizar título para nome de arquivo
    titulo_sanitizado = sanitizar_titulo(titulo)
    
    try:
        # Etapa 1: Agente Escritor
        print(f"\n{'─'*60}")
        print(f"ETAPA 1/5: AGENTE ESCRITOR")
        print(f"{'─'*60}")
        blog_post_original = gerar_blog_post(titulo)
        
        # Salvar draft
        caminho_draft = Path("intermediarios/drafts") / f"{titulo_sanitizado}.md"
        salvar_arquivo(blog_post_original, caminho_draft)
        
        # Etapa 2: Agente Editor
        print(f"\n{'─'*60}")
        print(f"ETAPA 2/5: AGENTE EDITOR")
        print(f"{'─'*60}")
        feedback_editor = revisar_blog_post(blog_post_original)
        
        # Salvar feedback
        caminho_feedback = Path("intermediarios/feedbacks") / f"{titulo_sanitizado}.md"
        salvar_arquivo(feedback_editor, caminho_feedback)
        
        # Etapa 3: Agente Revisor
        print(f"\n{'─'*60}")
        print(f"ETAPA 3/5: AGENTE REVISOR")
        print(f"{'─'*60}")
        blog_post_revisado = aplicar_revisoes(blog_post_original, feedback_editor)
        
        # Salvar revisão intermediária
        caminho_revisao = Path("intermediarios/revisoes") / f"{titulo_sanitizado}.md"
        salvar_arquivo(blog_post_revisado, caminho_revisao)
        
        # Salvar blog post final
        caminho_final = Path("blog_posts_finais") / f"{titulo_sanitizado}.md"
        salvar_arquivo(blog_post_revisado, caminho_final)
        
        # Etapa 4: Agente LinkedIn
        print(f"\n{'─'*60}")
        print(f"ETAPA 4/5: AGENTE LINKEDIN")
        print(f"{'─'*60}")
        post_linkedin = gerar_post_linkedin(blog_post_revisado)
        
        # Salvar post do LinkedIn
        caminho_linkedin = Path("linkedin_posts") / f"{titulo_sanitizado}.md"
        salvar_arquivo(post_linkedin, caminho_linkedin)
        
        # Resumo final
        print(f"\n{'─'*60}")
        print(f"ETAPA 5/5: CONCLUSÃO")
        print(f"{'─'*60}")
        print(f"✅ Blog post '{titulo}' processado com sucesso!")
        print(f"📁 Arquivos gerados:")
        print(f"   - Draft: {caminho_draft}")
        print(f"   - Feedback: {caminho_feedback}")
        print(f"   - Revisão: {caminho_revisao}")
        print(f"   - Final: {caminho_final}")
        print(f"   - LinkedIn: {caminho_linkedin}")
        
    except Exception as e:
        print(f"\n{'─'*60}")
        print(f"❌ ERRO ao processar '{titulo}': {str(e)}")
        print(f"{'─'*60}")
        raise


def main():
    """
    Função principal que orquestra todo o processo.
    """
    print(f"\n{'='*60}")
    print(f"SISTEMA DE AGENTES AUTÔNOMOS DE MARKETING")
    print(f"{'='*60}\n")
    
    # Verificar se o arquivo CSV existe
    caminho_csv = Path("ideias.csv")
    if not caminho_csv.exists():
        print(f"❌ Erro: Arquivo 'ideias.csv' não encontrado!")
        print(f"   Crie um arquivo CSV com uma coluna chamada 'titulo'")
        return
    
    # Verificar API key
    if not os.getenv("OPENAI_API_KEY"):
        print(f"❌ Erro: Variável de ambiente 'OPENAI_API_KEY' não configurada!")
        print(f"   Configure a variável de ambiente ou crie um arquivo .env")
        return
    
    # Ler CSV
    print(f"📖 Lendo arquivo: {caminho_csv}")
    try:
        df = pd.read_csv(caminho_csv)
        
        if "titulo" not in df.columns:
            print(f"❌ Erro: Coluna 'titulo' não encontrada no CSV!")
            print(f"   Colunas encontradas: {', '.join(df.columns)}")
            return
        
        titulos = df["titulo"].dropna().tolist()
        total = len(titulos)
        
        if total == 0:
            print(f"⚠️  Nenhum título encontrado no CSV!")
            return
        
        print(f"✅ {total} título(s) encontrado(s) no CSV\n")
        
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {str(e)}")
        return
    
    # Processar cada título sequencialmente
    for indice, titulo in enumerate(titulos, start=1):
        try:
            processar_blog_post(titulo, indice, total)
            
            # Pausa entre posts (exceto no último)
            if indice < total:
                print(f"\n{'='*60}")
                print(f"⏸️  Pausa antes do próximo blog post...")
                print(f"{'='*60}\n")
                
        except Exception as e:
            print(f"\n{'='*60}")
            print(f"❌ ERRO CRÍTICO: Interrompendo processamento")
            print(f"{'='*60}")
            print(f"Erro: {str(e)}")
            break
    
    # Resumo final
    print(f"\n{'='*60}")
    print(f"🏁 PROCESSAMENTO CONCLUÍDO")
    print(f"{'='*60}")
    print(f"Total de blog posts processados: {indice}/{total}")
    print(f"\n📁 Estrutura de arquivos gerados:")
    print(f"   - intermediarios/drafts/      (rascunhos originais)")
    print(f"   - intermediarios/feedbacks/   (feedback do editor)")
    print(f"   - intermediarios/revisoes/    (versões revisadas)")
    print(f"   - blog_posts_finais/         (blog posts finais)")
    print(f"   - linkedin_posts/            (posts do LinkedIn)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

