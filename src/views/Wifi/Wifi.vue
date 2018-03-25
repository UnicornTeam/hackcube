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
  </div>
</template>

<script>
  import CubeNav from '@/components/CubeNav';

  export default {
    name: 'Wifi',
    components: {
      CubeNav,
    },
    data() {
      return {
        showDismissibleAlert: true,
      };
    },
  };
</script>

<style scoped>

</style>
