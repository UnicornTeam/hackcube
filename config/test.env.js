var merge = require('webpack-merge')
var devEnv = require('./dev.env')

module.exports = merge(devEnv, {
  NODE_ENV: '"testing"',
  BACKEND_HOST: '"http://localhost:5000"',
  UPLOAD_API: '"//localhost:5000/upload"',
});
