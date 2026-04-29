"""FlowCash email HTML templates — inline-styled, responsive, email-client safe."""
from datetime import datetime

# ── Brand tokens (mirrors design/tokens.jsx) ──────────────────────────────────
_C = {
    "indigo":      "#7B5CFF",
    "indigoDeep":  "#4B2EFF",
    "teal":        "#2EE6CA",
    "coral":       "#FF5E7A",
    "amber":       "#FFB545",
    "bgDark":      "#0B0B14",
    "bgDark2":     "#12121F",
    "bgLight":     "#F6F5FB",
    "bgLight2":    "#ECEBF5",
    "white":       "#FFFFFF",
}

# Media queries injected into every email.
# - fc-outer  : outer wrapper <td> padding
# - fc-header : header <td> padding / border-radius
# - fc-body   : body <td> padding
# - fc-footer : footer <td> padding / border-radius
# - fc-title  : main heading font-size
# - fc-otp    : OTP digit string — font-size + letter-spacing shrink on narrow screens
# - fc-col    : left column of a 2-col feature grid — stacks to full-width block
# - fc-col-r  : right column (last in row, retains bottom margin when stacked)
# - fc-col-end: absolute-last feature card — removes trailing bottom margin
_MEDIA = f"""
<style type="text/css">
  /* ── Reset ── */
  body, table, td, p, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
  img {{ border: 0; outline: none; text-decoration: none; }}

  @media only screen and (max-width: 620px) {{
    /* Outer wrapper */
    .fc-outer  {{ padding: 16px 8px 36px !important; }}

    /* Card sections */
    .fc-header {{ padding: 28px 16px 22px !important;
                  border-radius: 14px 14px 0 0 !important; }}
    .fc-body   {{ padding: 24px 18px 24px !important; }}
    .fc-footer {{ padding: 18px 16px 22px !important;
                  border-radius: 0 0 14px 14px !important; }}

    /* Typography */
    .fc-title  {{ font-size: 18px !important; letter-spacing: -0.3px !important; }}

    /* OTP code — shrink so 6 digits + spaces fit on 320 px */
    .fc-otp    {{ font-size: 28px !important;
                  letter-spacing: 5px !important;
                  padding-right: 5px !important; }}

    /* Feature grid — stack columns */
    .fc-col     {{ display: block !important; width: 100% !important;
                   padding: 0 0 10px 0 !important; box-sizing: border-box !important; }}
    .fc-col-r   {{ display: block !important; width: 100% !important;
                   padding: 0 0 10px 0 !important; box-sizing: border-box !important; }}
    .fc-col-end {{ display: block !important; width: 100% !important;
                   padding: 0 !important; box-sizing: border-box !important; }}
  }}
</style>"""


def _logo() -> str:
    return f"""
<table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center">
  <tr>
    <td align="center" width="64" height="64"
        bgcolor="{_C['indigoDeep']}"
        style="background:linear-gradient(135deg,{_C['indigoDeep']} 0%,{_C['indigo']} 50%,{_C['teal']} 100%);
               border-radius:19px;width:64px;height:64px;">
      <span style="display:block;color:#ffffff;font-size:30px;font-weight:800;
                   font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;
                   line-height:64px;text-align:center;letter-spacing:-1px;">F</span>
    </td>
  </tr>
</table>
<p style="margin:14px 0 4px;font-size:26px;font-weight:700;letter-spacing:-0.8px;color:#ffffff;
          font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;">FlowCash</p>
<p style="margin:0;font-size:13px;color:#AABBCC;">Your money, finally in flow.</p>"""


def _header() -> str:
    return f"""
<tr>
  <td class="fc-header" align="center"
      bgcolor="{_C['indigoDeep']}"
      style="background:linear-gradient(135deg,{_C['indigoDeep']} 0%,{_C['indigo']} 50%,{_C['teal']} 100%);
             padding:36px 32px 30px;border-radius:20px 20px 0 0;">
    {_logo()}
  </td>
</tr>"""


def _footer() -> str:
    year = datetime.now().year
    return f"""
<tr>
  <td class="fc-footer" align="center"
      bgcolor="{_C['bgDark2']}"
      style="background-color:{_C['bgDark2']};padding:24px 32px 28px;
             border-radius:0 0 20px 20px;">
    <p style="margin:0 0 8px;font-size:12px;color:{_C['teal']};font-weight:600;
              letter-spacing:0.4px;">FlowCash</p>
    <p style="margin:0 0 6px;font-size:11px;color:#667788;line-height:1.6;">
      Este es un correo autom&#225;tico. Por favor no respondas a este mensaje.
    </p>
    <p style="margin:0;font-size:11px;color:#445566;">
      &copy; {year} FlowCash. Todos los derechos reservados.
    </p>
  </td>
</tr>"""


