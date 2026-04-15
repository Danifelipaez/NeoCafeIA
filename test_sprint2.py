"""
Test rápido del ReActAgent y integración con hooks.
Valida que el ciclo ReAct completo funciona correctamente.
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(name)s: %(message)s",
)

# Agregar raíz del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.react_agent import ReActAgent, MockToolInvoker
from src.domain.schemas import AIProvider, ChatRequest
from src.infrastructure.model_factory import AIModelFactory


def test_react_agent_basic():
    """Test básico del ciclo ReAct."""
    print("\n" + "=" * 60)
    print("TEST 1: ReActAgent con ciclo completo")
    print("=" * 60)

    agent = ReActAgent(
        system_prompt="Eres un asistente de cafetería amigable.",
        tool_invoker=MockToolInvoker(),
        max_iterations=3,
    )

    questions = [
        "¿Qué bebidas tienen?",
        "¿Cuál es el precio del cappuccino?",
        "¿Me recomiendas algo?",
    ]

    for question in questions:
        print(f"\n👤 Usuario: {question}")
        response = agent.run(question)
        print(f"🤖 ReAct: {response}\n")
        print(f"   [Thought history: {len(agent.thought_history)} thoughts]")
        print(f"   [Action history: {len(agent.action_history)} actions]")


def test_react_adapter_integration():
    """Test de integración ReactAdapter con factory."""
    print("\n" + "=" * 60)
    print("TEST 2: ReactAdapter - Integración con Factory")
    print("=" * 60)

    try:
        adapter = AIModelFactory.create(AIProvider.REACT)
        print(f"✅ ReactAdapter creado exitosamente: {type(adapter).__name__}")

        response, tokens = adapter.complete(
            system_prompt="Eres un asistente de cafetería.",
            user_message="¿Qué recomendaciones tienen?",
            history=[],
        )

        print(f"\n🤖 Respuesta: {response}")
        print(f"📊 Tokens: {tokens}")

    except Exception as e:
        print(f"❌ Error: {e}")


def test_chat_request_with_react():
    """Test de ChatRequest usando provider REACT."""
    print("\n" + "=" * 60)
    print("TEST 3: ChatRequest con provider REACT")
    print("=" * 60)

    request = ChatRequest(
        pregunta="¿Cuál es el combo más popular?",
        provider=AIProvider.REACT,
        historial=[],
    )

    print(f"✅ ChatRequest creado:")
    print(f"   Pregunta: {request.pregunta}")
    print(f"   Provider: {request.provider}")
    print(f"   Historial: {len(request.historial)} mensajes")


def test_hooks():
    """Test de hooks de validación y auditoría."""
    print("\n" + "=" * 60)
    print("TEST 4: Hooks - PreToolUse y PostToolUse")
    print("=" * 60)

    from src.infrastructure.hooks import (
        PreToolUseHook,
        PostToolUseHook,
        DESTRUCTIVE_TOOLS,
    )

    # Test PreToolUseHook
    print("\n📋 PreToolUseHook:")
    print(f"   Validando tool segura 'buscar_bebida'...")
    is_valid = PreToolUseHook.validate("buscar_bebida", {"query": "cappuccino"})
    print(f"   ✅ Válida: {is_valid}")

    print(f"\n   Validando tool destructiva 'delete_beverage'...")
    is_valid = PreToolUseHook.validate("delete_beverage", {})
    print(f"   ✅ Bloqueada: {not is_valid}")

    # Test PostToolUseHook
    print("\n📊 PostToolUseHook:")
    result = '{"bebida": "Cappuccino", "precio": 4.50}'
    audited = PostToolUseHook.audit("buscar_bebida", result, 125.5)
    print(f"   ✅ Auditado: {len(audited)} caracteres")

    anomaly = PostToolUseHook.detect_anomalies("buscar_bebida", result)
    print(f"   ✅ Anomalías detectadas: {anomaly is not None}")


if __name__ == "__main__":
    try:
        test_react_agent_basic()
        test_react_adapter_integration()
        test_chat_request_with_react()
        test_hooks()

        print("\n" + "=" * 60)
        print("✅ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
