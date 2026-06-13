from .config import settings

SYSTEM_PROMPT = '''
Você é um estrategista sênior de bancos, meios de pagamento, cartões, Pix, crédito, risco, canais digitais e concorrência.
Gere uma análise executiva em português do Brasil, clara, direta e útil para alguém do Itaú.
Sempre conecte as notícias com:
- Itaú
- Nubank e concorrentes
- cartões
- Pix
- pagamentos
- crédito
- risco/fraude/contestação
- eficiência operacional
- oportunidades e ameaças
Responda em JSON válido.
'''

def fallback_analysis(news):
    top_topics = sorted({t for n in news for t in n.get("topic_tags", [])})
    top_banks = sorted({b for n in news for b in n.get("bank_tags", [])})
    return {
        "headline": "Pulso bancário atualizado: dados, pagamentos e concorrência seguem no centro da disputa",
        "executive_summary": (
            "As notícias mais relevantes indicam que a competição bancária segue migrando para frequência de uso, "
            "cartões, Pix, pagamentos, prevenção a fraude, crédito e eficiência operacional. Para o Itaú, o tema central "
            "é defender principalidade enquanto usa dados e IA para reduzir custo de servir e melhorar decisões."
        ),
        "itau_meaning": (
            "Para o Itaú, cada movimento do setor deve ser lido pelo impacto em share of wallet, uso do cartão, Pix, "
            "recorrência no app, inadimplência, contestação, fraude e custo operacional. A vantagem do banco está em combinar "
            "confiança, escala, portfólio e capacidade analítica."
        ),
        "risks": [
            "Nubank e fintechs capturarem frequência diária e dados transacionais.",
            "Aumento de golpes, fraude, chargebacks e disputas em canais digitais.",
            "Pressão de margem se crédito crescer com piora de inadimplência.",
            "Custo de servir elevado em jornadas confusas, especialmente cartões e contestação."
        ],
        "opportunities": [
            "IA para classificar notícias, atendimento, contestação e sinais de risco.",
            "Explicador de fatura, estorno, Pix e crédito provisório.",
            "Motor de autorização e limite mais contextual em cartões.",
            "Dashboard executivo para acompanhar concorrência, resultados e tendências por tema."
        ],
        "topics_detected": top_topics,
        "banks_detected": top_banks
    }

async def generate_analysis(news):
    if not settings.openai_api_key:
        return fallback_analysis(news)

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        compact_news = [
            {
                "title": n["title"],
                "source": n["source"],
                "summary": n.get("summary","")[:500],
                "banks": n.get("bank_tags", []),
                "topics": n.get("topic_tags", [])
            }
            for n in news[:20]
        ]
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.25,
            response_format={"type": "json_object"},
            messages=[
                {"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content":f"Gere o briefing executivo com base nestas notícias: {compact_news}"}
            ]
        )
        import json
        return json.loads(response.choices[0].message.content)
    except Exception as exc:
        print(f"AI failed: {exc}")
        return fallback_analysis(news)
