# agent-rules-kit

CLI local para diagnosticar la calidad mínima de archivos de instrucciones para agentes IA en repositorios.

Estado actual: inception local. No hay release, no hay remoto y no hay promesas de producción.

## Propósito

`agent-rules-kit` ayuda a revisar archivos como `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, reglas de Cursor e instrucciones de GitHub Copilot para detectar ausencias, duplicación, contradicciones básicas y riesgos operativos.

## Límites v0.1

- Read-only por defecto.
- Sin red.
- Sin LLM.
- Sin ejecutar comandos del repositorio analizado.
- Sin modificar archivos salvo modo explícito futuro.
- Sin prometer seguridad total.
- Hallazgos de secretos siempre redactados.

## Licencia

MIT.
