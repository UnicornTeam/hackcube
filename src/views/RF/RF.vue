<template>
  <div style="margin: 10px">
    <cube-nav/>

    <h1 class="text-center">Cube RF Manage</h1>
    <h3 class="text-center">对工作在433Mhz,315Mhz的设备进行安全风险检测</h3>
    <br/><br/>
    <b-container>
      <b-row align-h="between">
        <b-col cols="4">
          <h4>Sniffer</h4>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="snifferSwitch" @change="onSwitch" size="25px" />
        </b-col>
      </b-row>
    </b-container>

    <b-table :items="items" :fields="fields">
      <div slot="重放" slot-scope="data">
        <b-button size="sm" variant="success" @click="onClick(data.index)">Run</b-button>
      </div>
    </b-table>

    <!-- Attack -->
    <b-container>
      <b-row align-h="between">
        <b-col cols="4">
          <h4>Attack</h4>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="attackSwitch" @change="onSwitch" size="25px" />
        </b-col>
      </b-row>
    </b-container>

    <b-progress :value="70" variant="danger" :animated="animate" class="mb-3"/>

  </div>
</template>

<script>
  /* eslint-disable no-restricted-syntax */

  import CubeNav from '@/components/CubeNav';

  export default {
    name: 'RF',
    components: {
      CubeNav,
    },
    data() {
      return {
        snifferSwitch: false,
        attackSwitch: false,
        // if continue animate
        animate: true,
        fields: ['数据', '频率', '协议', '调制', '重放'],
        items: [
          { Index: 0, 数据: 'f1a2a2f23', 频率: '315.00Mhz', 协议: 'PT226X', 调制: 'ASK', 重放: false },
          { Index: 1, 数据: 'f1a2a2682', 频率: '433.92Mhz', 协议: 'Keeloq', 调制: 'ASK', 重放: false },
          { Index: 2, 数据: 'f1jgf92f3', 频率: '433.92Mhz', 协议: 'PT224X', 调制: 'FSK', 重放: false },
        ],
      };
    },
    methods: {
      onSwitch() {
        // TODO: Check which item's JAM is true and do more thing.
        // TODO: Check is wifi list or client list's item
        for (const item of this.items) {
          console.log(item.Index);
        }
      },
      // TODO: Deal with onClick logic.
      onClick(index) {
        console.log(index);
      },
    },
  };
</script>

<style scoped>

</style>
