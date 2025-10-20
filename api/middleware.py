
import logging
from django.conf import settings
import time

request_logger = logging.getLogger('request_logger')

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = None
        exception = None

        try:
            response = self.get_response(request)
        except Exception as e:
            exception = e

        if settings.LOG_REQUESTS:
            headers_to_log = getattr(settings, 'LOG_HEADERS', ['diary-uid', 'diary-token'])
            headers = {key: request.headers.get(key) for key in headers_to_log if request.headers.get(key)}

            log_parts = [
                f"#####################\nRequest: {request.method} {request.path}",
            ]
            if headers:
                log_parts.append(f"Headers: {headers}")

            if request.method != 'GET':
                body_str = ''
                if hasattr(request, '_body'):
                    body_str = request._body.decode('utf-8', 'ignore')
                
                if body_str:
                    if len(body_str) > 1000:
                        body_str = body_str[:1000] + '...'
                    log_parts.append(f"Body: {body_str}")

            if response:
                if response.get('Content-Type', '').startswith('text/html'):
                    template_name = getattr(response, 'template_name', None)
                    if template_name:
                        log_parts.append(f"| Response: {response.status_code} for template {template_name}")
                    else:
                        log_parts.append(f"| Response: {response.status_code} for path {request.path}")
                else:
                    log_parts.append(f"| Response: {response.status_code}")
                    response_content = response.content.decode('utf-8', 'ignore')
                    if len(response_content) > 5000:
                        response_content = response_content[:5000] + '...'
                    log_parts.append(response_content)

            if exception:
                log_parts.append(f"| Exception: {exception}")

            duration = time.time() - start_time
            log_parts.append(f"| Duration: {duration:.2f}s")

            log_message = " ".join(log_parts)

            if exception or (response and response.status_code >= 400):
                request_logger.error(log_message)
            else:
                request_logger.info(log_message)

        if exception:
            raise exception

        return response
