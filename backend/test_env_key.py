from services.ai_analyzer import AIAnalyzer


analyzer = AIAnalyzer()
print('openai_client is set:', analyzer.openai_client)
print('api_key present:', analyzer.api_key)
if analyzer.api_key:
    print('masked key:', analyzer.api_key[:6] + '...' + analyzer.api_key[-4:])
