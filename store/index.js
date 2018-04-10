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
    socket: {
      isConnected: false,
      message: '',
      reconnectError: false,
    },
  },
  mutations: {
    SOCKET_ONOPEN(state) {
      const socket = state.socket;
      socket.isConnected = true;
      Vue.set(state, 'socket', socket);
    },
    SOCKET_ONCLOSE(state) {
      const socket = state.socket;
      socket.isConnected = false;
      Vue.set(state, 'socket', socket);
    },
    SOCKET_ONERROR(state, event) {
      console.error(state, event);
    },
    // default handler called for all methods
    SOCKET_ONMESSAGE(state, message) {
      Vue.set(state, 'message', message);
    },
    // mutations for reconnect methods
    SOCKET_RECONNECT(state, count) {
      console.info(state, count);
    },
    SOCKET_RECONNECT_ERROR(state) {
      const socket = state.socket;
      socket.reconnectError = true;
      Vue.set(state, 'socket', socket);
    },
  },
});
