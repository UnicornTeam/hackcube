import {
  SET_AP_ITEMS, SET_AP_JAM_BY_INDEX,
  SET_AP_SPIN_SHOW, SET_CHANNEL,
  SET_SCAN_STATUS,
  SET_STA_ITEMS,
  SET_STA_JAM_BY_INDEX, SET_STA_SPIN_SHOW,
} from '@/../store/mutation-types';
import services from '@/../services/WiFi';

export default {
  getAPList({ state, commit }) {
      // commit(SET_AP_SPIN_SHOW, true);
    return services.getAPList()
        .then((resp) => {
          if (resp.status !== 304) {
            const result = resp.data;
            const items = result[result.data_key];
            commit('setAPItems', items);
            commit(SET_AP_SPIN_SHOW, false);
          } else if (state.apSpinShow) {
            commit(SET_AP_SPIN_SHOW, false);
          }
        }).catch((err) => {
          commit('setAPSpinShow', false);
          return Promise.reject(err);
        });
  },
  getSTAList({ state, commit }) {
      // commit(SET_STA_SPIN_SHOW, true);
    return services.getSTAList()
        .then((resp) => {
          if (resp.status !== 304) {
            const result = resp.data;
            const items = result[result.data_key];
            commit('setSTAItems', items);
            commit(SET_STA_SPIN_SHOW, false);
          } else if (state.staSpinShow) {
            commit(SET_STA_SPIN_SHOW, false);
          }
        }).catch((err) => {
          commit('setSTASpinShow', false);
          return Promise.reject(err);
        });
  },
  otherAction: (context, type) => true,
  socket_message: (context, message) => {
    context.dispatch('newMessage', message);
    context.commit('NEW_MESSAGE_RECEIVED', message);
    if (message.is_important) {
      context.dispatch('alertImportantMessage', message);
    }
  },
  setAPList({ commit }, apList) {
    commit(SET_AP_ITEMS, apList);
  },
  setSTAList({ commit }, staList) {
    commit(SET_STA_ITEMS, staList);
  },
  setScanStatus({ commit }, status) {
    commit(SET_SCAN_STATUS, status);
  },
  setChannel({ commit }, channel) {
    commit(SET_CHANNEL, channel);
  },
  setAPSpinShow({ commit }, status) {
    commit(SET_AP_SPIN_SHOW, status);
  },
  setSTASpinShow({ commit }, status) {
    commit(SET_STA_SPIN_SHOW, status);
  },
  changeSTAJAMByIndex({ commit }, index) {
    commit(SET_STA_JAM_BY_INDEX, index);
  },
  changeAPJAMByIndex({ commit }, index) {
    commit(SET_AP_JAM_BY_INDEX, index);
  },
};

