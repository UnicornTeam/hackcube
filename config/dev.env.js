var merge = require('webpack-merge');
var prodEnv = require('./prod.env');

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  BACKEND_HOST: '"http://192.168.2.3:5000"',
  UPLOAD_API: '"//192.168.2.3:5000/upload"'
  // BACKEND_HOST: '"http://localhost:5000"',
  // UPLOAD_API: '"//localhost:5000/upload"'
});
