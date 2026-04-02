from ..domain.schemas import AIProvider


def get_webchat_html() -> str:
    providers = [p.value for p in AIProvider]
    provider_options = "\n".join([f'<option value="{p}">{p.capitalize()}</option>' for p in providers])

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chat Cafetería Selecto Granos</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f8f9fa;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            .card {{
                width: min(780px, 95vw);
                border-radius: 12px;
                box-shadow: 0 1rem 2rem rgba(0,0,0,.12);
                background: #fff;
                padding: 1rem 1.1rem;
            }}
            h1 {{
                margin: 0 0 0.75rem 0;
                font-size: 1.4rem;
            }}
            .history {{
                height: 400px;
                overflow: auto;
                background: #fafbfc;
                border: 1px solid #e3e7eb;
                border-radius: 8px;
                padding: .8rem;
                margin-bottom: .8rem;
            }}
            .msg {{
                margin: .35rem 0;
                padding: .45rem .65rem;
                border-radius: 8px;
            }}
            .user {{
                background: #e2f1ff;
                align-self: flex-end;
            }}
            .bot {{
                background: #f2f2f7;
                align-self: flex-start;
            }}
            .input-group {{
                display: flex;
                gap: .5rem;
                align-items: center;
            }}
            input {{
                flex: 1;
                border: 1px solid #cfd6e4;
                border-radius: 8px;
                padding: .7rem;
                font-size: 1rem;
            }}
            select {{
                border: 1px solid #cfd6e4;
                border-radius: 8px;
                padding: .7rem;
                font-size: 1rem;
            }}
            button {{
                border: none;
                border-radius: 8px;
                background: #0078d4;
                color: #fff;
                padding: .7rem 1rem;
                cursor: pointer;
                font-weight: 700;
            }}
            button:disabled {{
                background: #8fbce6;
                cursor: not-allowed;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Chat Cafetería Selecto Granos ☕</h1>
            <div class="history" id="history"></div>
            <div class="input-group">
                <select id="provider">
                    {provider_options}
                </select>
                <input id="message" placeholder="Escribe tu pregunta..." />
                <button id="send">Enviar</button>
            </div>
        </div>
        <script>
            const history = document.getElementById('history');
            const message = document.getElementById('message');
            const send = document.getElementById('send');
            const provider = document.getElementById('provider');

            function appendBubble(text, origin) {{
                const div = document.createElement('div');
                div.className = 'msg ' + (origin === 'user' ? 'user' : 'bot');
                div.textContent = text;
                history.appendChild(div);
                history.scrollTop = history.scrollHeight;
            }}

            async function sendMessage() {{
                const text = message.value.trim();
                const selectedProvider = provider.value;
                if (!text) return;
                appendBubble('Tú: ' + text, 'user');
                message.value = '';
                send.disabled = true;
                appendBubble('Cargando...', 'bot');
                try {{
                    const res = await fetch('/chat', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{mensaje: text, provider: selectedProvider}})
                    }});
                    const data = await res.json();
                    history.lastChild.textContent = 'Bot: ' + (data.respuesta || 'No hay respuesta');
                }} catch (e) {{
                    history.lastChild.textContent = 'Bot: Error de conexión';
                }} finally {{
                    send.disabled = false;
                    message.focus();
                }}
            }}

            send.addEventListener('click', sendMessage);
            message.addEventListener('keydown', e => {{
                if (e.key === 'Enter') sendMessage();
            }});
        </script>
    </body>
    </html>
    """