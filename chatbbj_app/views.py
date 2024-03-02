from pathlib import Path

from django.http import HttpResponse, Http404
from django.conf import settings


def download_file(request):
    file_path = Path(settings.MEDIA_ROOT) / 'zh_core_web_trf-3.7.2-py3-none-any.whl'  # 使用 Path 构造文件路径
    if file_path.exists():
        with file_path.open('rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'inline; filename="{file_path.name}"'
            return response
    else:
        raise Http404("文件未找到")
