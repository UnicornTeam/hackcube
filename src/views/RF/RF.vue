<template>
  <div class="board">
    <cube-nav/>
    <b-alert :show="showARFAlert" variant="primary">
      <h4 class="alert-heading">RF</h4>
      <p>
        频率{{latest_arf_item.频率}}发现协议为{{latest_arf_item.协议}}.数据内容为{{latest_arf_item.数据}}信号.
      </p>
    </b-alert>

    <b-alert :show="showNFCAlert" variant="success">
      <h4 class="alert-heading">NFC</h4>
      <p>
        捕获卡号:{{latest_nfc_item.id}}, <u href="#" @click="clickNFC">点击查看</u>
      </p>
    </b-alert>

    <h1 class="text-center">Cube RF Manage</h1>
    <h3 class="text-center">对工作在433Mhz,315Mhz的设备进行安全风险检测</h3>
    <br/><br/>
    <b-container>
      <b-row align-h="between">
        <b-col cols="4">
          <h5>Sniffer</h5>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="snifferSwitch" @change="onSwitch('sniffer')" ></van-switch>
        </b-col>
      </b-row>
    </b-container>

    <b-table :items="rfItems" :fields="fields_show">
      <div slot="重放" slot-scope="data">
        <b-button size="sm" variant="success" @click="onClick(data.index)">Run</b-button>
      </div>
    </b-table>


    <b-container>
      <b-row align-h="between">
        <b-col cols="4">
          <h5>TPMS</h5>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="tpmsSwitch" @change="onSwitch('tpms')" />
        </b-col>
      </b-row>
    </b-container>

    <b-table :items="tpmsItems" :fields="fields_input">
      <div slot="电压" slot-scope="data">
        <b-form-input v-model="tpmsItems[data.index].电压" type="text"></b-form-input>
      </div>
      <div slot="压力" slot-scope="data">
        <b-form-input v-model="tpmsItems[data.index].压力" type="text"></b-form-input>
      </div>
      <div slot="温度" slot-scope="data">
        <b-form-input v-model="tpmsItems[data.index].温度" type="text"></b-form-input>
      </div>
      <div slot='气阀' slot-scope="data">
        <b-form-input v-model="tpmsItems[data.index].气阀" type="text"></b-form-input>
      </div>
    </b-table>


    <!-- Attack -->
    <b-container>
      <b-row align-h="between">
        <b-col cols="4">
          <h5>Attack</h5>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="attackSwitch" @change="onSwitch('attack')" />
        </b-col>
      </b-row>
    </b-container>

    <b-progress :value="70" variant="danger" :animated="animate" class="mb-3"/>

  </div>
</template>

<script>
  /* eslint-disable no-restricted-syntax */

  import CubeNav from '@/components/CubeNav';
  import axios from 'axios';
  import router from '@/router';

  export default {
    name: 'RF',
    components: {
      CubeNav,
    },
    data() {
      return {
        // todo: set latest_nfc_item and showNFCAlert from NFC page
        latest_nfc_item: '',
        showNFCAlert: false,
        latest_arf_item: '',
        showARFAlert: false,
        snifferSwitch: true,
        tpmsSwitch: false,
        attackSwitch: false,
        // if continue animate
        animate: true,
        fields_show: ['数据', '频率', '协议', '调制', '重放'],
        fields_input: ['ID', '电压', '压力', '温度', '气阀'],
        rfItems: [
          { 频率: '315.00Mhz', 协议: 'PT226X', 调制: 'ASK', 重放: false, 数据: 'hfgh34h' },
          { 频率: '433.92Mhz', 协议: 'Keeloq', 调制: 'ASK', 重放: false, 数据: 'hfgd3fd' },
          { 频率: '433.92Mhz', 协议: 'PT224X', 调制: 'FSK', 重放: false, 数据: 'sa29f9w' },
        ],
        tpmsItems: [
          { ID: '20959185', 电压: '', 压力: '', 温度: '', 气阀: '' },
          { ID: 'eb107f85', 电压: '', 压力: '', 温度: '', 气阀: '' },
          { ID: 'F0FB2385', 电压: '', 压力: '', 温度: '', 气阀: '' },
          { ID: '2093ef85', 电压: '', 压力: '', 温度: '', 气阀: '' },
        ],
      };
    },
    methods: {
      clickNFC() {
        router.push('/nfc');
      },
      serialSend(parameter) {
        axios
          .get(`${process.env.BACKEND_HOST}/serial_send/${parameter}`)
          .then((response) => {
            const result = response.data;
            console.log(result);
            this.$Message.success('Execute success.');
          })
          .catch((err) => {
            console.log(err.response);
            this.$Message.error('Execute fail.');
          });
      },
      fetchData() {
        const dataAPIs = ['arf', 'crf'];
        for (const api of dataAPIs) {
          axios
            .get(`${process.env.BACKEND_HOST}/rf_item/${api}`, {
              validateStatus(status) {
                return status < 400; // Reject only if the status code is greater than or equal to 400
              },
            })
            .then((response) => {
              const result = response.data;
              // todo: check what 304 not modify will do
              // todo: write test code
              console.log(result);
              if (response.status === 304) {
                return;
              }
              const dataKey = result.data_key;
              const isExist = this.rfItems.indexOf(result[dataKey]) !== -1;
              if (isExist) {
                return;
              }
              this.rfItems.unshift(result[dataKey]);
              if (dataKey === 'arf_item') {
                this.latest_arf_item = result[dataKey];
                this.showARFAlert = true;
              }
            })
            .catch((err) => {
              console.log(err.response);
              this.$Message.error(`Fetch ${api} data fail.`);
            });
        }
      },
      onSwitch(switchType) {
        console.log(switchType);
        switch (switchType) {
          case 'sniffer':
            if (this.snifferSwitch) {
              this.$timer.start('fetchData');
            } else {
              this.$timer.stop('fetchData');
            }
            break;
          case 'tpms':
            // todo: send data to serial_send
            if (!this.tpmsSwitch) {
              return;
            }
            for (const item in this.tpmsItems) {
              // todo: write test code
              if (!item.电压 && !item.压力 && !item.温度 && !item.气阀) {
                // this.$Message.error('You need input one or more.');
                return;
              }
              const parameter = `t${item.ID}${item.电压}${item.压力}${item.温度}${item.气阀}`;
              setTimeout(function timer() {
                // todo: does it need promotion after per request send?
                this.serialSend(parameter);
              }, 700);
            }
            this.$Message.success('Send all valid item to process!');
            break;
          default:
            break;
        }
      },
      // TODO: Deal with onClick logic.
      onClick(index) {
        console.log(index);
        const item = this.rfItems[index];
        const parameter = `rfreq:${item.频率};protocol:${item.协议};modulation:${item.调制};data:${item.数据}`;
        this.serialSend(parameter);
      },
    },
    created() {
      // TODO: 初始化数据
      if (this.snifferSwitch) {
        this.$timer.start('fetchData');
      }
    },
    timers: {
      fetchData: { time: 3000, autostart: false, repeat: true },
    },
  };
</script>

<style scoped>

</style>
