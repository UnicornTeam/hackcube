import Vuex from 'vuex';
// import 'iview/dist/styles/iview.css';
import iView from 'iview';
import { shallow, createLocalVue } from '@vue/test-utils';
import Wifi from '@/views/Wifi/Wifi';
import storeConfig from '@/../store/modules/WiFi/WiFi';

test('WiFi.vue', (done) => {
  const localVue = createLocalVue();
  localVue.use(Vuex);
  localVue.use(iView);
  const store = new Vuex.Store({
    modules: {
      WiFi: storeConfig,
    },
  });
  const defaultWiFiField = ['SSID', 'BSSID', 'RSSI', 'JAM'];
  const defaultClientField = ['MAC', 'BSSID', 'RSSI', 'JAM'];
  const wrapper = shallow(Wifi, {
    mocks: {
      propsData: {
        wifi_fields: defaultWiFiField,
        client_fields: defaultClientField,
      },
      $store: store,
    },
    localVue,
  });

  wrapper.find('van-button').trigger('click');
  wrapper.vm.$nextTick(() => {
    expect(wrapper.vm.value).toBe('value');
    done();
  });
});

