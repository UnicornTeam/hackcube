// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Vant from 'vant';
import 'vant/lib/vant-css/index.css';
import 'iview/dist/styles/iview.css';
import iView from 'iview';
import App from './App';
import router from './router';
import '../static/global.css';


Vue.use(Vant);
Vue.use(BootstrapVue);
Vue.use(iView);
Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
});
