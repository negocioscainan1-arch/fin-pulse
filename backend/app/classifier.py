import hashlib
from datetime import datetime, timezone

BANKS = {
    "Itaú": ["itaú","itau","rede","iti","ion"],
    "Nubank": ["nubank","nu holdings","roxinho"],
    "Bradesco": ["bradesco","next"],
    "Santander": ["santander"],
    "Banco do Brasil": ["banco do brasil","bb"],
    "Fintechs": ["fintech","pagbank","picpay","mercado pago","inter","c6"],
    "Global": ["visa","mastercard","stripe","jpmorgan","fed","global","finextra"]
}

TOPICS = {
    "cartões": ["cartão","cartões","cartoes","card","cards","interchange"],
    "Pix": ["pix"],
    "pagamentos": ["pagamento","pagamentos","payments","wallet","maquininha","adquirência","rede","tpv"],
    "crédito": ["crédito","credito","inadimplência","npl","pdd","provisão","cobrança"],
    "fraude": ["fraude","golpe","scam","phishing","chargeback","contestação","disputa"],
    "resultados": ["lucro","roe","receita","resultado","balanço","margem financeira"],
    "regulação": ["banco central","bacen","regulação","cvm"],
    "IA": ["ia","ai","inteligência artificial","machine learning","genai"]
}

def make_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:16]

def classify(title: str, summary: str = ""):
    text = f"{title} {summary}".lower()
    banks = [bank for bank, terms in BANKS.items() if any(t in text for t in terms)]
    topics = [topic for topic, terms in TOPICS.items() if any(t in text for t in terms)]
    score = 0.25 + 0.16 * len(banks) + 0.1 * len(topics)
    if "itaú" in text or "itau" in text:
        score += 0.18
    if any(t in text for t in ["pix","cartão","cartões","fraude","inadimplência","resultado","banco central"]):
        score += 0.18
    score = min(1, score)
    if score > .82:
        impact = "critical"
    elif score > .62:
        impact = "high"
    elif score > .42:
        impact = "medium"
    else:
        impact = "low"
    return banks or ["Setor"], topics or ["bancos"], score, impact
