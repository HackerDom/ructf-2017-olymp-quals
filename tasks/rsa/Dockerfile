FROM python:3-onbuild
ENV PYTHONUNBUFFERED 1

CMD ["gunicorn", "crypto:app", "--bind", "0.0.0.0:8000", "--worker-class", "aiohttp.worker.GunicornWebWorker", "--workers", "2"]
