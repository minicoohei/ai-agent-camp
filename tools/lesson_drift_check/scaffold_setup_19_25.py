#!/usr/bin/env python3
"""
Scaffold the 5 missing setup commands for module 19-25 (Discord/LINE
already exist from PR #59). Generates idempotent .claude + .cursor mirrored
files in 3 locales each = 30 files.

Usage:
    python3 tools/lesson_drift_check/scaffold_setup_19_25.py [--dry-run]
"""

from __future__ import annotations

import argparse
from pathlib import Path

# slug → (module_id, locale_blocks)
COMMANDS = {
    "setup-m365cli": {
        "module": 19,
        "service": "Microsoft 365 CLI (PnP CLI)",
        "noninteractive": "deferred",
        "ja": {
            "title": "M365 CLI セットアップ",
            "duration": "約20分",
            "service_desc": "Microsoft 365 (Outlook / SharePoint / Teams) を CLI からまとめて触る `@pnp/cli-microsoft365`。デバイスコード認証だけで完結します。",
            "highlight": "PAT 不要・OAuth デバイスコードのみ",
            "main_steps": [
                ("Node.js 18+ を確認", "node -v"),
                ("@pnp/cli-microsoft365 を pin install",
                 "npm install -g @pnp/cli-microsoft365@7.x"),
                ("デバイスコードでログイン",
                 "m365 login\\n# 出力された URL をブラウザで開いてコードを入力"),
                ("接続確認", "m365 status"),
            ],
            "pitfalls": [
                "ログインしたままにするには `m365 logout` を実行しないこと（Token 失効まで保持）",
                "WSL 環境では `m365 login` 出力 URL を Windows ブラウザで開く必要あり（自動 open は呼ばない）",
            ],
        },
        "en": {
            "title": "M365 CLI setup",
            "duration": "~20 min",
            "service_desc": "Drive Microsoft 365 (Outlook / SharePoint / Teams) from one CLI: `@pnp/cli-microsoft365`. Device-code auth, nothing else.",
            "highlight": "No PAT required — OAuth device code only",
            "main_steps": [
                ("Confirm Node.js 18+", "node -v"),
                ("Install @pnp/cli-microsoft365 (pinned)",
                 "npm install -g @pnp/cli-microsoft365@7.x"),
                ("Sign in via device code",
                 "m365 login\\n# Open the printed URL in your browser and enter the code"),
                ("Verify", "m365 status"),
            ],
            "pitfalls": [
                "Avoid running `m365 logout` if you want to stay signed in — the token persists until it expires",
                "On WSL, open the URL in your Windows browser (the CLI doesn't auto-launch a browser there)",
            ],
        },
        "es": {
            "title": "Setup de M365 CLI",
            "duration": "~20 min",
            "service_desc": "Maneja Microsoft 365 (Outlook / SharePoint / Teams) desde un único CLI: `@pnp/cli-microsoft365`. Auth por device code, nada más.",
            "highlight": "Sin PAT — solo OAuth device code",
            "main_steps": [
                ("Confirma Node.js 18+", "node -v"),
                ("Instala @pnp/cli-microsoft365 (versión fijada)",
                 "npm install -g @pnp/cli-microsoft365@7.x"),
                ("Inicia sesión con device code",
                 "m365 login\\n# Abre la URL impresa en el navegador e introduce el código"),
                ("Verifica", "m365 status"),
            ],
            "pitfalls": [
                "Evita `m365 logout` si quieres mantener la sesión — el token persiste hasta caducar",
                "En WSL, abre la URL en tu navegador de Windows (el CLI no lanza navegador allí)",
            ],
        },
    },
    "setup-freee": {
        "module": 20,
        "service": "Freee MCP",
        "noninteractive": "incompatible",
        "ja": {
            "title": "Freee MCP セットアップ",
            "duration": "約30分",
            "service_desc": "freee 会計に MCP 経由で接続。ブラウザ OAuth + Client ID/Secret が必要。",
            "highlight": "Freee Developer App + OAuth ブラウザログイン必須",
            "main_steps": [
                ("freee Developer Portal でアプリ作成", "https://app.secure.freee.co.jp/developers/applications"),
                ("Client ID / Client Secret を控える", "（Web ブラウザのみ）"),
                ("freee-mcp を pin install", "npm install -g freee-mcp@0.26.0"),
                ("Claude Code に MCP 登録",
                 "claude mcp add --transport stdio freee -- npx freee-mcp@0.26.0"),
                ("OAuth ブラウザフローで認可", "claude mcp の指示に従う"),
            ],
            "pitfalls": [
                "事業所 ID は `freee_get_companies` で取得 → `~/.config/freee-mcp/config.json` に保存",
                "Sandbox / 本番アプリは別物。Sandbox で試してから本番アプリに切り替え",
            ],
        },
        "en": {
            "title": "Freee MCP setup",
            "duration": "~30 min",
            "service_desc": "Connect to freee Accounting via MCP. Requires browser OAuth + Client ID/Secret.",
            "highlight": "Freee Developer App + browser OAuth login required",
            "main_steps": [
                ("Create an app in the freee Developer Portal", "https://app.secure.freee.co.jp/developers/applications"),
                ("Save Client ID / Client Secret", "(browser only)"),
                ("Install freee-mcp (pinned)", "npm install -g freee-mcp@0.26.0"),
                ("Register the MCP",
                 "claude mcp add --transport stdio freee -- npx freee-mcp@0.26.0"),
                ("Authorise via the OAuth browser flow", "follow the MCP prompts"),
            ],
            "pitfalls": [
                "Get your company ID via `freee_get_companies` → save to `~/.config/freee-mcp/config.json`",
                "Sandbox vs production apps are separate. Test in sandbox first, then swap to a production app",
            ],
        },
        "es": {
            "title": "Setup de Freee MCP",
            "duration": "~30 min",
            "service_desc": "Conéctate a freee Contabilidad vía MCP. Requiere OAuth de navegador + Client ID/Secret.",
            "highlight": "App en Freee Developer + OAuth de navegador obligatorio",
            "main_steps": [
                ("Crea una app en el Freee Developer Portal", "https://app.secure.freee.co.jp/developers/applications"),
                ("Guarda Client ID / Client Secret", "(solo navegador)"),
                ("Instala freee-mcp (versión fijada)", "npm install -g freee-mcp@0.26.0"),
                ("Registra el MCP",
                 "claude mcp add --transport stdio freee -- npx freee-mcp@0.26.0"),
                ("Autoriza con el flujo OAuth del navegador", "sigue las indicaciones del MCP"),
            ],
            "pitfalls": [
                "Obtén tu company ID con `freee_get_companies` → guárdalo en `~/.config/freee-mcp/config.json`",
                "Sandbox y producción son apps distintas. Prueba en sandbox y luego cambia a la app de producción",
            ],
        },
    },
    "setup-figma": {
        "module": 21,
        "service": "Figma + Serendie MCP",
        "noninteractive": "incompatible",
        "ja": {
            "title": "Figma + Serendie デザインシステム MCP セットアップ",
            "duration": "約20分",
            "service_desc": "Figma 公式プラグイン（書き込み担当）と Serendie MCP（知識担当）の 2 つを接続。",
            "highlight": "PAT 不要・OAuth ブラウザログインで完結",
            "main_steps": [
                ("Claude Code に Figma プラグインを導入",
                 "/plugin install figma@claude-plugins-official"),
                ("OAuth で Figma にログイン",
                 "/mcp → figma → Authenticate → ブラウザで Allow Access"),
                ("Serendie MCP を追加",
                 "claude mcp add --transport http serendie-mcp https://serendie.design/mcp"),
                ("動作確認", "claude mcp list"),
                ("Serendie UI Kit を Figma の自分のチームに取り込み",
                 "https://www.figma.com/community/file/1433690846108785966"),
            ],
            "pitfalls": [
                "Serendie UI Kit を Community からチームに移動しないと「ライブラリを公開」できない",
                "Figma OAuth は組織アカウントの場合、管理者が App 利用許可を出す必要あり",
            ],
        },
        "en": {
            "title": "Figma + Serendie design-system MCP setup",
            "duration": "~20 min",
            "service_desc": "Wire the official Figma plugin (the writer) and Serendie MCP (the knowledge source).",
            "highlight": "No PAT needed — OAuth browser login does it all",
            "main_steps": [
                ("Install the Figma plugin into Claude Code",
                 "/plugin install figma@claude-plugins-official"),
                ("Sign in to Figma via OAuth",
                 "/mcp → figma → Authenticate → 'Allow Access' in the browser"),
                ("Add the Serendie MCP",
                 "claude mcp add --transport http serendie-mcp https://serendie.design/mcp"),
                ("Verify", "claude mcp list"),
                ("Bring the Serendie UI Kit into your Figma team",
                 "https://www.figma.com/community/file/1433690846108785966"),
            ],
            "pitfalls": [
                "You can't 'Publish library' until you move the Serendie UI Kit from Community into your team",
                "On enterprise Figma accounts, an admin has to approve the app first",
            ],
        },
        "es": {
            "title": "Setup de Figma + Serendie MCP",
            "duration": "~20 min",
            "service_desc": "Conecta el plugin oficial de Figma (escritor) y Serendie MCP (fuente de conocimiento).",
            "highlight": "Sin PAT — login OAuth de navegador resuelve todo",
            "main_steps": [
                ("Instala el plugin Figma en Claude Code",
                 "/plugin install figma@claude-plugins-official"),
                ("Inicia sesión en Figma con OAuth",
                 "/mcp → figma → Authenticate → 'Allow Access' en el navegador"),
                ("Añade el MCP de Serendie",
                 "claude mcp add --transport http serendie-mcp https://serendie.design/mcp"),
                ("Verifica", "claude mcp list"),
                ("Lleva el Serendie UI Kit a tu equipo en Figma",
                 "https://www.figma.com/community/file/1433690846108785966"),
            ],
            "pitfalls": [
                "No podrás 'Publicar biblioteca' hasta mover el UI Kit de Community a tu equipo",
                "En cuentas Figma corporativas, un admin debe aprobar la app primero",
            ],
        },
    },
    "setup-salesforce": {
        "module": 24,
        "service": "Salesforce CLI (sf)",
        "noninteractive": "incompatible",
        "ja": {
            "title": "Salesforce CLI (sf) セットアップ",
            "duration": "約15分",
            "service_desc": "Salesforce 組織を CLI から触る `sf` コマンド。Connected App は不要、ブラウザ OAuth で完結。",
            "highlight": "Connected App 不要・ブラウザ OAuth のみ",
            "main_steps": [
                ("Salesforce CLI を pin install (npm 推奨)",
                 "npm install -g @salesforce/cli@2.x"),
                ("Production 組織にログイン", "sf org login web --alias prod"),
                ("Sandbox の場合", "sf org login web --alias dev --instance-url https://test.salesforce.com"),
                ("接続確認", "sf org list"),
            ],
            "pitfalls": [
                "`sf` v1 (`sfdx`) と v2 (`sf`) はコマンド体系が異なる。v2 を使うこと",
                "Sandbox は `--instance-url https://test.salesforce.com` を必ず付ける",
            ],
        },
        "en": {
            "title": "Salesforce CLI (sf) setup",
            "duration": "~15 min",
            "service_desc": "Drive Salesforce orgs from the `sf` CLI. No Connected App — browser OAuth is enough.",
            "highlight": "No Connected App — browser OAuth only",
            "main_steps": [
                ("Install Salesforce CLI (pinned, npm preferred)",
                 "npm install -g @salesforce/cli@2.x"),
                ("Sign in to Production", "sf org login web --alias prod"),
                ("For Sandbox", "sf org login web --alias dev --instance-url https://test.salesforce.com"),
                ("Verify", "sf org list"),
            ],
            "pitfalls": [
                "`sf` v1 (`sfdx`) and v2 (`sf`) have different commands — use v2",
                "Always pass `--instance-url https://test.salesforce.com` for Sandbox",
            ],
        },
        "es": {
            "title": "Setup de Salesforce CLI (sf)",
            "duration": "~15 min",
            "service_desc": "Maneja organizaciones Salesforce desde el CLI `sf`. Sin Connected App — basta OAuth de navegador.",
            "highlight": "Sin Connected App — solo OAuth de navegador",
            "main_steps": [
                ("Instala Salesforce CLI (versión fijada, npm recomendado)",
                 "npm install -g @salesforce/cli@2.x"),
                ("Inicia sesión en Producción", "sf org login web --alias prod"),
                ("Para Sandbox", "sf org login web --alias dev --instance-url https://test.salesforce.com"),
                ("Verifica", "sf org list"),
            ],
            "pitfalls": [
                "`sf` v1 (`sfdx`) y v2 (`sf`) tienen comandos distintos — usa v2",
                "Para Sandbox pon siempre `--instance-url https://test.salesforce.com`",
            ],
        },
    },
    "setup-google-ads": {
        "module": 25,
        "service": "Google Ads API",
        "noninteractive": "incompatible",
        "ja": {
            "title": "Google Ads API セットアップ",
            "duration": "約180分（API Center 承認待ちが大半）",
            "service_desc": "Google Ads API v21 (Python SDK) を叩くまでの 3 日間 journey。MCC + Basic Access + OAuth refresh_token が必要。",
            "highlight": "Basic Access 承認に最大 1 営業日。OAuth は web flow が必須",
            "main_steps": [
                ("Google Ads Manager Account (MCC) を作成",
                 "https://ads.google.com/aw/signup/manager"),
                ("API Center で Developer Token をリクエスト",
                 "MCC → Tools → API Center → Apply for Basic Access"),
                ("GCP プロジェクトと OAuth Client (web) を作成",
                 "https://console.cloud.google.com/apis/credentials"),
                ("refresh_token を取得 (web flow ローカル受信)",
                 "uv run python scripts/gtm/google_ads_oauth.py"),
                ("Keychain と GitHub Secrets に 5 つの値を保存",
                 "GOOGLE_ADS_DEVELOPER_TOKEN / CLIENT_ID / CLIENT_SECRET / REFRESH_TOKEN / LOGIN_CUSTOMER_ID"),
                ("Python SDK で疎通確認 (validate_only=True dry-run)",
                 "uv run python scripts/gtm/manage_google_ads.py --dry-run"),
            ],
            "pitfalls": [
                "Test Account からは課金広告は配信できない。Basic Access 承認後は本番アカウントを使う",
                "EU political advertising ステータスを campaign_operation に必須でセット (`DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING`)",
                "validate_only=True の dry-run でも `mutate` の atomic batch（budget+campaign with temp resource_name `-1`）にしないと resource_name 存在チェックで弾かれる",
            ],
        },
        "en": {
            "title": "Google Ads API setup",
            "duration": "~180 min (API Center approval is most of it)",
            "service_desc": "The 3-day journey to actually call Google Ads API v21 (Python SDK). You need MCC + Basic Access + OAuth refresh_token.",
            "highlight": "Basic Access approval can take a business day. OAuth must use the web flow",
            "main_steps": [
                ("Create a Google Ads Manager Account (MCC)",
                 "https://ads.google.com/aw/signup/manager"),
                ("Request a Developer Token in the API Center",
                 "MCC → Tools → API Center → Apply for Basic Access"),
                ("Create a GCP project and an OAuth Client (web)",
                 "https://console.cloud.google.com/apis/credentials"),
                ("Mint a refresh_token via the web flow (local listener)",
                 "uv run python scripts/gtm/google_ads_oauth.py"),
                ("Save the 5 secrets in Keychain + GitHub Secrets",
                 "GOOGLE_ADS_DEVELOPER_TOKEN / CLIENT_ID / CLIENT_SECRET / REFRESH_TOKEN / LOGIN_CUSTOMER_ID"),
                ("Smoke-test from the Python SDK (validate_only=True dry-run)",
                 "uv run python scripts/gtm/manage_google_ads.py --dry-run"),
            ],
            "pitfalls": [
                "Test Accounts can't run paid ads. Switch to a production account once Basic Access is granted",
                "Always set EU political advertising status on campaign_operation (`DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING`) — it's required",
                "Even with validate_only=True you must use a `mutate` atomic batch (budget + campaign with temp resource_name `-1`); otherwise the resource_name existence check fails",
            ],
        },
        "es": {
            "title": "Setup de Google Ads API",
            "duration": "~180 min (la mayoría es la aprobación del API Center)",
            "service_desc": "El viaje de 3 días para de verdad llamar a Google Ads API v21 (Python SDK). Necesitas MCC + Basic Access + refresh_token OAuth.",
            "highlight": "El Basic Access puede tardar un día hábil. El OAuth requiere flujo web",
            "main_steps": [
                ("Crea una Manager Account (MCC) de Google Ads",
                 "https://ads.google.com/aw/signup/manager"),
                ("Solicita el Developer Token en el API Center",
                 "MCC → Tools → API Center → Apply for Basic Access"),
                ("Crea un proyecto GCP y un OAuth Client (web)",
                 "https://console.cloud.google.com/apis/credentials"),
                ("Genera un refresh_token con el flujo web (listener local)",
                 "uv run python scripts/gtm/google_ads_oauth.py"),
                ("Guarda 5 secrets en Keychain + GitHub Secrets",
                 "GOOGLE_ADS_DEVELOPER_TOKEN / CLIENT_ID / CLIENT_SECRET / REFRESH_TOKEN / LOGIN_CUSTOMER_ID"),
                ("Prueba con el SDK de Python (dry-run validate_only=True)",
                 "uv run python scripts/gtm/manage_google_ads.py --dry-run"),
            ],
            "pitfalls": [
                "Los Test Accounts no pueden lanzar anuncios pagos. Cambia a producción cuando aprueben Basic Access",
                "Pon siempre el estado de EU political advertising en campaign_operation (`DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING`)",
                "Aun con validate_only=True hay que usar un batch atómico de `mutate` (budget + campaign con temp resource_name `-1`); si no, el chequeo de resource_name lo rechaza",
            ],
        },
    },
}


