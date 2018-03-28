<template>
  <div style="margin: 10px">
    <cube-nav/>

    <h1 class="text-center">Cube Wifi Manage</h1>
    <h3 class="text-center">对工作在2.4Ghz 5Ghz设备进行安全风险检测</h3>
    <br/>
    <b-container>
      <b-row align-h="between">
        <b-col cols="4">
          <h5>WiFi List</h5>
        </b-col>
        <b-col cols="2">
          <b-button size="sm" variant="success" @click="onClickScan">Scan</b-button>
        </b-col>
      </b-row>
    </b-container>

    <b-table :items="items" :fields="fields">
      <div slot="JAM" slot-scope="data">
        <van-switch v-model="items[data.index].JAM"
                    @change="onSwitch('ap_block', items[data.index].BSSID, data.index, items[data.index].JAM)" />
      </div>
    </b-table>


    <!-- Client list -->
    <h5>Client List</h5>
    <b-table :items="items2" :fields="fields2">
      <div slot="JAM" slot-scope="data">
        <van-switch v-model="items2[data.index].JAM"
                    @change="onSwitch('sta_block', items2[data.index].MAC, data.index, items2[data.index].JAM)" />
      </div>
    </b-table>
  </div>
</template>

<script>
  /* eslint-disable no-restricted-syntax */

  import CubeNav from '@/components/CubeNav';
  import axios from 'axios';

  export default {
    name: 'Wifi',
    components: {
      CubeNav,
    },
    data() {
      return {
        scanStatus: 'off',
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
      onSwitch(api, value, index, isOpen) {
        console.log(api, value, index, isOpen);
        const action = isOpen ? 'on' : 'off';
        axios.get(`${process.env.BACKEND_HOST}/${api}/${value}/${action}`)
          .then((response) => {
            console.log(response.data);
            const result = response.data;
            if (result.status === 'fail') {
              this.$Message.error(result.message);
            } else {
              this.$Message.success(result.message);
            }
          })
          .catch((err) => {
            console.log(err);
          });
      },
      error() {
        this.$Message.error('This is an error tip');
      },
      onClickScan() {
        // send request with action to backend
        this.scanStatus = this.scanStatus === 'on' ? 'off' : 'on';
        axios.get(`${process.env.BACKEND_HOST}/wifi_scan/${this.scanStatus}`)
          .then((response) => {
            console.log(response.data);
            const result = response.data;
            if (result.status === 'fail') {
              // TODO: show prompt when fail or success
              this.$Message.error(result.message);
            } else {
              this.$Message.success(result.message);
            }
          })
          .catch((err) => {
            console.log(err);
          });
      },
    },
    created() {
      // TODO: 初始化数据
      console.log(`items is: ${this.items}`);
    },
  };
</script>

<style scoped>

</style>
