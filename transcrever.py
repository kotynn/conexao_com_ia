import json
import requests
import assemblyai as aai
import google.genai as genai
from google.genai import types
import traceback

# =========================
# 🔑 CONFIGURAÇÕES
# =========================
ASSEMBLY_KEY = "sua chave"  # Sua chave AssemblyAI
GEMINI_KEY = "sua chave"  # Sua chave Gemini
KANBAN_URL = "http:29838749283742"  # URL do seu backend Flask

if not GEMINI_KEY:
    raise RuntimeError("❌ A chave do Gemini não foi encontrada.")
if not ASSEMBLY_KEY:
    raise RuntimeError("❌ A chave da AssemblyAI não foi encontrada.")

# Configura AssemblyAI
aai.settings.api_key = ASSEMBLY_KEY
transcriber = aai.Transcriber()

def transcrever_audio(audio_file: str) -> str:
    print(f"📤 Transcrevendo arquivo: {audio_file}")
    try:
        transcript = transcriber.transcribe(audio_file, config=aai.TranscriptionConfig(language_code="pt"))
    except Exception as e:
        raise RuntimeError(f"❌ Erro ao transcrever o áudio: {e}")
    if transcript.error:
        raise RuntimeError(f"❌ Falha na transcrição: {transcript.error}")
    print("✅ Transcrição concluída.")
    return transcript.text

def analisar_texto(texto: str) -> str:
    client = genai.Client(api_key=GEMINI_KEY)
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=texto)],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=types.Schema(
            type=types.Type.OBJECT,
            required=["descricao", "status"],
            properties={
                "titulo": types.Schema(type=types.Type.STRING),
                "descricao": types.Schema(type=types.Type.STRING),
                "status": types.Schema(
                    type=types.Type.STRING,
                    enum=["criado", "atendido", "fechado"]
                ),
            },
        ),
    )
    print("🤖 Enviando texto para Gemini...")
    resposta_final = ""
    try:
        for chunk in client.models.generate_content_stream(
            model="gemini-2.0-flash-exp",
            contents=contents,
            config=generate_content_config,
        ):
            resposta_final += chunk.text or ""
    except Exception as e:
        raise RuntimeError(f"❌ Erro ao enviar texto para Gemini: {e}")
    print("✅ Resposta do Gemini recebida.")
    return resposta_final

def enviar_chamado_para_kanban(dados_json: str):
    print("📨 Enviando chamado para Kanban...")
    try:
        dados_dict = json.loads(dados_json)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"❌ Resposta do Gemini não é um JSON válido:\n{dados_json}\nErro: {e}")
    try:
        resposta = requests.post(
            KANBAN_URL,
            headers={"Content-Type": "application/json"},
            json=dados_dict
        )
        resposta.raise_for_status()
        print("✅ Chamado enviado com sucesso para o Kanban.")
    except requests.RequestException as e:
        raise RuntimeError(f"❌ Erro ao enviar chamado para o Kanban: {e}")

if __name__ == "__main__":
    caminho_audio = "/home/rafaelk/Downloads/tire a mão do meu peru dotor nefario.mp3"
    try:
        texto_transcrito = transcrever_audio(caminho_audio)
        print(f"\n📜 Texto transcrito:\n{texto_transcrito}")

        resposta_gemini = analisar_texto(texto_transcrito)
        print("\n📦 Resposta do Gemini AI (JSON puro esperado):")
        print(resposta_gemini)

        enviar_chamado_para_kanban(resposta_gemini)

    except Exception as e:
        print("\n❌ Ocorreu um erro no processo:")
        print(e)
        traceback.print_exc()
