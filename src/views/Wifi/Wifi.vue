<template>
  <div class="board">
    <cube-nav/>
    <div v-for="latest_crf_item in latest_crf_items" >
      <b-alert show variant="primary" dismissible>
        <h4 class="alert-heading">RF</h4>
        <p>
          In frequency {{latest_crf_item.freq}} found prot: {{latest_crf_item.prot}}, data: {{latest_crf_item.data}} signal.<u @click="clickRF">Learn More.</u>
        </p>
      </b-alert>
    </div>
    <b-alert :show="showNFCAlert" variant="success" dismissible>
      <h4 class="alert-heading">NFC</h4>
      <p>
        Found NFC card ID: {{latest_nfc_item.ID}}, <u @click="clickNFC">Learn More.</u>
      </p>
    </b-alert>
    <h1 class="text-center">Cube Wifi Manage</h1>
    <h3 class="text-center">Security Risk Detection on 2.4Ghz 5Ghz Devices</h3>
    <br/>
    <b-container>
      <b-row >
        <b-col cols="5" style="padding-left: 0;">
          <h5>WiFi List</h5>
        </b-col>
        <b-col cols="1"></b-col>
        <b-col cols="4" style="padding-right: 4px;">
          <Select v-model="channel" size="small" placeholder="Channel" filterable>
            <Option v-for="item in channelList" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>
        </b-col>
        <b-col cols="1">
          <van-button size="small" v-if="scanStatus==='off'" @click="onClickScan">Scan</van-button>
          <van-button size="small" type="danger" v-if="scanStatus==='on'" @click="onClickScan">Stop</van-button>
        </b-col>
      </b-row>
    </b-container>
    <div>
      <b-table id="ellipsis-list" :items="apList" :fields="wifi_fields" :per-page="apPerPage" :current-page="apCurrentPage">
        <div slot="JAM" slot-scope="data">
          <b-button size="sm" variant="primary" v-if="!apList[((apCurrentPage-1) * apPerPage) + data.index].JAM"
                    @click="controlBlock('ap_block', data.index)">
            Run</b-button>
          <b-button size="sm" variant="danger" v-if="apList[((apCurrentPage-1) * apPerPage) + data.index].JAM"
                    @click="controlBlock('ap_block', data.index)">
            Stop</b-button>
        </div>
      </b-table>
      <b-pagination align="center" v-if="apCount" size="sm" :total-rows="apCount" v-model="apCurrentPage" :per-page="apPerPage">
      </b-pagination>
      <!--<Spin fix v-if="apSpinShow"></Spin>-->
      <div>
        <van-loading type="spinner" color="black" v-if="!apCount&&scanStatus==='on'" id="aligncenter" />
        <div style="clear: both;"></div>
      </div>
    </div>
    <br/><br/>

    <!-- Client list -->
    <h5>Client List</h5>
    <div>
      <b-table id="ellipsis-list" :items="staList" :fields="client_fields" :per-page="staPerPage" :current-page="staCurrentPage">
        <div slot="JAM" slot-scope="data">
          <b-button size="sm" variant="primary" v-if="!staList[((staCurrentPage-1) * staPerPage) + data.index].JAM"
                    @click="controlBlock('sta_block', data.index)">
            Run</b-button>
          <b-button size="sm" variant="danger" v-if="staList[((staCurrentPage-1) * staPerPage) + data.index].JAM"
                    @click="controlBlock('sta_block', data.index)">
            Stop</b-button>
        </div>
      </b-table>
      <!--<Spin fix v-if="staSpinShow"></Spin>-->
      <div>
        <van-loading type="spinner" color="black" v-if="!staCount&&scanStatus==='on'" id="aligncenter" />
        <div style="clear: both;"></div>
      </div>
    </div>
    <b-pagination align="center" v-if="staCount" size="sm" :total-rows="staCount" v-model="staCurrentPage" :per-page="staPerPage">
    </b-pagination>
    <b-button size="sm" variant="primary"
              @click="pingServer">
      Run</b-button>
  </div>
