<template>
  <div class="board">
    <cube-nav/>

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
          <b-button size="sm" variant="primary" v-if="scanStatus==='off'" @click="onClickScan">Scan</b-button>
          <b-button size="sm" variant="danger" v-if="scanStatus==='on'" @click="onClickScan">Stop</b-button>
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
        <van-loading type="spinner" color="black" v-if="apSpinShow" id="aligncenter" />
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
        <van-loading type="spinner" color="black" v-if="staSpinShow" id="aligncenter" />
        <div style="clear: both;"></div>
      </div>
    </div>
    <b-pagination align="center" v-if="staCount" size="sm" :total-rows="staCount" v-model="staCurrentPage" :per-page="staPerPage">
    </b-pagination>
  </div>
</template>

<script>

import CubeNav from '@/components/CubeNav';
import axios from 'axios';
import { mapState, mapGetters, mapActions } from 'vuex';
import apis from '@/../services/api/WIFI';

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
      // keep a list of element which is active
      apActiveList: new Set(),
      staActiveList: new Set(),
    };
  },
  methods: {
    ...mapActions('WIFI', ['getAPList', 'getSTAList', 'getStarted', 'setScanStatus', 'setChannel',
      'setAPSpinShow', 'setSTASpinShow', 'changeAPJAMByIndex', 'changeSTAJAMByIndex']),
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
        if (isRunning) {
          this.apActiveList.delete(actualIndex);
        } else {
          this.apActiveList.add(actualIndex);
        }
      } else if (api === apis.STA_BLOCK) {
        actualIndex = ((this.staCurrentPage - 1) * this.staPerPage) + index;
        value = this.staList[actualIndex].MAC;
        isRunning = this.staList[actualIndex].JAM;
        this.changeSTAJAMByIndex(actualIndex);
        if (isRunning) {
          this.staActiveList.delete(actualIndex);
        } else {
          this.staActiveList.add(actualIndex);
        }
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
  },
  created() {
    if (this.scanStatus === 'on') {
      this.$timer.start('fetchWifiList');
    }
    this.getChannelList();
  },
  timers: {
    fetchWifiList: { time: 3000, autostart: false, repeat: true },
  },
  computed: {
    ...mapState(
      'WIFI',
      ['apList',
        'staList',
        'apSpinShow',
        'staSpinShow',
        'scanStatus',
      ]),
    ...mapGetters('WIFI', ['staCount', 'apCount']),
  },
  // beforeRouteLeave(to, from, next) {
  //   this.setScanStatus('off');
  //   this.controlScan('off', this.channel);
  //   // close all element still active
  //   // eslint-disable-next-line no-restricted-syntax
  //   for (const i of this.apActiveList) {
  //     this.controlBlock(apis.AP_BLOCK, i);
  //   }
  //   // eslint-disable-next-line no-restricted-syntax
  //   for (const i of this.staActiveList) {
  //     this.controlBlock(apis.STA_BLOCK, i);
  //   }
  //   next();
  // },
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
</style>
