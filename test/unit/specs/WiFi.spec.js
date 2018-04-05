import Vuex from 'vuex';
import { shallow, createLocalVue } from '@vue/test-utils';
import Wifi from '@/views/Wifi/Wifi';
// import store from '@/../store';

const localVue = createLocalVue();
localVue.use(Vuex);

describe('WiFi.vue', () => {
  it('renders a value from $store.state', () => {
    const wrapper = shallow(Wifi, {
      mocks: {
        propsData: {
          wifi_fields: ['SSID', 'BSSID', 'RSSI', 'JAM'],
          client_fields: ['MAC', 'BSSID', 'RSSI', 'JAM'],
        },
        $store: new Vuex.Store({
          modules: {
            WIFI: {
              namespaced: true,
              state: {
                apList: [{
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
                }],
                staList: [{
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
                }],
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
    const defaultTitle = 'Cube Wifi Manage';
    expect(wrapper.find('.board h1').text()).to.equal(defaultTitle);
    const WifiComponent = wrapper.find(Wifi);
    expect(WifiComponent.props()).contains({ wifi_fields: ['SSID', 'BSSID', 'RSSI', 'JAM'] });
  });
});
