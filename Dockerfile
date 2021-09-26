FROM golang
RUN apt-get update
WORKDIR /go/src/app
COPY app .
EXPOSE 8080
RUN  go mod init api && go mod tidy
ENTRYPOINT ["go","run","main.go"]
