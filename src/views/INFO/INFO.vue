<template>
  <div style="margin: 10px">
    <cube-nav/>

    <h1 class="text-center">Cube Status Manage</h1>
    <h3 class="text-center">显示Cube设备状态</h3>
    <br/>
    <h5 class="text-center">电量</h5>
    <b-progress :value="energyPercent"
                variant="dark"
    ></b-progress>
    <br/>
    <h5 class="text-center">硬盘</h5>
    <b-progress :value="storePercent"
                variant="dark"
    ></b-progress>
    <br/><br/>

    <!-- TODO: 上传预览，上传进度 -->
    <h5>上传arduino固件</h5>
    <Upload
      :data="extraDataArdu"
      :before-upload="beforeUpload"
      action="//localhost/upload">
      <Button type="ghost" icon="ios-cloud-upload-outline">Upload files</Button>
    </Upload>
    <br/><br/>
    <div style="margin-right: 10px">
      <Input v-model="updateLog" type="textarea" :autosize="{minRows: 2,maxRows: 10}" placeholder="Enter something..."></Input>
    </div>
  </div>
</template>

<script>
  import CubeNav from '@/components/CubeNav';
  import { Upload, Button } from 'iview';

  export default {
    name: 'INFO',
    components: {
      CubeNav,
      Upload,
      Button,
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
      beforeUpload(file) {
        // TODO: Add more feature argument
        console.log(file);
      },
    },
    data() {
      return {
        updateLog: '',
        energyPercent: 68,
        storePercent: 83,
        extraDataPie: { type: 'INFO-Pie' },
        extraDataArdu: { type: 'INFO-Ardu' },
      };
    },
    created() {
      // TODO: 初始化数据
      console.log(`items is: ${this.items}`);
    },
  };
</script>

<style scoped>

</style>
