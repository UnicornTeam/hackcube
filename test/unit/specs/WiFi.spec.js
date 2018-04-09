import Vuex from 'vuex';
import { Button } from 'vant';
import { shallow, createLocalVue } from '@vue/test-utils';
import Wifi from '@/views/Wifi/Wifi';
import storeConfig from '@/../store/modules/WiFi/WiFi';
import { SET_AP_SPIN_SHOW, SET_AP_ITEMS, SET_STA_ITEMS, SET_SCAN_STATUS, SET_CHANNEL,
  SET_STA_SPIN_SHOW, SET_AP_JAM_BY_INDEX, SET_STA_JAM_BY_INDEX } from '../../../store/mutation-types';
// eslint-disable-next-line import/no-webpack-loader-syntax
const actionInjector = require('!!vue-loader?inject!@/../store/modules/WiFi/actions');

const localVue = createLocalVue();
localVue.use(Vuex);

describe('WiFi.vue', () => {
  const defaultWiFiField = ['SSID', 'BSSID', 'RSSI', 'JAM'];
  const defaultClientField = ['MAC', 'BSSID', 'RSSI', 'JAM'];
  let store;
  let wrapper;
  // storeConfig.action = actions;
  let newStoreConfig;
  let actions;
  let defaultAPList;
  let defaultSTAList;
  before(() => {
    defaultAPList = [{
      Index: 0,
      SSID: '360WIFI-XX',
      BSSID: '11:22:33:44:55:66',
      RSSI: '-80',
      JAM: false,
    },
    {
      Index: 1,
      SSID: '360WIFI-X2',
      BSSID: '11:22:33:44:55:66',
      RSSI: '-94',
      JAM: false,
    },
    {
      Index: 2,
      SSID: '360WIFI-X3',
      BSSID: '11:22:33:44:55:66',
      RSSI: '-81',
      JAM: false,
    }];

    defaultSTAList = [{
      Index: 0,
      NAME: 'iPhone',
      MAC: '11:22:33:44:55:66',
      RSSI: '522',
      JAM: false,
    },
    {
      Index: 1,
      NAME: 'Android',
      MAC: '11:22:33:44:55:66',
      RSSI: '94',
      JAM: false,
    },
    {
      Index: 2,
      NAME: 'iPhone',
      MAC: '11:22:33:44:55:66',
      RSSI: '101',
      JAM: false,
    }];
    actionInjector({
      '@/../services/WiFi': {
        getAPList: ({ commit }) => setTimeout(() => {
          // mock apList
          commit('setAPItems', defaultAPList);
          commit(SET_AP_SPIN_SHOW, false);
        }, 100),
        getSTAList: ({ commit }) => setTimeout(() => {
          // mock staList
          commit('setAPItems', defaultSTAList);
          commit(SET_AP_SPIN_SHOW, false);
        }, 100),
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
      },
    });
    // newStoreConfig = { ...storeConfig, actions };
    store = new Vuex.Store({
      modules: {
        WIFI: storeConfig,
      },
    });
    wrapper = shallow(Wifi, {
      mocks: {
        propsData: {
          wifi_fields: defaultWiFiField,
          client_fields: defaultClientField,
        },
        $store: store,
      },
      localVue,
    });
  });


  it('should render title correctly', () => {
    const defaultTitle = 'Cube Wifi Manage';
    expect(wrapper.find('.board h1').text()).to.equal(defaultTitle);
  });

  it('should renders wifi_fields to first table from $store.state', () => {
    expect(wrapper.findAll('b-table').wrappers[0].vnode.data.attrs.fields).deep.equal(defaultWiFiField);
  });
  it('should renders client_fields to second table from $store.state', () => {
    expect(wrapper.findAll('b-table').wrappers[1].vnode.data.attrs.fields).deep.equal(defaultClientField);
  });

  it('should renders apList to first table from $store.state', () => {
    expect(wrapper.findAll('b-table').wrappers[0].vnode.data.attrs.items)
      .deep.equal([]);
  });
  it('should renders staList to second table from $store.state', () => {
    expect(wrapper.findAll('b-table').wrappers[1].vnode.data.attrs.items)
      .deep.equal([]);
  });

  it('should renders Scan button before click', () => {
    expect(wrapper.find(Button).text()).to.equal('Scan');
  });
  it('should renders Stop button after click', () => {
    wrapper.find('van-button').trigger('click');
    expect(wrapper.find('van-button').text()).to.equal('Stop');
  });

  it('should renders Scan button after double click', () => {
    wrapper.find('van-button').trigger('click');
    expect(wrapper.find('van-button').text()).to.equal('Scan');
  });
});
