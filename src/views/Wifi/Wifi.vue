<template>
  <div>
    <cube-nav/>

    <div>
      <b-alert variant="warning"
               dismissible
               :show="showDismissibleAlert"
               @dismissed="showDismissibleAlert=false">
        <h4>Warning!</h4>
        <p>本设备仅限风险演示,请您注意自觉遵守相关法律法规.</p>
      </b-alert>
    </div>

    <h1 class="text-center">Cube Wifi Manage</h1>
    <h3 class="text-center">对工作在2.4Ghz 5Ghz设备进行安全风险检测</h3>

    <b-container>
      <b-row align-h="between">
        <b-col cols="4">
          <h4>WiFi List</h4>
        </b-col>
        <b-col cols="3">
          <b-button size="sm" variant="success">Scan</b-button>
        </b-col>
      </b-row>
    </b-container>

    <b-table :items="items" :fields="fields">
      <div slot="JAM" slot-scope="data">
        <van-switch v-model="items[data.index].JAM" @change="onSwitch" />
      </div>
    </b-table>

    <b-container>
      <b-row align-h="between">
        <b-col cols="4">
          <h4>Client List</h4>
        </b-col>
      </b-row>
    </b-container>

    <b-table :items="items2" :fields="fields2">
      <div slot="JAM" slot-scope="data">
        <van-switch v-model="items2[data.index].JAM" @change="onSwitch" />
      </div>
    </b-table>

  </div>
</template>

<script>
  /* eslint-disable no-restricted-syntax */

  import CubeNav from '@/components/CubeNav';

  export default {
    name: 'Wifi',
    components: {
      CubeNav,
    },
    data() {
      return {
        showDismissibleAlert: true,
        test: [true],
        fields: ['SSID', 'BSSID', 'RSSI', 'JAM'],
        items: [
        { Index: 0, SSID: '360WIFI-XX', BSSID: '11:22:33:44:55:66', RSSI: '-80', JAM: false },
        { Index: 1, SSID: '360WIFI-X2', BSSID: '11:22:33:44:55:66', RSSI: '-94', JAM: false },
        { Index: 2, SSID: '360WIFI-X3', BSSID: '11:22:33:44:55:66', RSSI: '-81', JAM: false },
        ],
        fields2: ['NAME', 'MAC', 'Data', 'JAM'],
        items2: [
          { Index: 0, NAME: 'iPhone', MAC: '11:22:33:44:55:66', Data: '522', JAM: false },
          { Index: 1, NAME: 'Android', MAC: '11:22:33:44:55:66', Data: '94', JAM: false },
          { Index: 2, NAME: 'iPhone', MAC: '11:22:33:44:55:66', Data: '101', JAM: false },
        ],
      };
    },
    methods: {
      onSwitch() {
        // TODO: Check which item's JAM is true and do more thing.
        // TODO: Check is wifi list or client list's item
        for (const item of this.items) {
          if (item.JAM === true) {
            console.log(item.Index);
          }
        }
      },
    },
  };
</script>

<style scoped>

</style>
