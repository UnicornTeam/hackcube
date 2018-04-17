import Vuex from 'vuex';
import { shallow, createLocalVue } from '@vue/test-utils';
import Wifi from '@/views/Wifi/Wifi';
import storeConfig from '@/../store/modules/WiFi/WiFi';
import originActions from '@/../store/modules/WiFi/actions';

const localVue = createLocalVue();
localVue.use(Vuex);
// jest.mock('axios');

describe('WiFi.vue', () => {
  const defaultWiFiField = ['SSID', 'BSSID', 'RSSI', 'JAM'];
  const defaultClientField = ['MAC', 'BSSID', 'RSSI', 'JAM'];
  let store;
  let wrapper;
  let defaultAPList;
  let defaultSTAList;
  let newActions;
  let editActions;
  let newStoreConfig;
  beforeAll(() => {
    editActions = {
      getAPList: jest.fn(),
      getSTAList: jest.fn(),
    };
    newActions = { ...originActions, ...editActions };
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
    newStoreConfig = { ...storeConfig, actions: newActions };
    store = new Vuex.Store({
      modules: {
        WiFi: newStoreConfig,
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
    expect(wrapper.find('.board h1').text()).toBe(defaultTitle);
  });

  it('should renders wifi_fields to first table from $store.state', () => {
    expect(wrapper.findAll('b-table').wrappers[0].vnode.data.attrs.fields).toEqual(defaultWiFiField);
  });
  it('should renders client_fields to second table from $store.state', () => {
    expect(wrapper.findAll('b-table').wrappers[1].vnode.data.attrs.fields).toEqual(defaultClientField);
  });

  it('should renders apList to first table from $store.state', () => {
    expect(wrapper.findAll('b-table').wrappers[0].vnode.data.attrs.items)
      .toEqual([]);
  });
  it('should renders staList to second table from $store.state', () => {
    expect(wrapper.findAll('b-table').wrappers[1].vnode.data.attrs.items)
      .toEqual([]);
  });

  it('should renders Scan button before click', () => {
    expect(wrapper.find('van-button').text()).toBe('Scan');
  });
  it('should renders Stop button after click', () => {
    wrapper.find('van-button').trigger('click');
    expect(wrapper.find('van-button').text()).toBe('Stop');
    wrapper.find('van-button').trigger('click');
  });
  it('should renders default ap_list after click', () => {
    wrapper.find('van-button').trigger('click');
    expect(editActions.getAPList).toHaveBeenCalled();
    expect(editActions.getSTAList).toHaveBeenCalled();
    wrapper.vm.$nextTick((done) => {
      expect(wrapper.vm.value).deep.equal('bar');
      expect(wrapper.findAll('b-table').wrappers[1].vnode.data.attrs.items).deep.equal('foo');
      done();
    });
  });
  it('should renders Scan button after double click', () => {
    wrapper.find('van-button').trigger('click');
    expect(wrapper.find('van-button').text()).toBe('Scan');
  });
});
