module.exports = {
    //Steps to Ensure 95%+ Coverage
    collectCoverage: true,
    collectCoverageFrom: [
      '**/*.(t|j)s',
      '!<rootDir>/node_modules/',
      '!<rootDir>/*.module.(t|j)s', // exclude boilerplate
    ],
    coverageThreshold: {
      global: {
        branches: 95,
        functions: 95,
        lines: 95,
        statements: 95,
      },
    },
    //END - Steps to Ensure 95%+ Coverage
  };
  