def _wrap(rows: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <meta name="color-scheme" content="light">
  <meta name="supported-color-schemes" content="light">
  <title>FlowCash</title>
  {_MEDIA}
</head>
<body style="margin:0;padding:0;background-color:{_C['bgLight']};
             font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;
             -webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;">
  <!--[if mso]>
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
    <tr><td>
  <![endif]-->
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"
         bgcolor="{_C['bgLight']}" style="background-color:{_C['bgLight']};">
    <tr>
      <td class="fc-outer" align="center" style="padding:40px 16px 56px;">
        <!--[if mso]>
        <table role="presentation" width="560" cellspacing="0" cellpadding="0" border="0" align="center">
          <tr><td>
        <![endif]-->
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"
               style="max-width:560px;width:100%;">
          {rows}
        </table>
        <!--[if mso]>
          </td></tr>
        </table>
        <![endif]-->
      </td>
    </tr>
  </table>
  <!--[if mso]>
    </td></tr>
  </table>
  <![endif]-->
</body>
</html>"""


# ── Feature card helper (used by welcome_html) ────────────────────────────────

def _feature_card(emoji: str, title: str, desc: str, bg: str, color: str) -> str:
    return f"""
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
  <tr>
    <td bgcolor="{bg}"
        style="background-color:{bg};border-radius:14px;padding:16px 14px;">
      <p style="margin:0 0 4px;font-size:20px;">{emoji}</p>
      <p style="margin:0 0 2px;font-size:13px;font-weight:700;color:{color};">{title}</p>
      <p style="margin:0;font-size:12px;color:{color}99;line-height:1.4;">{desc}</p>
    </td>
  </tr>
</table>"""


# ── Public templates ───────────────────────────────────────────────────────────

def verification_code_html(name: str, code: str, ttl_minutes: int = 15) -> str:
    """Verification email with 6-digit OTP code."""
    # "123456" → "123 456" with non-breaking space; trailing padding-right offsets letter-spacing clip
    formatted = f"{code[:3]}&nbsp;{code[3:]}" if len(code) == 6 else code
    body = f"""
<tr>
  <td class="fc-body" bgcolor="{_C['white']}"
      style="background-color:{_C['white']};padding:40px 32px 36px;">

    <p class="fc-title"
       style="margin:0 0 6px;font-size:22px;font-weight:700;color:{_C['bgDark']};
              letter-spacing:-0.5px;line-height:1.2;">
      Hola, {name} &#128075;
    </p>
    <p style="margin:0 0 28px;font-size:15px;color:#555570;line-height:1.65;">
      Usa el siguiente c&#243;digo para verificar tu cuenta de FlowCash.
      El c&#243;digo expira en <strong>{ttl_minutes}&nbsp;minutos</strong>.
    </p>

    <!-- OTP code box -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
      <tr>
        <td align="center" bgcolor="#F0EEFF"
            style="background-color:#F0EEFF;border-radius:16px;
                   border:2px solid {_C['indigo']};padding:26px 16px;">
          <p style="margin:0 0 10px;font-size:11px;font-weight:600;color:{_C['indigo']};
                    letter-spacing:2.5px;text-transform:uppercase;">
            C&#211;DIGO DE VERIFICACI&#211;N
          </p>
          <p class="fc-otp"
             style="margin:0;font-size:44px;font-weight:800;color:{_C['indigoDeep']};
                    letter-spacing:10px;padding-right:10px;
                    font-family:'Courier New',Courier,monospace;
                    word-break:break-all;">
            {formatted}
          </p>
        </td>
      </tr>
    </table>

    <!-- Expiry notice -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"
           style="margin-top:14px;">
      <tr>
        <td bgcolor="#FFF8ED"
            style="background-color:#FFF8ED;border-radius:12px;
                   border-left:4px solid {_C['amber']};padding:13px 15px;">
          <p style="margin:0;font-size:13px;color:#886600;line-height:1.5;">
            &#9201; Este c&#243;digo expira en
            <strong>{ttl_minutes}&nbsp;minutos</strong>.
            Si no lo usas a tiempo, solicita uno nuevo.
          </p>
        </td>
      </tr>
    </table>

    <p style="margin:22px 0 0;font-size:12px;color:#9090AA;line-height:1.65;
              border-top:1px solid {_C['bgLight2']};padding-top:18px;">
      &#128274; Si no solicitaste este c&#243;digo, ignora este correo.
      Tu cuenta permanece segura. FlowCash nunca compartir&#225; tu c&#243;digo.
    </p>
  </td>
</tr>"""
    return _wrap(_header() + body + _footer())


def password_reset_html(name: str, code: str, ttl_minutes: int = 60) -> str:
    """Password reset email with OTP code."""
    formatted = f"{code[:3]}&nbsp;{code[3:]}" if len(code) == 6 else code
    body = f"""
<tr>
  <td class="fc-body" bgcolor="{_C['white']}"
      style="background-color:{_C['white']};padding:40px 32px 36px;">

    <p class="fc-title"
       style="margin:0 0 4px;font-size:22px;font-weight:700;color:{_C['bgDark']};
              letter-spacing:-0.5px;line-height:1.2;">
      Restablecer contrase&#241;a
    </p>
    <p style="margin:0 0 4px;font-size:15px;font-weight:600;color:{_C['bgDark']};">
      Hola, {name}
    </p>
    <p style="margin:0 0 28px;font-size:15px;color:#555570;line-height:1.65;">
      Recibimos una solicitud para restablecer la contrase&#241;a de tu cuenta.
      Usa el c&#243;digo a continuaci&#243;n. Expira en
      <strong>{ttl_minutes}&nbsp;minutos</strong>.
    </p>

    <!-- OTP code box -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
      <tr>
        <td align="center" bgcolor="#FFF0F3"
            style="background-color:#FFF0F3;border-radius:16px;
                   border:2px solid {_C['coral']};padding:26px 16px;">
          <p style="margin:0 0 10px;font-size:11px;font-weight:600;color:{_C['coral']};
                    letter-spacing:2.5px;text-transform:uppercase;">
            C&#211;DIGO DE RESTABLECIMIENTO
          </p>
          <p class="fc-otp"
             style="margin:0;font-size:44px;font-weight:800;color:#CC2244;
                    letter-spacing:10px;padding-right:10px;
                    font-family:'Courier New',Courier,monospace;
                    word-break:break-all;">
            {formatted}
          </p>
        </td>
      </tr>
    </table>

    <!-- Expiry notice -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"
           style="margin-top:14px;">
      <tr>
        <td bgcolor="#FFF8ED"
            style="background-color:#FFF8ED;border-radius:12px;
                   border-left:4px solid {_C['amber']};padding:13px 15px;">
          <p style="margin:0;font-size:13px;color:#886600;line-height:1.5;">
            &#9201; Este c&#243;digo expira en
            <strong>{ttl_minutes}&nbsp;minutos</strong>.
          </p>
        </td>
      </tr>
    </table>

    <!-- Security warning -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"
           style="margin-top:10px;">
      <tr>
        <td bgcolor="#FFF0F3"
            style="background-color:#FFF0F3;border-radius:12px;
                   border-left:4px solid {_C['coral']};padding:13px 15px;">
          <p style="margin:0;font-size:13px;color:#CC3355;line-height:1.5;">
            &#128680; Si no solicitaste este cambio, ignora este correo o
            contacta soporte de inmediato. Tu contrase&#241;a no cambiar&#225;
            hasta que uses este c&#243;digo.
          </p>
        </td>
      </tr>
    </table>

    <p style="margin:22px 0 0;font-size:12px;color:#9090AA;line-height:1.65;
              border-top:1px solid {_C['bgLight2']};padding-top:18px;">
      &#128274; FlowCash nunca te pedir&#225; tu contrase&#241;a por correo.
    </p>
  </td>
</tr>"""
    return _wrap(_header() + body + _footer())


def welcome_html(name: str) -> str:
    """Welcome email sent after successful account verification."""
    # Feature grid: 2 columns on desktop, stacked single column on mobile.
    # Each <td> gets a fc-col / fc-col-r / fc-col-end class so @media can
    # set display:block + width:100% to force single-column stacking.
    reportes   = _feature_card("&#128202;", "Reportes",    "Visualiza tus gastos por categor&#237;a.", "#F0EEFF", _C["indigoDeep"])
    balance    = _feature_card("&#128176;", "Balance",     "Controla ingresos y egresos.",            "#E8FBF8", "#008870")
    categorias = _feature_card("&#127991;", "Categor&#237;as", "Organiza tus transacciones.",         "#FFF0F3", _C["coral"])
    alertas    = _feature_card("&#128276;", "Alertas",     "Mant&#233;nte al tanto de tus l&#237;mites.", "#FFFBED", "#996600")

    body = f"""
<tr>
  <td class="fc-body" bgcolor="{_C['white']}"
      style="background-color:{_C['white']};padding:40px 32px 36px;">

    <p class="fc-title"
       style="margin:0 0 6px;font-size:24px;font-weight:700;color:{_C['bgDark']};
              letter-spacing:-0.5px;line-height:1.2;">
      &#127881; &#161;Bienvenido a FlowCash, {name}!
    </p>
    <p style="margin:0 0 26px;font-size:15px;color:#555570;line-height:1.65;">
      Tu cuenta ha sido verificada exitosamente. Ya puedes comenzar a
      gestionar tus finanzas personales de forma inteligente.
    </p>

    <!-- Feature grid: 2-col desktop / 1-col mobile -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
      <tr>
        <td class="fc-col" width="50%"
            style="width:50%;padding:0 6px 10px 0;vertical-align:top;">
          {reportes}
        </td>
        <td class="fc-col-r" width="50%"
            style="width:50%;padding:0 0 10px 6px;vertical-align:top;">
          {balance}
        </td>
      </tr>
      <tr>
        <td class="fc-col" width="50%"
            style="width:50%;padding:0 6px 0 0;vertical-align:top;">
          {categorias}
        </td>
        <td class="fc-col-end" width="50%"
            style="width:50%;padding:0 0 0 6px;vertical-align:top;">
          {alertas}
        </td>
      </tr>
    </table>

    <p style="margin:26px 0 0;font-size:13px;color:#9090AA;line-height:1.65;
              border-top:1px solid {_C['bgLight2']};padding-top:18px;">
      &#128075; &#191;Tienes preguntas? Estamos aqu&#237; para ayudarte.
    </p>
  </td>
</tr>"""
    return _wrap(_header() + body + _footer())
