import Vue from 'vue';
import actions from './actions';
import { SET_AP_ITEMS, SET_STA_ITEMS, SET_AP_SPIN_SHOW, SET_STA_SPIN_SHOW,
  SET_SCAN_STATUS, SET_CHANNEL, SET_STA_JAM_BY_INDEX, SET_AP_JAM_BY_INDEX } from '../../mutation-types';

export default {
  namespaced: true,
  state: {
    apList: [],
    staList: [],
    apSpinShow: false,
    staSpinShow: false,
    scanStatus: 'off',
  },
  getters: {
    apCount: state => state.apList.length,
    staCount: state => state.staList.length,
  },
  actions,
  mutations: {
    [SET_AP_ITEMS](state, items) {
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
  },
};
