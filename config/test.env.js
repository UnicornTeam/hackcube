var merge = require('webpack-merge')
var devEnv = require('./dev.env')

module.exports = merge(devEnv, {
  NODE_ENV: '"testing"',
  BACKEND_HOST: '"http://192.168.2.3:5000"',
  UPLOAD_API: '"//192.168.2.3:5000/upload"',
});
