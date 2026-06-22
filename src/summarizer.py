def gerar_resumo_extrativo(sentencas_originais, scores, taxa_compressao=0.3, formato="paragrafos"):
    # Define a quantidade de frases do resumo final
    qtd_frases = max(1, int(len(sentencas_originais) * taxa_compressao))
    
    frases_com_score = [
        (i, sentencas_originais[i], scores[i]) 
        for i in range(len(sentencas_originais))
    ]
    
    # Ordena para pegar os maiores scores primeiro
    frases_ordenadas_por_score = sorted(frases_com_score, key=lambda x: x[2], reverse=True)
    top_frases = frases_ordenadas_por_score[:qtd_frases]
    
    # Reordena as frases vencedoras pelo índice original (cronologia do documento)
    top_frases_cronologicas = sorted(top_frases, key=lambda x: x[0])
    
    # Estrutura o texto final baseado no formato escolhido
    if formato == "topicos":
        # Junta as frases adicionando um marcador de tópico e uma quebra de linha
        resumo_final = "\n".join([f"• {frase[1]}" for frase in top_frases_cronologicas])
    else:
        # Junta as frases adicionando duas quebras de linha (formando parágrafos separados)
        resumo_final = "\n\n".join([frase[1] for frase in top_frases_cronologicas])
    
    return resumo_final