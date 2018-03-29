<template>
  <div style="margin: 10px">
    <cube-nav/>
    <b-alert :show="showRFAlert" variant="primary">
      <h4 class="alert-heading">RF</h4>
      <p>
        频率{{latest_rf_item.频率}}发现协议为{{latest_rf_item.协议}}.数据内容为{{latest_rf_item.数据}}信号.
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
          <van-switch v-model="snifferSwitch" @change="onSwitch('sniffer')" />
        </b-col>
      </b-row>
    </b-container>

    <b-table :items="items" :fields="fields_show">
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

    <b-table :items="items" :fields="fields_input">
      <div slot="电压" slot-scope="data">
        <b-form-input v-model="items[data.index].电压" type="text"></b-form-input>
      </div>
      <div slot="压力" slot-scope="data">
        <b-form-input v-model="items[data.index].压力" type="text"></b-form-input>
      </div>
      <div slot="湿度" slot-scope="data">
        <b-form-input v-model="items[data.index].湿度" type="text"></b-form-input>
      </div>
      <div slot='气阀' slot-scope="data">
        <b-form-input v-model="items[data.index].气阀" type="text"></b-form-input>
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
        latest_nfc_item: {},
        latest_rf_item: {},
        showNFCAlert: false,
        showRFAlert: false,
        snifferSwitch: true,
        tpmsSwitch: false,
        attackSwitch: false,
        // if continue animate
        animate: true,
        fields_show: ['数据', '频率', '协议', '调制', '重放'],
        fields_input: ['ID', '电压', '压力', '湿度', '气阀'],
        items: [
          { Index: 0, ID: 'f1a2a2f23', 频率: '315.00Mhz', 协议: 'PT226X', 调制: 'ASK', 重放: false, 电压: '', 压力: '', 湿度: '', 气阀: '', 数据: 'hfgh34h' },
          { Index: 1, ID: 'f1a2a2682', 频率: '433.92Mhz', 协议: 'Keeloq', 调制: 'ASK', 重放: false, 电压: '', 压力: '', 湿度: '', 气阀: '', 数据: 'hfgd3fd' },
          { Index: 2, ID: 'f1jgf92f3', 频率: '433.92Mhz', 协议: 'PT224X', 调制: 'FSK', 重放: false, 电压: '', 压力: '', 湿度: '', 气阀: '', 数据: 'sa29f9w' },
        ],
      };
    },
    methods: {
      clickNFC() {
        router.push('/nfc');
      },
      fetchData(dataApi) {
        axios
          .get(`${process.env.BACKEND_HOST}/${dataApi}`)
          .then((response) => {
            const result = response.data;
            // todo: check what 304 not modify will do
            console.log(result);
            const isExist = this.items.indexOf(result[dataApi]) !== -1;
            if (isExist) {
              return;
            }
            // TODO: 1. NFC是否也放进去items？
            // TODO: 2. 服务器端和前端字段不一致怎么解决
            this.items.unshift(result[dataApi]);
            switch (dataApi) {
              case 'nfc_item':
                this.latest_nfc_item = result[dataApi];
                this.showNFCAlert = true;
                break;
              case 'rf_item':
                this.latest_rf_item = result[dataApi];
                this.showRFAlert = true;
                break;
              default:
                break;
            }
          })
          .catch((err) => {
            console.log(err);
            this.$Message.error('Fetch nfc data fail.');
          });
      },
      onSwitch(switchType) {
        console.log(switchType);
      },
      // TODO: Deal with onClick logic.
      onClick(index) {
        console.log(index);
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
