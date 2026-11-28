"""DeepSeek/OpenAI-compatible transport with usage-backed tracing, no key in browser."""
import json
import os
from pathlib import Path
import urllib.request
import urllib.error
from tracing import model_call

ROOT = Path(__file__).resolve().parents[1]


def load_env():
    path = ROOT / '.env'
    if path.exists():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip().strip('\"\''))


load_env()
MODEL_PROVIDER = os.environ.get('MODEL_PROVIDER', 'deepseek').strip().lower() or 'deepseek'
MODEL_NAME = os.environ.get('MODEL_NAME', 'deepseek-flash').strip() or 'deepseek-flash'


def model_status():
    key = os.environ.get('API_KEY') or os.environ.get('DEEPSEEK_API_KEY', '')
    return {'provider': MODEL_PROVIDER, 'model': MODEL_NAME,
            'ready': MODEL_PROVIDER != 'fake' and bool(key.strip()),
            'message': 'Đã cấu hình; kết nối được xác minh khi gọi model.' if key.strip() else 'Chưa có API key. Điền API_KEY trong starter-repo/.env rồi khởi động lại backend.'}


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == 'fake':
        return {'text': '[mock — chưa gọi model]', 'model': 'fake', 'tokens_in': 0, 'tokens_out': 0}
    if MODEL_PROVIDER not in ('deepseek', 'openai'):
        raise ValueError('Nhà cung cấp hỗ trợ: deepseek hoặc openai.')
    key = os.environ.get('API_KEY') or os.environ.get('DEEPSEEK_API_KEY', '')
    if not key.strip():
        raise ValueError('Chưa cấu hình API_KEY trong .env.')
    base = os.environ.get('API_BASE_URL') or ('https://api.deepseek.com' if MODEL_PROVIDER == 'deepseek' else 'https://api.openai.com/v1')
    body = {'model': MODEL_NAME, 'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
            'response_format': {'type': 'json_object'}, 'max_tokens': 4096, 'stream': False}
    if MODEL_PROVIDER == 'deepseek':
        body['thinking'] = {'type': 'disabled'}
    elif MODEL_PROVIDER == 'openai':
        body['max_completion_tokens'] = body.pop('max_tokens')
    req = urllib.request.Request(base.rstrip('/') + '/chat/completions', data=json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=75) as response:
            result = json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        messages = {401: 'API key không hợp lệ.', 402: 'Tài khoản model chưa đủ số dư.', 429: 'Nhà cung cấp đang giới hạn lượt gọi.'}
        raise RuntimeError(messages.get(error.code, f'Nhà cung cấp trả HTTP {error.code}; kiểm tra cấu hình rồi thử lại.')) from None
    except (urllib.error.URLError, TimeoutError):
        raise RuntimeError('Không kết nối được model trong thời gian cho phép.') from None
    content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError('Model trả nội dung rỗng; thử lại yêu cầu.')
    usage = result.get('usage', {})
    if not all(isinstance(usage.get(field), int) for field in ('prompt_tokens', 'completion_tokens')):
        raise RuntimeError('Phản hồi thiếu usage; không thể ghi token thực.')
    return {'text': content, 'model': result.get('model', MODEL_NAME),
            'tokens_in': usage['prompt_tokens'], 'tokens_out': usage['completion_tokens']}
