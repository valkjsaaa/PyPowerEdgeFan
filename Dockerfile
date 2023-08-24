FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /PyPowerEdgeFan

COPY requirements.txt /PyPowerEdgeFan/
RUN apt-get update && apt-get install -y lm-sensors ipmitool
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /PyPowerEdgeFan

CMD if [ -z "$HOST" ] && [ -z "$USERNAME" ] && [ -z "$PASSWORD" ]; then \
python ./poweredge_fan/poweredge_fan.py -I $HIGH -L $LOW -T $TARGET; else \
python ./poweredge_fan/poweredge_fan.py -H $HOST -U $USERNAME -P $PASSWORD -I $HIGH -L $LOW -T $TARGET; fi