def render(slug: str, spec: dict, locale: str) -> str:
    block = spec[locale]
    mod = spec["module"]
    service = spec["service"]
    nim = spec["noninteractive"]
    title = block["title"]
    duration = block["duration"]
    service_desc = block["service_desc"]
    highlight = block["highlight"]
    steps = block["main_steps"]
    pitfalls = block["pitfalls"]

    if locale == "ja":
        labels = {
            "head": "セットアップ手順",
            "highlight": "ハイライト",
            "pitfalls": "つまずきポイント",
            "ni_section": "非対話モード",
            "see_also": "関連スライド",
        }
        ni_body = {
            "compliant": "`claude -p` / `cursor-agent --print` でもそのまま走ります（read-only 中心）。",
            "deferred": "ブラウザ操作と入力が必要なので、`claude -p` 実行時は読み取り系チェックのみ実施し、`setup-resume.md` を生成して終了します。",
            "incompatible": "ブラウザ OAuth が必須なので `claude -p` / `cursor-agent --print` では完走できません。対話モードで実行してください。",
        }[nim]
    elif locale == "en":
        labels = {
            "head": "Setup steps",
            "highlight": "Highlight",
            "pitfalls": "Gotchas",
            "ni_section": "Non-interactive mode",
            "see_also": "Related slides",
        }
        ni_body = {
            "compliant": "Runs cleanly under `claude -p` / `cursor-agent --print` (mostly read-only).",
            "deferred": "Browser interaction is required, so `-p` mode runs only the read-only checks then writes a `setup-resume.md` and exits.",
            "incompatible": "Browser OAuth is mandatory — cannot complete under `claude -p` / `cursor-agent --print`. Re-run in interactive mode.",
        }[nim]
    else:
        labels = {
            "head": "Pasos de setup",
            "highlight": "Punto clave",
            "pitfalls": "Tropezones",
            "ni_section": "Modo no interactivo",
            "see_also": "Slides relacionadas",
        }
        ni_body = {
            "compliant": "Funciona en `claude -p` / `cursor-agent --print` (mayormente read-only).",
            "deferred": "Necesita navegador, así que en modo `-p` solo ejecuta los chequeos read-only, escribe `setup-resume.md` y sale.",
            "incompatible": "El OAuth en navegador es obligatorio — no termina bajo `claude -p` / `cursor-agent --print`. Re-ejecuta en modo interactivo.",
        }[nim]

    fm = (
        f"---\n"
        f"description: \"Lesson command — {title}\"\n"
        f"duration: \"{duration}\"\n"
        f"prerequisites: [\"{service} アカウント\"]\n"
        f"level: \"intermediate\"\n"
        f"nonInteractiveMode: {nim}\n"
        f"tags: [\"setup\", \"module-{mod}\"]\n"
        f"---\n\n"
    )
    if locale == "ja":
        fm = fm.replace("アカウント", "アカウント")
    elif locale == "en":
        fm = fm.replace(f"{service} アカウント", f"{service} account")
    else:
        fm = fm.replace(f"{service} アカウント", f"cuenta de {service}")

    body = (
        f"# /{slug} -- {title}\n\n"
        f"> {service_desc}\n\n"
        f"**{labels['highlight']}**: {highlight}\n\n"
        f"## {labels['head']}\n\n"
    )
    for i, (label, cmd) in enumerate(steps, 1):
        cmd_block = cmd.replace("\\n", "\n")
        if "\n" in cmd_block or " " not in cmd_block.strip():
            body += f"{i}. {label}\n\n   ```bash\n   {cmd_block}\n   ```\n\n"
        else:
            body += f"{i}. {label} — `{cmd_block}`\n\n"
    body += f"## {labels['pitfalls']}\n\n"
    for p in pitfalls:
        body += f"- {p}\n"
    body += f"\n## {labels['ni_section']}\n\n{ni_body}\n\n"
    body += (
        f"## {labels['see_also']}\n\n"
        f"- aiagent-course Module {mod}: see slide deck for the full visual walkthrough\n"
    )
    return fm + body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    edited = skipped = 0
    for slug, spec in COMMANDS.items():
        for tree in (".claude", ".cursor"):
            for loc in ("ja", "en", "es"):
                ext = ".md" if loc == "ja" else f".{loc}.md"
                path = Path(f"{tree}/commands/lesson/{slug}{ext}")
                if path.exists():
                    skipped += 1
                    continue
                content = render(slug, spec, loc)
                print(f"+ {path}")
                if not args.dry_run:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content, encoding="utf-8")
                edited += 1
    print(f"\nedited={edited}, skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