</template>

<script>

import CubeNav from '@/components/CubeNav';
import axios from 'axios';
import { mapState, mapGetters, mapActions } from 'vuex';
import router from '@/router';
import apis from '@/../services/api/WiFi';

export default {
  name: 'Wifi',
  components: {
    CubeNav,
  },
  data() {
    return {
      wifi_fields: ['SSID', 'BSSID', 'RSSI', 'JAM'],
      client_fields: ['MAC', 'BSSID', 'RSSI', 'JAM'],
      defaultChannel: 6,
      channelList: [],
      apPerPage: 6,
      staPerPage: 6,
      channel: 6,
      apCurrentPage: 1,
      staCurrentPage: 1,
      showNFCAlert: false,
      latest_nfc_item: '',
      latest_crf_items: [],
    };
  },
  sockets: {
    connect() {
      console.log('socket connected anderson');
      this.$socket.emit('foo', 'bar');
    },
    disconnect() {
      console.log('socket disconnect');
    },
    message(data) {
      console.log(data);
    },
    emit_method(val) {
      console.log('this method was fired by the socket server. eg: io.emit("customEmit", data)', val);
    },
  },
  methods: {
    ...mapActions('WiFi', ['getAPList', 'getSTAList', 'getStarted', 'setScanStatus', 'setChannel',
      'setAPSpinShow', 'setSTASpinShow', 'changeAPJAMByIndex', 'changeSTAJAMByIndex', 'setAPList', 'setSTAList']),
    pingServer() {
      // Send the "pingServer" event to the server.
      this.$socket.emit('message', 'Got it![Send by client]');
    },
    controlBlock(api, index) {
      let actualIndex;
      let value;
      let isRunning;
      this.setScanStatus('off');
      this.$timer.stop('fetchWifiList');
      if (api === apis.AP_BLOCK) {
        actualIndex = ((this.apCurrentPage - 1) * this.apPerPage) + index;
        value = this.apList[actualIndex].BSSID;
        isRunning = this.apList[actualIndex].JAM;
        this.changeAPJAMByIndex(actualIndex);
      } else if (api === apis.STA_BLOCK) {
        actualIndex = ((this.staCurrentPage - 1) * this.staPerPage) + index;
        value = this.staList[actualIndex].MAC;
        isRunning = this.staList[actualIndex].JAM;
        this.changeSTAJAMByIndex(actualIndex);
      } else {
        this.$Message.error('Please input the right api');
        return;
      }
      const action = isRunning ? 'off' : 'on';
      axios
        .get(`${process.env.BACKEND_HOST}/${api}/${value}/${action}`)
        .then((response) => {
          const result = response.data;
          this.$Message.success(result.message);
        })
        .catch((err) => {
          if (err.response) {
            this.$Message.error(err.response.data.message);
          } else {
            this.$Message.error('Request fail');
          }
        });
    },
    controlScan(status, channel) {
      axios
        .get(
          `${process.env.BACKEND_HOST}/wifi_scan/${status}/${channel}`,
        )
        .then(() => {
          if (status === 'on') {
            this.$timer.start('fetchWifiList');
            this.$Message.info('Start scan WiFi.');
          } else if (status === 'off') {
            this.$timer.stop('fetchWifiList');
            this.$Message.info('Stop scan WiFi.');
          }
        })
        .catch((err) => {
          if (err.response) {
            this.$Message.error(err.response.data.message);
          } else {
            this.$Message.error('Request fail');
          }
          this.setAPSpinShow(false);
          this.setSTASpinShow(false);
        });
    },
    onClickScan() {
      // send request with action to backend
      let newStatus;
      if (this.scanStatus === 'on') {
        newStatus = 'off';
      } else if (this.scanStatus === 'off') {
        newStatus = 'on';
        this.setAPSpinShow(true);
        this.setSTASpinShow(true);
      }
      this.setScanStatus(newStatus);
      const channel = this.channel === null ? this.defaultChannel : this.channel;
      this.controlScan(this.scanStatus, channel);
    },
    fetchWifiList() {
      this.getAPList().catch((err) => {
        if (err.response) {
          this.$Message.error(err.response.data.message);
        } else {
          this.$Message.error('Request fail');
        }
      });

      this.getSTAList().catch((err) => {
        if (err.response) {
          this.$Message.error(err.response.data.message);
        } else {
          this.$Message.error('Request fail');
        }
      });
    },
    fetchCRFItems() {
      const api = 'crf';
      const that = this;
      axios
        .get(`${process.env.BACKEND_HOST}/rf_item/${api}`, {
          validateStatus(status) {
            return status < 400; // Reject only if the status code is greater than or equal to 400
          },
        })
        .then((response) => {
          const result = response.data;
          // todo: write test code
          if (response.status === 304) {
            return;
          }
          const dataKey = result.data_key;
          if (result[dataKey].length > 0) {
            that.$Message.success(result.message);
          }
          // todo: change as for item of them :display notice
          if (dataKey === 'crf_item') {
            that.latest_crf_items = result[dataKey];
          }
        })
        .catch((err) => {
          if (err.response) {
            this.$Message.error(err.response.data.message);
          } else {
            this.$Message.error('Request fail');
          }
        });
    },
    clickRF() {
      router.push({
        path: '/rf',
        name: 'RF',
        params: {
          latest_crf_items: this.latest_crf_items,
        },
      });
    },
    getChannelList() {
      const channelList = [];
      const numList = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 36, 40, 44, 48,
        52, 56, 60, 64, 100, 104, 108, 112, 115, 120, 124, 128, 132,
        136, 140, 149, 153, 157, 161, 165,
      ];
      // eslint-disable-next-line no-restricted-syntax
      for (const num of numList) {
        const channel = {
          value: num,
          label: num,
        };
        channelList.push(channel);
      }
      this.channelList = channelList;
    },
    clickNFC() {
      router.push({
        path: '/nfc',
        name: 'NFC',
        params: {
          latest_nfc_item: this.latest_nfc_item,
        },
      });
    },
    fetchNFCData() {
      axios
        .get(`${process.env.BACKEND_HOST}/nfc_item`, {
          validateStatus(status) {
            return status < 400;
          },
        })
        .then((response) => {
          const result = response.data;
          if (response.status === 304) {
            return;
          }
          this.latest_nfc_item = result[result.data_key];
          this.showNFCAlert = true;
          this.$Message.info(result.message);
        })
        .catch((err) => {
          if (err.response) {
            this.$Message.error(err.response.data.message);
          } else {
            this.$Message.error('Request fail');
          }
        });
    },
  },
  created() {
    if (this.scanStatus === 'on') {
      this.$timer.start('fetchWifiList');
    }
    this.getChannelList();
    // Empty apList and staList
    this.setAPList([]);
    this.setSTAList([]);
    this.$options.sockets.event_name = (data) => {
      console.log(data);
    };
  },
  timers: {
    fetchWifiList: { time: 3400, autostart: false, repeat: true },
    fetchCRFItems: { time: 3200, autostart: true, repeat: true },
    fetchNFCData: { time: 3000, autostart: true, repeat: true },
  },
  computed: {
    ...mapState(
      'WiFi',
      ['apList',
        'staList',
        'apSpinShow',
        'staSpinShow',
        'scanStatus',
      ]),
    ...mapGetters('WiFi', ['staCount', 'apCount']),
  },
};
</script>

<style>
  #ellipsis-list td[aria-colindex] {
    overflow: hidden;
    text-overflow:ellipsis;
    white-space: nowrap;
    max-width: 6em;
    padding-right: 4px;
    padding-left: 4px;
    text-align:center;
    vertical-align:middle;
  }
  .van-button--small {
    bottom: 3px;
    right: 15px;
  }
</style>
