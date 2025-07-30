## npmrc

- .npmrc is required in your directory before installing this package.
- contents required in .npmrc

```
//npm.pkg.github.com/:_authToken=<personal_access_token>
@<repo>:registry=https://npm.pkg.github.com/<repo>
```

- personal_access_token should have access to download the package from the git repo. (this will be provided by DevOps.)

## Package Installation

Install from the command line (check latest version):

```
$ npm install @<repo>/logs-something@1.0.0
```

Install via package.json:

```
"@<repo>/logs-something": "1.0.0" (check latest version)
```

# build package on local

1. npm pack
2. mv <repo>-logs-something-0.0.0-development.tgz /Users/deepakpoojari/ (or ~)
3. add package.json dependency { "@<repo>/logs-something": "file:~/<repo>-logs-something-0.0.0-development.tgz" }
4. npm install
5. require and use in code

## How to commit code in this repo

- use: npx cz instead of git commit
- for manual commit : https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#-git-commit-guidelines