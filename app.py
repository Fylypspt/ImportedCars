from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, User, Quote
from datetime import datetime
from dotenv import load_dotenv
import os, requests

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')

db.init_app(app)
with app.app_context():
    db.create_all()


# -------------------------
# Funções utilitárias
# -------------------------
def parse_float(value, default=0.0):
    if value is None:
        return default
    try:
        return float(str(value).replace(',', '.'))
    except:
        return default

def parse_int(value, default=None):
    if value is None or value == '':
        return default
    try:
        return int(float(str(value)))
    except:
        return default

# -------------------------
# Routes
# -------------------------
@app.route('/')
def index():
    return render_template('index.html', year=datetime.now().year)

@app.route('/orcamento', methods=['GET', 'POST'])
def orcamento():
    if request.method == 'POST':
        # Recebe dados do formulário
        username = request.form.get('username', '').strip()
        phone = request.form.get('phone', '').strip()
        carro_info = request.form.get('carro_info', '').strip()
        condition = request.form.get('condition', '').strip()
        color = request.form.get('color', '').strip()
        cilindrada = request.form.get('cilindrada', '').strip()
        ano = request.form.get('ano', '').strip()
        combustivel = request.form.get('combustivel', '').strip()

        # Validação mínima
        if not phone or not carro_info:
            flash('Por favor insere o número de telefone e informação do carro.', 'danger')
            return redirect(url_for('orcamento'))

        # Cria ou atualiza o utilizador
        user = User.query.filter_by(phone=phone).first()
        if not user:
            user = User(username=username or None, phone=phone)
            db.session.add(user)
            db.session.commit()
        else:
            if username:
                user.username = username
                db.session.commit()

        # Cria a cotação
        quote = Quote(
            user_id=user.id,
            car_info=carro_info,
            condition=condition,
            color=color,
            cilindrada=cilindrada,
            ano=ano,
            combustivel=combustivel
        )
        db.session.add(quote)
        db.session.commit()

        # Monta detalhes para WhatsApp (num único parâmetro)
        detalhes = (
            f"Carro: {carro_info}\n"
            f"Condição: {condition or 'não especificada'}\n"
            f"Cor: {color or 'não especificada'}\n"
            f"Cilindrada: {cilindrada or 'não especificada'}\n"
            f"Ano: {ano or 'não especificado'}\n"
            f"Combustível: {combustivel or 'não especificado'}\n"
            f"Contacto: {user.phone}"
        )

        # ======================
        # ENVIO PARA WHATSAPP (TEMPLATE)
        # ======================
        token = os.environ.get("WHATSAPP_TOKEN")
        phone_id = os.environ.get("WHATSAPP_PHONE_ID")
        owner_phone = os.environ.get("OWNER_PHONE")

        if not token or not phone_id or not owner_phone:
            raise ValueError("Credenciais WhatsApp não configuradas (WHATSAPP_TOKEN / WHATSAPP_PHONE_ID / OWNER_PHONE)")

        url = f"https://graph.facebook.com/v22.0/{phone_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": owner_phone,
            "type": "template",
            "template": {
                "name": "info_update2",  # <-- nome do template que vais criar
                "language": {"code": "pt_PT"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": user.username or "Cliente"},
                            {"type": "text", "text": detalhes}
                        ]
                    }
                ]
            }
        }
        headers = {"Authorization": f"Bearer {token}"}

        r = requests.post(url, json=payload, headers=headers)
        print("Resposta WhatsApp:", r.json())

        print("=== Mensagem enviada via template ===")
        print(detalhes)
        print("========================")

        return render_template('sent.html', message=detalhes, year=datetime.now().year)

    # GET request
    return render_template('quote.html', year=datetime.now().year)

@app.route('/calcular')
def calcular():
    return render_template('calcular.html', year=datetime.now().year)

if __name__ == '__main__':
    app.run(debug=True)