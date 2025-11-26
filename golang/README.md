`
go mod init test
go get package_name eg: go get github.com/gorilla/mux
go mod vendor
go build .
go run .\main.go

make test
make check-coverage

sudo apt install golang-golang-x-tools

pre commits stored in: Backend/.git/hooks/pre-commit

todo
USE
"github.com/go-playground/validator/v10"
add integration and ETE testing.
