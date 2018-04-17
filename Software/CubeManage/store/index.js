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
  state: {
    connect: false,
    message: null,
  },
  mutations: {
    SOCKET_CONNECT: (state, status) => {
      Vue.set(state, 'connect', true);
      console.log(status);
      // state.connect = true;
    },
    SOCKET_MESSAGE: (state, message) => {
      Vue.set(state, 'message', message);
      // state.message = message;
    },
  },
  actions: {
    otherAction: (context, type) => true,
    socket_message: (context, message) => {
      context.dispatch('newMessage', message);
      context.commit('NEW_MESSAGE_RECEIVED', message);
      if (message.is_important) {
        context.dispatch('alertImportantMessage', message);
      }
    },
  },
});
