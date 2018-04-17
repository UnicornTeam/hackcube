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
import Vuex from 'vuex';
import VueTimers from 'vue-timers';
// import VueNativeSock from 'vue-native-websocket';
import VueSocketio from 'vue-socket.io';
import AlloyFinger from 'alloyfinger';
import AlloyFingerPlugin from 'alloyfinger/vue/alloy_finger.vue';
import App from './App';
import router from './router';
import '../static/global.css';
import store from '../store';

Vue.use(Vant);
Vue.use(BootstrapVue);
Vue.use(iView);
Vue.use(VueTimers);
Vue.use(Vuex);
Vue.use(AlloyFingerPlugin, {
  AlloyFinger,
});
Vue.use(VueSocketio, 'ws://0.0.0.0:5000/', store);
Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  template: '<App/>',
  components: { App },
});
