import Vue from 'vue';
import Vuex from 'vuex';
import createLogger from 'vuex/dist/logger';
import WIFI from './modules/WIFI';


Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
  modules: {
    WIFI,
  },
  strict: debug,
  plugins: debug ? [createLogger()] : [],
});
