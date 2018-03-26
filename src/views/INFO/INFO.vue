<template>
  <div style="margin: 10px">
    <cube-nav/>

    <h1 class="text-center">Cube Status Manage</h1>
    <h3 class="text-center">显示Cube设备状态</h3>
    <br/>
    <h4 class="text-center">电量</h4>
    <b-progress :value="energyPercent"
                variant="dark"
    ></b-progress>
    <br/>
    <h4 class="text-center">硬盘</h4>
    <b-progress :value="storePercent"
                variant="dark"
    ></b-progress>
    <br/><br/>

    <!-- TODO: 上传预览，上传进度 -->
    <h5>上传arduino固件</h5>
    <van-uploader :after-read="onRead" multiple>
      <b-button size="sm" variant="outline-secondary">
        Choose File
      </b-button>
    </van-uploader>
    <br/><br/>

    <h5>上传树莓派固件</h5>
    <van-uploader :after-read="onRead" multiple>
      <b-button size="sm" variant="outline-secondary">
        Choose File
      </b-button>
    </van-uploader>
  </div>
</template>

<script>
  import CubeNav from '@/components/CubeNav';

  export default {
    name: 'INFO',
    components: {
      CubeNav,
    },
    methods: {
      onRead(file, content) {
        console.log(file);
        console.log(content);
        console.log(Buffer.from(file.content, 'base64').toString('utf-8'));
        // TODO: Send result to backend
        // TODO: Add upload success prompt
      },
      // TODO: Deal with onClick logic.
      onClick(index) {
        console.log(index);
      },
    },
    data() {
      return {
        energyPercent: 68,
        storePercent: 83,
      };
    },
  };
</script>

<style scoped>

</style>
