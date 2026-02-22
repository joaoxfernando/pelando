import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from bot import escapar_markdown, escapar_html


def test_escapar_markdown():
    texto = "Testando *asterisco* e _sublinhado_"
    esperado = "Testando \\*asterisco\\* e \\_sublinhado\\_"
    assert escapar_markdown(texto) == esperado

def test_escapar_html():
    texto = 'Texto com <tags> e "aspas"'
    esperado = 'Texto com &lt;tags&gt; e &quot;aspas&quot;'
    assert escapar_html(texto) == esperado