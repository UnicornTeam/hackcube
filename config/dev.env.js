var merge = require('webpack-merge');
var prodEnv = require('./prod.env');

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  // BACKEND_HOST: '"http://192.168.2.3:5000"',
  // UPLOAD_API: '"//192.168.2.3:5000/upload"'
  // BACKEND_HOST: '"http://192.168.3.69:5000"',
  // UPLOAD_API: '"//192.168.3.69:5000/upload"'
  BACKEND_HOST: '"http://0.0.0.0:5000"',
  UPLOAD_API: '"//0.0.0.0:5000/upload"'
});
