"""
Serviços de Notificação
Envio de alertas por E-mail e WhatsApp
"""

import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class EmailNotifier:
    """Envia notificações por e-mail"""
    
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', 'alertas@sistema.com')
        self.enabled = bool(self.smtp_user and self.smtp_password)
    
    def send(self, to_email: str, subject: str, alert_data: Dict) -> bool:
        """Envia e-mail de notificação"""
        if not self.enabled:
            logger.warning("⚠ E-mail não configurado, notificação ignorada")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            # HTML formatado
            html_body = self._create_html_body(alert_data)
            msg.attach(MIMEText(html_body, 'html'))
            
            # Enviar e-mail
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"✓ E-mail enviado para {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"✗ Erro ao enviar e-mail: {e}")
            return False
    
    def _create_html_body(self, alert_data: Dict) -> str:
        """Cria HTML formatado para o e-mail"""
        severity_colors = {
            'critical': '#dc2626',
            'high': '#f97316',
            'medium': '#eab308',
            'low': '#3b82f6'
        }
        
        severity_labels = {
            'critical': 'CRÍTICO',
            'high': 'ALTO',
            'medium': 'MÉDIO',
            'low': 'BAIXO'
        }
        
        severity = alert_data.get('severity', 'medium')
        color = severity_colors.get(severity, '#6b7280')
        label = severity_labels.get(severity, 'MÉDIO')
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ 
                    background: linear-gradient(135deg, {color} 0%, {color}cc 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 8px 8px 0 0;
                }}
                .severity-badge {{
                    display: inline-block;
                    padding: 5px 15px;
                    background: rgba(255,255,255,0.2);
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                .content {{ 
                    background: #f9fafb;
                    padding: 30px;
                    border-radius: 0 0 8px 8px;
                    border: 1px solid #e5e7eb;
                }}
                .alert-info {{ 
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                .label {{ 
                    color: #6b7280;
                    font-size: 12px;
                    text-transform: uppercase;
                    font-weight: 600;
                    margin-bottom: 5px;
                }}
                .value {{ 
                    color: #111827;
                    font-size: 16px;
                    margin-bottom: 15px;
                }}
                .footer {{ 
                    text-align: center;
                    color: #6b7280;
                    font-size: 12px;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #e5e7eb;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 24px;
                    background: {color};
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: 600;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0 0 10px 0;">🚨 Novo Alerta</h1>
                    <span class="severity-badge">{label}</span>
                </div>
                <div class="content">
                    <div class="alert-info">
                        <div class="label">Cliente</div>
                        <div class="value">{alert_data.get('client_name', 'N/A')}</div>
                        
                        <div class="label">Tipo de Alerta</div>
                        <div class="value">{alert_data.get('alert_type', 'N/A').replace('_', ' ').title()}</div>
                        
                        <div class="label">Título</div>
                        <div class="value"><strong>{alert_data.get('title', 'N/A')}</strong></div>
                        
                        <div class="label">Descrição</div>
                        <div class="value">{alert_data.get('description', 'N/A')}</div>
                    </div>
                    
                    <a href="http://localhost:3000/alerts" class="button">
                        Ver no Dashboard →
                    </a>
                </div>
                <div class="footer">
                    <p>Este é um alerta automático do Sistema de Monitoramento</p>
                    <p>Para parar de receber essas notificações, acesse as configurações do sistema</p>
                </div>
            </div>
        </body>
        </html>
        """


class WhatsAppNotifier:
    """Envia notificações por WhatsApp"""
    
    def __init__(self):
        self.api_url = os.getenv('WHATSAPP_API_URL', '')
        self.api_token = os.getenv('WHATSAPP_API_TOKEN', '')
        self.enabled = bool(self.api_url and self.api_token)
    
    def send(self, phone: str, alert_data: Dict) -> bool:
        """Envia mensagem via WhatsApp API"""
        if not self.enabled:
            logger.warning("⚠ WhatsApp não configurado, notificação ignorada")
            return False
        
        try:
            message = self._format_message(alert_data)
            
            headers = {
                'Authorization': f'Bearer {self.api_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'phone': phone,
                'message': message
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"✓ WhatsApp enviado para {phone}")
                return True
            else:
                logger.error(f"✗ Erro WhatsApp: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"✗ Erro ao enviar WhatsApp: {e}")
            return False
    
    def _format_message(self, alert_data: Dict) -> str:
        """Formata mensagem para WhatsApp"""
        severity_emoji = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🔵'
        }
        
        emoji = severity_emoji.get(alert_data.get('severity', 'medium'), '⚠️')
        
        return f"""
{emoji} *ALERTA DO SISTEMA*

*Cliente:* {alert_data.get('client_name', 'N/A')}
*Tipo:* {alert_data.get('alert_type', 'N/A').replace('_', ' ').title()}
*Severidade:* {alert_data.get('severity', 'N/A').upper()}

*{alert_data.get('title', 'N/A')}*

{alert_data.get('description', 'N/A')}

_Acesse o dashboard para mais detalhes_
        """.strip()


class NotificationManager:
    """Gerencia envio de notificações por múltiplos canais"""
    
    def __init__(self, db_manager):
        self.db = db_manager
        self.email_notifier = EmailNotifier()
        self.whatsapp_notifier = WhatsAppNotifier()
    
    def send_alert_notification(self, alert_data: Dict, 
                                channels: Optional[List[str]] = None) -> Dict[str, bool]:
        """Envia notificação do alerta pelos canais especificados"""
        if channels is None:
            channels = ['email']  # Default
        
        results = {}
        
        # E-mail
        if 'email' in channels:
            # Em produção, buscar e-mail do cliente do BD
            recipient_email = self._get_client_email(alert_data.get('client_id'))
            
            subject = f"[{alert_data.get('severity', 'MEDIUM').upper()}] {alert_data.get('title', 'Alerta')}"
            
            success = self.email_notifier.send(
                recipient_email,
                subject,
                alert_data
            )
            results['email'] = success
            
            # Registrar notificação
            self._log_notification(
                alert_data.get('_id'),
                'email',
                recipient_email,
                'sent' if success else 'failed'
            )
        
        # WhatsApp
        if 'whatsapp' in channels:
            phone = self._get_client_phone(alert_data.get('client_id'))
            
            success = self.whatsapp_notifier.send(phone, alert_data)
            results['whatsapp'] = success
            
            self._log_notification(
                alert_data.get('_id'),
                'whatsapp',
                phone,
                'sent' if success else 'failed'
            )
        
        return results
    
    def _get_client_email(self, client_id: str) -> str:
        """Busca e-mail do cliente (simulado)"""
        # Em produção, buscar do banco de dados
        return f"suporte@{client_id.lower()}.com"
    
    def _get_client_phone(self, client_id: str) -> str:
        """Busca telefone do cliente (simulado)"""
        # Em produção, buscar do banco de dados
        return "+5511999999999"
    
    def _log_notification(self, alert_id: Optional[str], 
                         notif_type: str, recipient: str, status: str):
        """Registra notificação enviada"""
        if not alert_id:
            return
        
        log_data = {
            'alert_id': alert_id,
            'notification_type': notif_type,
            'recipient': recipient,
            'status': status,
            'origin': 'NotificationManager',
            'level': 'INFO' if status == 'sent' else 'ERROR',
            'message': f"Notificação {status}: {notif_type} para {recipient}"
        }
        
        self.db.insert_log(log_data)
