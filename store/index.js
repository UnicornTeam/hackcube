import Vue from 'vue';
import Vuex from 'vuex';
import createLogger from 'vuex/dist/logger';
import NFC from './modules/NFC';
import RF from './modules/RF';


Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
  modules: {
    NFC,
    RF,
  },
  strict: debug,
  plugins: debug ? [createLogger()] : [],
});
