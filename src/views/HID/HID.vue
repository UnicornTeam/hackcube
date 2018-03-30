<template>
  <div class="board">
    <cube-nav/>

    <h1 class="text-center">Cube HID Manage</h1>
    <h3 class="text-center">用Cube模拟成键盘、鼠标、HID等设备</h3>
    <br/>
    <h5>要输出的键值</h5>
    <b-form-input v-model="Key"
                  type="text"
                  placeholder="Key">
    </b-form-input>
    <br/>
    <div class="text-center">
      <Button type="ghost" icon="ios-cloud-upload-outline">Submit</Button>
    </div>


    <h5>Script</h5>
    <b-table :items="items" :fields="fields">
      <div slot="Run" slot-scope="data">
        <b-button size="sm" variant="success" @click="onClick(data.index)">Run</b-button>
      </div>
    </b-table>
  </div>
</template>

<script>
    import CubeNav from '@/components/CubeNav';

    export default {
      name: 'HID',
      components: {
        CubeNav,
      },
      data() {
        return {
          Key: null,
          uploadHost: process.env.UPLOAD_API,
          extraData: { type: 'HID-Script' },
          fields: ['Info', 'Size', 'Run'],
          items: [
            { Index: 0, Info: '539fsdf', Size: '522', Run: false },
            { Index: 1, Info: '54j3n4j', Size: '94', Run: false },
            { Index: 2, Info: 'ipfd93v', Size: '101', Run: false },
          ],
        };
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
        onUploadSuccess(response) {
          console.log(response);
          this.$Message.success('Upload success');
        },
        onUploadFail(err) {
          console.log(err);
          this.$Message.error('Upload fail');
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
