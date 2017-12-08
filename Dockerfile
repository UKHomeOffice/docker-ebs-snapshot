FROM alpine:3.6

RUN apk -Uuv add --no-cache groff less python py-pip && \
    pip install boto3 && \
    apk --purge -v del py-pip

RUN adduser -S ebs

USER ebs

ADD bin/* /usr/local/bin/

ENTRYPOINT ["python", "/usr/local/bin/create_snapshots.py"]
