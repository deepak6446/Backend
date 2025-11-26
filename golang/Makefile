# Run unit tests with coverage
test:
	go test ./... -cover -coverprofile=coverage.out -covermode=atomic

# Check coverage threshold (95%)
check-coverage: test
	@COVERAGE=$$(go tool cover -func=coverage.out | grep total | awk '{print substr($3, 1, length($3)-1)}'); \
	echo "Total coverage: $$COVERAGE%"; \
	if (( $$(echo "$$COVERAGE < 95.0" | bc -l) )); then \
		echo "❌ Coverage ($$COVERAGE%) is below required 95%"; \
		exit 1; \
	else \
		echo "✅ Coverage check passed ($$COVERAGE%)"; \
	fi
