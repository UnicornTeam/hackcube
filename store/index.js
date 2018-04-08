import Vue from 'vue';
import Vuex from 'vuex';
import createLogger from 'vuex/dist/logger';
import createPersistedState from 'vuex-persistedstate';
import WiFi from './modules/WiFi/WiFi';

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
  modules: {
    WiFi,
  },
  strict: debug,
  plugins: debug
    ? [
      createLogger(),
      createPersistedState(),
    ]
    : [
      createPersistedState(),
    ],
});
