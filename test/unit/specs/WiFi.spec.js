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
        $store: new Vuex.Store({
          modules: {
            WIFI: {
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
            },
          },
        }),
      },
      localVue,
    });
    expect(wrapper.find('.board h1').text()).to.equal('Cube Wifi Manage');
  });
});
