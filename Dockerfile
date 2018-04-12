FROM alpine:3.7

RUN apk -Uuv add --no-cache groff less python py-pip && \
    pip install boto3 && \
    apk --purge -v del py-pip

RUN adduser -S -u 1000 ebs

USER 1000

ADD bin/* /usr/local/bin/

ENTRYPOINT ["python", "/usr/local/bin/create_snapshots.py"]
