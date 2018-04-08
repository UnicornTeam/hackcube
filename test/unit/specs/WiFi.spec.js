import Vuex from 'vuex';
import { shallow, createLocalVue } from '@vue/test-utils';
import Wifi from '@/views/Wifi/Wifi';

const localVue = createLocalVue();
localVue.use(Vuex);

describe('WiFi.vue', () => {
  const defaultAPList = [{
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

  const defaultSTAList = [{
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

  const defaultWiFiField = ['SSID', 'BSSID', 'RSSI', 'JAM'];
  const defaultClientField = ['MAC', 'BSSID', 'RSSI', 'JAM'];

  const wrapper = shallow(Wifi, {
    mocks: {
      propsData: {
        wifi_fields: defaultWiFiField,
        client_fields: defaultClientField,
      },
      $store: new Vuex.Store({
        modules: {
          WIFI: {
            namespaced: true,
            state: {
              apList: defaultAPList,
              staList: defaultSTAList,
              apSpinShow: false,
              staSpinShow: false,
              scanStatus: 'off',
            },
            getters: {
              apCount: state => state.apList.length,
              staCount: state => state.staList.length,
            },
          },
        },
      }),
    },
    localVue,
  });
  it('should render title correctly', () => {
    const defaultTitle = 'Cube Wifi Manage';
    expect(wrapper.find('.board h1').text()).to.equal(defaultTitle);
  });
  it('should renders wifi_fields from $store.state', () => {
    expect(wrapper.vm.wifi_fields).deep.equal(defaultWiFiField);
  });
  it('should renders client_fields from $store.state', () => {
    expect(wrapper.vm.client_fields).deep.equal(defaultClientField);
  });
  it('should renders apList from $store.state', () => {
    expect(wrapper.vm.apList).deep.equal(defaultAPList);
  });
});
