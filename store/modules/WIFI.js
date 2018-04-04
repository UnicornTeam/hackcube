import Vue from 'vue';
import services from '../../services';
import { SET_API_ITEMS, SET_STA_ITEMS, SET_AP_SPIN_SHOW, SET_STA_SPIN_SHOW,
  SET_SCAN_STATUS, SET_CHANNEL, SET_STA_JAM_BY_INDEX, SET_AP_JAM_BY_INDEX } from '../mutation-types';

const namespaced = true;
// initial state
const state = {
  apList: [],
  staList: [],
  apSpinShow: false,
  staSpinShow: false,
  scanStatus: 'off',
};

// getters
const getters = {
  apCount: state => state.apList.length,
  staCount: state => state.staList.length,
};

// actions
const actions = {
  getAPList({ commit }) {
    // commit(SET_AP_SPIN_SHOW, true);
    return services.WIFI.getAPList()
        .then((resp) => {
          if (resp.status !== 304) {
            const result = resp.data;
            const items = result[result.data_key];
            commit('setAPItems', items);
          }
          commit(SET_AP_SPIN_SHOW, false);
          return true;
        }).catch((err) => {
          commit('setAPSpinShow', false);
          return Promise.reject(err);
        });
  },
  getSTAList({ commit }) {
    // commit(SET_STA_SPIN_SHOW, true);
    return services.WIFI.getSTAList()
      .then((resp) => {
        if (resp.status !== 304) {
          const result = resp.data;
          const items = result[result.data_key];
          commit('setSTAItems', items);
        }
        commit(SET_STA_SPIN_SHOW, false);
      }).catch((err) => {
        commit('setSTASpinShow', false);
        return Promise.reject(err);
      });
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


// mutations
const mutations = {
  [SET_API_ITEMS](state, items) {
      // state.apList = items;
    Vue.set(state, 'apList', items);
  },
  [SET_STA_ITEMS](state, items) {
      // state.apList = items;
    Vue.set(state, 'staList', items);
  },
  [SET_AP_SPIN_SHOW](state, status) {
    Vue.set(state, 'apSpinShow', status);
  },
  [SET_STA_SPIN_SHOW](state, status) {
    Vue.set(state, 'staSpinShow', status);
  },
  [SET_SCAN_STATUS](state, status) {
    Vue.set(state, 'scanStatus', status);
  },
  [SET_CHANNEL](state, channel) {
    Vue.set(state, 'channel', channel);
  },
  [SET_STA_JAM_BY_INDEX](state, index) {
    const staList = state.staList;
    staList[index].JAM = staList[index].JAM === false;
    Vue.set(state, 'staList', staList);
  },
  [SET_AP_JAM_BY_INDEX](state, index) {
    const apList = state.apList;
    apList[index].JAM = apList[index].JAM === false;
    Vue.set(state, 'apList', apList);
  },
};

export default {
  namespaced,
  state,
  getters,
  mutations,
  actions,
};
