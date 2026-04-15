# Configuración de GitHub Secrets para CI/CD

Este documento explica cómo configurar los secretos necesarios en GitHub para que el pipeline de CI/CD funcione correctamente.

## Pasos para agregar Secrets en GitHub

1. Ve a tu repositorio en GitHub
2. Haz clic en **Settings** → **Secrets and variables** → **Actions**
3. Haz clic en **New repository secret**
4. Ingresa el nombre del secret y su valor
5. Hace clic en **Add secret**

## Secrets Requeridos

### Vercel Deployment

- **`VERCEL_TOKEN`**
  - Descripción: Token de autenticación de Vercel
  - Cómo obtenerlo:
    1. Ve a [https://vercel.com/account/tokens](https://vercel.com/account/tokens)
    2. Crea un nuevo token (Scope: Full Account)
    3. Copia el valor

- **`VERCEL_ORG_ID`**
  - Descripción: ID de tu organización en Vercel
  - Cómo obtenerlo:
    1. Ve a [https://vercel.com/account/general](https://vercel.com/account/general)
    2. Busca "Team ID" en Project Settings
    3. Copia el valor

- **`VERCEL_PROJECT_ID` (Backend)**
  - Descripción: ID del proyecto backend en Vercel
  - Cómo obtenerlo:
    1. Deploy el backend a Vercel primero
    2. Ve al proyecto → Settings → General
    3. Busca "Project ID"

- **`VERCEL_FRONTEND_PROJECT_ID` (Frontend)**
  - Descripción: ID del proyecto frontend en Vercel
  - Cómo obtenerlo:
    1. Deploy el frontend a Vercel primero
    2. Ve al proyecto → Settings → General
    3. Busca "Project ID"

- **`VERCEL_SCOPE`**
  - Descripción: Scope de tu cuenta Vercel (normalmente tu username)
  - Ejemplo: `danielmartinezp` o `my-org`

### APIs de IA (Opcionales en Docker)

Estos secrets se usan durante el build para validar que las claves están correctas.

- **`GOOGLE_API_KEY`**
  - Descripción: API Key de Google Gemini
  - Cómo obtenerlo: [Google AI Studio](https://aistudio.google.com/app/apikey)

- **`OPENAI_API_KEY`**
  - Descripción: API Key de OpenAI
  - Cómo obtenerlo: [OpenAI Dashboard](https://platform.openai.com/account/api-keys)

- **`ANTHROPIC_API_KEY`**
  - Descripción: API Key de Anthropic Claude
  - Cómo obtenerlo: [Anthropic Console](https://console.anthropic.com/account/keys)

- **`DEEPSEEK_API_KEY`**
  - Descripción: API Key de DeepSeek
  - Cómo obtenerlo: [DeepSeek API](https://platform.deepseek.com/)

### Variables de Entorno del Frontend

- **`NEXT_PUBLIC_API_URL`**
  - Descripción: URL del backend (visible en el cliente)
  - Ejemplo: `https://api.example.com` o `http://localhost:8000`
  - Nota: Prefijo `NEXT_PUBLIC_` la hace disponible en el navegador

## Script de Configuración Rápida

Si tienes acceso al CLI de GitHub, puedes automatizar:

```bash
#!/bin/bash
# script-secrets.sh

REPO_OWNER="tu-usuario"
REPO_NAME="NeoCafeIA"

gh secret set VERCEL_TOKEN --body "$(cat ~/.vercel/token)" -R $REPO_OWNER/$REPO_NAME
gh secret set VERCEL_ORG_ID --body "tu-org-id" -R $REPO_OWNER/$REPO_NAME
gh secret set VERCEL_PROJECT_ID --body "tu-backend-project-id" -R $REPO_OWNER/$REPO_NAME
gh secret set VERCEL_FRONTEND_PROJECT_ID --body "tu-frontend-project-id" -R $REPO_OWNER/$REPO_NAME
gh secret set VERCEL_SCOPE --body "tu-username" -R $REPO_OWNER/$REPO_NAME
gh secret set GOOGLE_API_KEY --body "tu-google-key" -R $REPO_OWNER/$REPO_NAME
gh secret set OPENAI_API_KEY --body "tu-openai-key" -R $REPO_OWNER/$REPO_NAME
gh secret set ANTHROPIC_API_KEY --body "tu-anthropic-key" -R $REPO_OWNER/$REPO_NAME
gh secret set DEEPSEEK_API_KEY --body "tu-deepseek-key" -R $REPO_OWNER/$REPO_NAME
gh secret set NEXT_PUBLIC_API_URL --body "https://api.example.com" -R $REPO_OWNER/$REPO_NAME
```

```bash
chmod +x script-secrets.sh
./script-secrets.sh
```

## Validación del Pipeline

Una vez configurados los secrets:

1. Haz push a `main` branch
2. Ve a **Actions** en tu repositorio
3. Verifica que el workflow `Deploy to Vercel` está corriendo
4. Espera a que se complete (normalmente 5-10 minutos)
5. Si todo es verde ✅, tu aplicación está desplegada en Vercel

## Troubleshooting

### Error: "Secret not found"
- Verifica que el nombre del secret es exacto
- Los nombres son case-sensitive

### Error: "Invalid Vercel token"
- Regenera el token en [https://vercel.com/account/tokens](https://vercel.com/account/tokens)
- Asegúrate de tener permisos de Full Account

### Error: "Project ID not found"
- Verifica que el proyecto existe en Vercel
- Copia el ID exacto de Settings → General

### Build falla por falta de API keys
- Las API keys no son críticas para el build
- El workflow tiene `continue-on-error: true` para validaciones opcionales
- Pero sí son necesarias para ejecutar la aplicación en producción

## Referencias

- [Documentación de GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Documentación de Vercel CI/CD](https://vercel.com/docs/concepts/git)
- [GitHub Actions para Vercel](https://github.com/marketplace/actions/vercel-action)
